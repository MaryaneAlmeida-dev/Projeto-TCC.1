import sqlite3
import hashlib
import os
from datetime import datetime

class Database:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados e cria as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                sobrenome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                telefone TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

        
    
    def hash_password(self, password):
        """Gera hash da senha usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    


    def create_user(self, nome, sobrenome, cpf, telefone, data_nascimento, email, senha):
        """Cria um novo usuário no banco de dados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            senha_hash = self.hash_password(senha)
            
            cursor.execute('''
                INSERT INTO users (nome, sobrenome, cpf, telefone, data_nascimento, email, senha_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nome, sobrenome, cpf, telefone, data_nascimento, email, senha_hash))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {"success": True, "user_id": user_id}
        
        except sqlite3.IntegrityError as e:
            conn.close()
            if "cpf" in str(e).lower():
                return {"success": False, "error": "CPF já cadastrado"}
            elif "email" in str(e).lower():
                return {"success": False, "error": "Email já cadastrado"}
            else:
                return {"success": False, "error": "Dados já existem no sistema"}
        
        except Exception as e:
            conn.close()
            return {"success": False, "error": f"Erro interno: {str(e)}"}
        
    
    def authenticate_user(self, login, senha):
        """Autentica usuário por email ou CPF"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            senha_hash = self.hash_password(senha)
            
            #busca por email ou CPF
            cursor.execute('''
                SELECT id, nome, sobrenome, email, cpf FROM users 
                WHERE (email = ? OR cpf = ?) AND senha_hash = ?
            ''', (login, login, senha_hash))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    "success": True,
                    "user": {
                        "id": user[0],
                        "nome": user[1],
                        "sobrenome": user[2],
                        "email": user[3],
                        "cpf": user[4]
                    }
                }
            else:
                return {"success": False, "error": "Email/CPF ou senha incorretos"}
        
        except Exception as e:
            return {"success": False, "error": f"Erro interno: {str(e)}"}
        



    
    def get_user_by_id(self, user_id):
        """Busca usurio por ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, nome, sobrenome, email, cpf, telefone, data_nascimento, created_at 
                FROM users WHERE id = ?
            ''', (user_id,))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    "success": True,
                    "user": {
                        "id": user[0],
                        "nome": user[1],
                        "sobrenome": user[2],
                        "email": user[3],
                        "cpf": user[4],
                        "telefone": user[5],
                        "data_nascimento": user[6],
                        "created_at": user[7]
                    }
                }
            else:
                return {"success": False, "error": "Usuário não encontrado"}
        
        except Exception as e:
            return {"success": False, "error": f"Erro interno: {str(e)}"}

