import asyncio
from fastapi import Request, HTTPException

__all__ = ["check_rate_limit"]


# Rate limiting por IP: máximo de 60 requisições por minuto
from collections import defaultdict, deque
import time

RATE_LIMIT = 60  # requisições por minuto
_ip_requests = defaultdict(lambda: deque())

async def check_rate_limit(request: Request):
    client_ip = request.client.host or request.headers.get("X-Forwarded-For", "unknown")
    now = time.time()
    requests = _ip_requests[client_ip]
    # Remove requisições antigas (mais de 1 minuto)
    while requests and now - requests[0] > 60:
        requests.popleft()
    requests.append(now)
    if len(requests) > RATE_LIMIT:
        # Registra evento de segurança
        try:
            from src.interfaces.shared.security.security_monitor import security_monitor
            await security_monitor.log_rate_limit_exceeded(request, client_ip)
        except Exception:
            pass
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Tente novamente mais tarde.")
    return
