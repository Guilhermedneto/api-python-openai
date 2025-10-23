"""
Sistema de monitoramento e alertas com Rollbar para detecção de ataques DDoS e problemas de segurança.
"""
import rollbar
import structlog
import time
from typing import Dict, Optional, Any
from collections import defaultdict, deque
from fastapi import Request
from enum import Enum
from dataclasses import dataclass, asdict


class SecurityEventType(Enum):
    """Tipos de eventos de segurança."""
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    DDOS_ATTACK_DETECTED = "ddos_attack_detected"
    SQL_INJECTION_ATTEMPT = "sql_injection_attempt"
    XSS_ATTEMPT = "xss_attempt"
    SUSPICIOUS_REQUEST = "suspicious_request"
    AUTHENTICATION_FAILURE = "authentication_failure"
    UNAUTHORIZED_ACCESS = "unauthorized_access"


@dataclass
class SecurityEvent:
    """Evento de segurança."""
    event_type: SecurityEventType
    client_ip: str
    timestamp: float
    request_path: str
    user_agent: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    severity: str = "warning"
    details: Optional[Dict[str, Any]] = None


class SecurityMonitor:
    """
    Monitor de segurança com integração ao Rollbar.
    """
    
    def __init__(self, rollbar_token: Optional[str] = None, environment: str = "development"):
        """
        Inicializa o monitor de segurança.
        
        Args:
            rollbar_token: Token do Rollbar para envio de alertas
            environment: Ambiente (development, production, etc.)
        """
        self.rollbar_enabled = bool(rollbar_token)
        self.environment = environment
        
        # Configuração do logger estruturado
        self.logger = structlog.get_logger("security_monitor")
        
        # Configuração do Rollbar se token fornecido
        if self.rollbar_enabled:
            rollbar.init(
                rollbar_token,
                environment=environment,
                handler="default"
            )
            self.logger.info("Rollbar inicializado", environment=environment)
        
        # Tracking de eventos para detecção de padrões
        self.events_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.ip_request_count: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        
        # Configurações de detecção
        self.ddos_threshold = 1000  # Requisições por minuto por IP
        self.suspicious_pattern_threshold = 10  # Eventos suspeitos por hora
    
    async def log_security_event(self, event: SecurityEvent):
        """
        Registra um evento de segurança.
        
        Args:
            event: Evento de segurança a ser registrado
        """
        # Log estruturado local
        self.logger.warning(
            "Security event detected",
            event_type=event.event_type.value,
            client_ip=event.client_ip,
            request_path=event.request_path,
            severity=event.severity,
            details=event.details or {}
        )
        
        # Adiciona ao histórico para análise de padrões
        self.events_history[event.client_ip].append(event)
        
        # Envia para Rollbar se habilitado
        if self.rollbar_enabled:
            await self._send_to_rollbar(event)
        
        # Verifica se é um possível ataque DDoS
        await self._check_ddos_pattern(event)
    
    async def log_rate_limit_exceeded(self, request: Request, client_ip: str):
        """
        Log específico para rate limiting excedido.
        
        Args:
            request: Requisição FastAPI
            client_ip: IP do cliente
        """
        event = SecurityEvent(
            event_type=SecurityEventType.RATE_LIMIT_EXCEEDED,
            client_ip=client_ip,
            timestamp=time.time(),
            request_path=str(request.url.path),
            user_agent=request.headers.get("User-Agent"),
            severity="warning",
            details={
                "method": request.method,
                "query_params": dict(request.query_params),
                "headers": dict(request.headers)
            }
        )
        
        await self.log_security_event(event)
    
    async def log_suspicious_request(self, request: Request, client_ip: str, reason: str, payload: Any = None):
        """
        Log para requisições suspeitas (SQL injection, XSS, etc.).
        
        Args:
            request: Requisição FastAPI
            client_ip: IP do cliente
            reason: Motivo da suspeita
            payload: Dados da requisição suspeita
        """
        event_type = SecurityEventType.SUSPICIOUS_REQUEST
        
        # Identifica tipo específico baseado na razão
        if "sql" in reason.lower() or "injection" in reason.lower():
            event_type = SecurityEventType.SQL_INJECTION_ATTEMPT
        elif "xss" in reason.lower() or "script" in reason.lower():
            event_type = SecurityEventType.XSS_ATTEMPT
        
        event = SecurityEvent(
            event_type=event_type,
            client_ip=client_ip,
            timestamp=time.time(),
            request_path=str(request.url.path),
            user_agent=request.headers.get("User-Agent"),
            payload=payload,
            severity="high" if "injection" in reason.lower() else "warning",
            details={
                "reason": reason,
                "method": request.method,
                "content_length": request.headers.get("Content-Length", "0")
            }
        )
        
        await self.log_security_event(event)
    
    async def _send_to_rollbar(self, event: SecurityEvent):
        """
        Envia evento para o Rollbar.
        
        Args:
            event: Evento de segurança
        """
        try:
            # Prepara dados para Rollbar
            extra_data = {
                "security_event": asdict(event),
                "environment": self.environment,
                "timestamp": event.timestamp
            }
            
            # Envia baseado na severidade
            if event.severity == "high" or event.event_type == SecurityEventType.DDOS_ATTACK_DETECTED:
                rollbar.report_message(
                    f"SECURITY ALERT: {event.event_type.value}",
                    level="error",
                    extra_data=extra_data
                )
            else:
                rollbar.report_message(
                    f"Security event: {event.event_type.value}",
                    level="warning",
                    extra_data=extra_data
                )
                
        except Exception as e:
            self.logger.error("Failed to send event to Rollbar", error=str(e))
    
    async def _check_ddos_pattern(self, event: SecurityEvent):
        """
        Verifica padrões de possível ataque DDoS.
        
        Args:
            event: Evento de segurança atual
        """
        client_ip = event.client_ip
        now = time.time()
        
        # Adiciona requisição ao contador
        self.ip_request_count[client_ip].append(now)
        
        # Remove requisições antigas (mais de 1 minuto)
        while (self.ip_request_count[client_ip] and 
               now - self.ip_request_count[client_ip][0] > 60):
            self.ip_request_count[client_ip].popleft()
        
        # Verifica se excede threshold de DDoS
        request_count = len(self.ip_request_count[client_ip])
        if request_count > self.ddos_threshold:
            ddos_event = SecurityEvent(
                event_type=SecurityEventType.DDOS_ATTACK_DETECTED,
                client_ip=client_ip,
                timestamp=now,
                request_path=event.request_path,
                severity="critical",
                details={
                    "requests_per_minute": request_count,
                    "threshold": self.ddos_threshold,
                    "user_agent": event.user_agent
                }
            )
            
            # Log crítico para DDoS
            self.logger.critical(
                "POSSIBLE DDOS ATTACK DETECTED",
                client_ip=client_ip,
                requests_per_minute=request_count,
                threshold=self.ddos_threshold
            )
            
            # Envia alerta crítico se Rollbar habilitado
            if self.rollbar_enabled:
                await self._send_to_rollbar(ddos_event)
    
    def get_security_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas de segurança.
        
        Returns:
            Dict com estatísticas atuais
        """
        now = time.time()
        recent_events = []
        
        # Coleta eventos das últimas 24 horas
        for ip, events in self.events_history.items():
            for event in events:
                if now - event.timestamp < 86400:  # 24 horas
                    recent_events.append(event)
        
        # Conta por tipo
        event_counts = defaultdict(int)
        for event in recent_events:
            event_counts[event.event_type.value] += 1
        
        return {
            "total_events_24h": len(recent_events),
            "unique_ips_24h": len(set(event.client_ip for event in recent_events)),
            "events_by_type": dict(event_counts),
            "rollbar_enabled": self.rollbar_enabled,
            "environment": self.environment
        }


# Instância global do monitor com token do Rollbar
security_monitor = SecurityMonitor(
    rollbar_token='7ffc24ac2c5b460097e98da83e39c56c',
    environment='development'
)