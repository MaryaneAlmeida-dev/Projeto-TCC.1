import json
import mimetypes
import os
from urllib.parse import parse_qs, urlparse

class HTTPUtils:
    @staticmethod
    def parse_post_data(content_type, post_data):
        """Parse dados POST baseado no Content-Type"""
        if 'application/json' in content_type:
            try:
                return json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError:
                return {}
        
        elif 'application/x-www-form-urlencoded' in content_type:
            try:
                parsed = parse_qs(post_data.decode('utf-8'))
                # Converte listas de um elemento em strings
                return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}
            except:
                return {}
        
        return {}
    
    @staticmethod
    def get_content_type(file_path):
        """Retorna o Content-Type baseado na extensão do arquivo"""
        content_type, _ = mimetypes.guess_type(file_path)
        return content_type or 'application/octet-stream'
    
    @staticmethod
    def create_json_response(data, status_code=200):
        """Cria resposta JSON padronizada"""
        return {
            'status_code': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            },
            'body': json.dumps(data, ensure_ascii=False)
        }
    
    @staticmethod
    def create_redirect_response(location, status_code=302):
        """Cria resposta de redirecionamento"""
        return {
            'status_code': status_code,
            'headers': {
                'Location': location,
                'Access-Control-Allow-Origin': '*'
            },
            'body': ''
        }
    
    @staticmethod
    def parse_cookies(cookie_header):
        """Parse cookies do header HTTP"""
        cookies = {}
        if cookie_header:
            for cookie in cookie_header.split(';'):
                if '=' in cookie:
                    key, value = cookie.strip().split('=', 1)
                    cookies[key] = value
        return cookies
    
    @staticmethod
    def create_cookie(name, value, max_age=3600, path='/', httponly=True):
        """Cria string de cookie HTTP"""
        cookie_parts = [f"{name}={value}"]
        
        if max_age:
            cookie_parts.append(f"Max-Age={max_age}")
        
        if path:
            cookie_parts.append(f"Path={path}")
        
        if httponly:
            cookie_parts.append("HttpOnly")
        
        return '; '.join(cookie_parts)

class FileUtils:
    @staticmethod
    def read_file(file_path):
        """Lê arquivo e retorna conteúdo"""
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            return None
        except Exception:
            return None
    
    @staticmethod
    def file_exists(file_path):
        """Verifica se arquivo existe"""
        return os.path.isfile(file_path)
    
    @staticmethod
    def get_file_size(file_path):
        """Retorna tamanho do arquivo"""
        try:
            return os.path.getsize(file_path)
        except:
            return 0

class ResponseBuilder:
    @staticmethod
    def success(data=None, message="Sucesso"):
        """Cria resposta de sucesso"""
        response = {"success": True, "message": message}
        if data:
            response["data"] = data
        return response
    
    @staticmethod
    def error(message="Erro interno", errors=None):
        """Cria resposta de erro"""
        response = {"success": False, "message": message}
        if errors:
            response["errors"] = errors
        return response
    
    @staticmethod
    def validation_error(errors):
        """Cria resposta de erro de validação"""
        return {
            "success": False,
            "message": "Dados inválidos",
            "errors": errors
        }

