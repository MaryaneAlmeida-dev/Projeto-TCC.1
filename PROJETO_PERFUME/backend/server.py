import http.server
import socketserver
import os
import json
from urllib.parse import urlparse, parse_qs
from backend.database import Database
from backend.auth import AuthValidator
from backend.session import SessionManager
from backend.utils import HTTPUtils, FileUtils, ResponseBuilder




class BelleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    db = Database()
    session_manager = SessionManager()
    
    def __init__(self, *args, **kwargs):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Manipula requisições GET"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Rotas da API
        if path.startswith('/api/'):
            self.handle_api_get(path)
        else:
            self.serve_static_file(path)
    
    def do_POST(self):
        """Manipula requisições POST"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path.startswith('/api/'):
            self.handle_api_post(path)
        else:
            self.send_error(404, "Not Found")
    
    def do_OPTIONS(self):
        """Manipula requisições OPTIONS (CORS)"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def handle_api_get(self, path):
        """Manipula requisições GET da API"""
        if path == '/api/profile':
            self.get_profile()
        elif path == '/api/check-auth':
            self.check_auth()
        else:
            self.send_json_response(ResponseBuilder.error("Endpoint não encontrado"), 404)
    
    def handle_api_post(self, path):
        """Manipula requisições POST da API"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        content_type = self.headers.get('Content-Type', '')
        
        data = HTTPUtils.parse_post_data(content_type, post_data)
        
        if path == '/api/register':
            self.register_user(data)
        elif path == '/api/login':
            self.login_user(data)
        elif path == '/api/logout':
            self.logout_user()
        else:
            self.send_json_response(ResponseBuilder.error("Endpoint não encontrado"), 404)
    
    def register_user(self, data):
        """Registra novo usuário"""
        #valida dados
        validation = AuthValidator.validate_registration_data(data)
        if not validation['valid']:
            self.send_json_response(
                ResponseBuilder.validation_error(validation['errors']), 
                400
            )
            return
        
        #criar usuário no banco
        result = self.db.create_user(
            nome=data['nome'].strip(),
            sobrenome=data['sobrenome'].strip(),
            cpf=data['cpf'].strip(),
            telefone=data['telefone'].strip(),
            data_nascimento=data['data_nascimento'],
            email=data['email'].strip().lower(),
            senha=data['senha']
        )
        
        if result['success']:
            self.send_json_response(
                ResponseBuilder.success(message="Cadastro realizado com sucesso!")
            )
        else:
            self.send_json_response(
                ResponseBuilder.error(result['error']), 
                400
            )
    
    def login_user(self, data):
        """Autentica usuário"""
        validation = AuthValidator.validate_login_data(data)
        if not validation['valid']:
            self.send_json_response(
                ResponseBuilder.validation_error(validation['errors']), 
                400
            )
            return
        
        # autenticar usuário
        result = self.db.authenticate_user(
            login=data['login'].strip(),
            senha=data['senha']
        )
        
        if result['success']:
            # Criar sessão
            session_id = self.session_manager.create_session(
                user_id=result['user']['id'],
                user_data=result['user']
            )
            
            # Enviar resposta com cookie
            response = ResponseBuilder.success(
                data=result['user'],
                message="Login realizado com sucesso!"
            )
            
            self.send_json_response_with_cookie(response, 'session_id', session_id)
        else:
            self.send_json_response(
                ResponseBuilder.error(result['error']), 
                401
            )
    
    def logout_user(self):
        """Faz logout do usuário"""
        session_id = self.get_session_id()
        if session_id:
            self.session_manager.destroy_session(session_id)
        
        response = ResponseBuilder.success(message="Logout realizado com sucesso!")
        self.send_json_response_with_cookie(response, 'session_id', '', max_age=0)
    
    def get_profile(self):
        """Retorna dados do perfil do usuário"""
        session_id = self.get_session_id()
        if not session_id:
            self.send_json_response(ResponseBuilder.error("Não autenticado"), 401)
            return
        
        user_data = self.session_manager.get_user_data(session_id)
        if not user_data:
            self.send_json_response(ResponseBuilder.error("Sessão inválida"), 401)
            return
        
        # Buscar dados completos do usuário
        result = self.db.get_user_by_id(user_data['id'])
        if result['success']:
            self.send_json_response(ResponseBuilder.success(data=result['user']))
        else:
            self.send_json_response(ResponseBuilder.error(result['error']), 404)
    
    def check_auth(self):
        """Verifica se usuário está autenticado"""
        session_id = self.get_session_id()
        is_authenticated = self.session_manager.is_authenticated(session_id)
        
        if is_authenticated:
            user_data = self.session_manager.get_user_data(session_id)
            self.send_json_response(ResponseBuilder.success(data={
                'authenticated': True,
                'user': user_data
            }))
        else:
            self.send_json_response(ResponseBuilder.success(data={
                'authenticated': False
            }))
    
    def serve_static_file(self, path):
        """Serve arquivos estáticos"""
        if path == '/':
            path = '/index.html'
        
        file_path = os.path.join(self.base_path, path.lstrip('/'))
        
        if not FileUtils.file_exists(file_path):
            self.send_error(404, "File Not Found")
            return
        
        content = FileUtils.read_file(file_path)
        if content is None:
            self.send_error(500, "Internal Server Error")
            return
        
        content_type = HTTPUtils.get_content_type(file_path)
        
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)
    
    def get_session_id(self):
        """Extrai session_id dos cookies"""
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            cookies = HTTPUtils.parse_cookies(cookie_header)
            return cookies.get('session_id')
        return None
    
    def send_json_response(self, data, status_code=200):
        """Envia resposta JSON"""
        response = HTTPUtils.create_json_response(data, status_code)
        
        self.send_response(response['status_code'])
        for header, value in response['headers'].items():
            self.send_header(header, value)
        self.end_headers()
        self.wfile.write(response['body'].encode('utf-8'))
    
    def send_json_response_with_cookie(self, data, cookie_name, cookie_value, max_age=3600):
        """Envia resposta JSON com cookie"""
        response = HTTPUtils.create_json_response(data)
        
        self.send_response(response['status_code'])
        for header, value in response['headers'].items():
            self.send_header(header, value)
        
        # Adicionar cookie
        cookie = HTTPUtils.create_cookie(cookie_name, cookie_value, max_age)
        self.send_header('Set-Cookie', cookie)
        
        self.end_headers()
        self.wfile.write(response['body'].encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override para personalizar logs"""
        print(f"[{self.date_time_string()}] {format % args}")

def start_server(port=8000):
    """Inicia o servidor"""
    handler = BelleHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Servidor Belle Parfum iniciado em http://localhost:{port}")
        print("Acesse http://localhost:8000 para ver o site")
        print("Pressione Ctrl+C para parar o servidor")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor parado pelo usuário")
            httpd.shutdown()

if __name__ == "__main__":
    start_server()

