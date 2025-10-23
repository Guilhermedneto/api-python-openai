import urllib.parse
from typing import Dict, Optional


class SqlServerConnectionHelper:
    """
    Utilitário para trabalhar com strings de conexão do SQL Server.
    """
    
    @staticmethod
    def parse_connection_string(connection_string: str) -> Dict[str, str]:
        """
        Parseia uma string de conexão do SQL Server.
        
        Args:
            connection_string: String de conexão no formato SQL Server
            
        Returns:
            Dict com os componentes da conexão
        """
        components = {}
        
        # Divide a string por ponto e vírgula
        pairs = connection_string.split(';')
        
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                components[key.strip()] = value.strip()
        
        return components
    
    @staticmethod
    def to_sqlalchemy_url(connection_string: str, database_name: str = "UsuariosDB") -> str:
        """
        Converte uma string de conexão SQL Server para URL do SQLAlchemy.
        
        Args:
            connection_string: String de conexão original
            database_name: Nome do banco de dados a ser criado/usado
            
        Returns:
            URL do SQLAlchemy para SQL Server
        """
        components = SqlServerConnectionHelper.parse_connection_string(connection_string)
        
        # Extrai o servidor (aceita SERVER ou Data Source)
        data_source = components.get('SERVER') or components.get('Data Source') or 'localhost'
        server_parts = data_source.split('\\')
        server = server_parts[0]
        instance = server_parts[1] if len(server_parts) > 1 else None

        # Constrói a URL base
        if instance:
            server_string = f"{server}\\{instance}"
        else:
            server_string = server

        # Verifica se usa autenticação integrada (Windows Authentication)
        integrated_security = (
            components.get('Trusted_Connection', 'False').lower() == 'yes' or
            components.get('Integrated Security', 'False').lower() == 'true'
        )
        
        if integrated_security:
            # Autenticação Windows
            driver = "ODBC Driver 17 for SQL Server"
            encoded_driver = urllib.parse.quote_plus(driver)
            
            # Parâmetros adicionais
            params = []
            
            if components.get('TrustServerCertificate', 'False').lower() == 'true':
                params.append('TrustServerCertificate=yes')
            
            if components.get('Encrypt', 'False').lower() == 'true':
                params.append('Encrypt=yes')
            
            params_string = '&'.join(params)
            
            # URL completa
            url = f"mssql+pyodbc://@{server_string}/{database_name}?driver={encoded_driver}"
            if params_string:
                url += f"&{params_string}"
                
        else:
            # Se não for autenticação integrada, seria necessário usuário e senha
            # Por enquanto, assumimos autenticação Windows
            raise ValueError("Autenticação por usuário/senha não implementada neste exemplo")
        
        return url
    
    @staticmethod
    def get_master_db_url(connection_string: str) -> str:
        """
        Obtém a URL para conectar ao banco master (usado para criar o banco).
        
        Args:
            connection_string: String de conexão original
            
        Returns:
            URL do SQLAlchemy para o banco master
        """
        return SqlServerConnectionHelper.to_sqlalchemy_url(connection_string, "master")


# Exemplo de uso
if __name__ == "__main__":
    # Sua string de conexão
    conn_str = "Data Source=HOME\\SQLEXPRESS;Integrated Security=True;Persist Security Info=False;Pooling=False;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=True;Application Name=\"SQL Server Management Studio\";Command Timeout=30"
    
    helper = SqlServerConnectionHelper()
    
    # URL para o banco master
    master_url = helper.get_master_db_url(conn_str)
    print(f"Master DB URL: {master_url}")
    
    # URL para o banco da aplicação
    app_url = helper.to_sqlalchemy_url(conn_str, "UsuariosDB")
    print(f"App DB URL: {app_url}")