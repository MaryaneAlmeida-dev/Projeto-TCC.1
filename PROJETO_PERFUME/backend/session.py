import uuid
import time
from datetime import datetime, timedelta

class SessionManager:
    def __init__(self):
        # Armazena sessões em memória 
        self.sessions = {}
        self.session_timeout = 3600  # 1 hora em segundos
    
    def create_session(self, user_id, user_data):
        """Cria uma nova sessão para o usuário"""
        session_id = str(uuid.uuid4())
        expires_at = time.time() + self.session_timeout
        
        self.sessions[session_id] = {
            'user_id': user_id,
            'user_data': user_data,
            'created_at': time.time(),
            'expires_at': expires_at,
            'last_activity': time.time()
        }
        
        return session_id
    
    def get_session(self, session_id):
        """Recupera dados da sessão se válida"""
        if not session_id or session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Verifica se a sessão expirou
        if time.time() > session['expires_at']:
            self.destroy_session(session_id)
            return None
        
        # Atualiza última atividade
        session['last_activity'] = time.time()
        
        return session
    
    def destroy_session(self, session_id):
        """Remove uma sessão"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def is_authenticated(self, session_id):
        """Verifica se o usuário está autenticado"""
        session = self.get_session(session_id)
        return session is not None
    
    def get_user_data(self, session_id):
        """Retorna dados do usuário da sessão"""
        session = self.get_session(session_id)
        if session:
            return session['user_data']
        return None
    
    def cleanup_expired_sessions(self):
        """Remove sessões expiradas (deve ser chamado periodicamente)"""
        current_time = time.time()
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if current_time > session['expires_at']
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        return len(expired_sessions)
    
    def extend_session(self, session_id):
        """Estende o tempo de vida da sessão"""
        if session_id in self.sessions:
            self.sessions[session_id]['expires_at'] = time.time() + self.session_timeout
            return True
        return False

