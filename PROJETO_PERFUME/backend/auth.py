import re
from datetime import datetime

class AuthValidator:
    @staticmethod
    def validate_email(email):
        """Valida formato do email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_cpf(cpf):
        """Valida CPF brasileiro"""
        # remove caracteres não numericos
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        # verifica se tem 11 digitos
        if len(cpf) != 11:
            return False
        
        # verifica se todos os digitos são iguais
        if cpf == cpf[0] * 11:
            return False
        
        # validação do primeiro digito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        if int(cpf[9]) != digito1:
            return False
        
        # validação do segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        return int(cpf[10]) == digito2
    
    @staticmethod
    def validate_phone(phone):
        """Valida telefone brasileiro"""
        # Remove caracteres não numéricos
        phone = re.sub(r'[^0-9]', '', phone)
        
        # Verifica se tem 10 ou 11 dígitos (com ou sem 9 no celular)
        return len(phone) in [10, 11] and phone.isdigit()
    
    @staticmethod
    def validate_password(password):
        """Valida senha (mínimo 6 caracteres)"""
        return len(password) >= 6
    
    @staticmethod
    def validate_name(name):
        """Valida nome (mínimo 2 caracteres, apenas letras e espaços)"""
        return len(name.strip()) >= 2 and re.match(r'^[a-zA-ZÀ-ÿ\s]+$', name.strip())
    
    @staticmethod
    def validate_date(date_str):
        """Valida data de nascimento"""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            # Verifica se a pessoa tem pelo menos 13 anos
            today = datetime.now()
            age = today.year - date_obj.year - ((today.month, today.day) < (date_obj.month, date_obj.day))
            return age >= 13
        except ValueError:
            return False
    
    @classmethod
    def validate_registration_data(cls, data):
        """Valida todos os dados de cadastro"""
        errors = []
        
        # Validar nome
        if not data.get('nome') or not cls.validate_name(data['nome']):
            errors.append("Nome deve ter pelo menos 2 caracteres e conter apenas letras")
        
        if not data.get('sobrenome') or not cls.validate_name(data['sobrenome']):
            errors.append("Sobrenome deve ter pelo menos 2 caracteres e conter apenas letras")
        
        if not data.get('cpf') or not cls.validate_cpf(data['cpf']):
            errors.append("CPF inválido")
        
        if not data.get('telefone') or not cls.validate_phone(data['telefone']):
            errors.append("Telefone deve ter 10 ou 11 dígitos")
        
        if not data.get('data_nascimento') or not cls.validate_date(data['data_nascimento']):
            errors.append("Data de nascimento inválida ou idade menor que 13 anos")
        
        if not data.get('email') or not cls.validate_email(data['email']):
            errors.append("Email inválido")
        
        if not data.get('senha') or not cls.validate_password(data['senha']):
            errors.append("Senha deve ter pelo menos 6 caracteres")
        
        # validar confirmação de senha
        if data.get('senha') != data.get('confirmar_senha'):
            errors.append("Senhas não coincidem")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    @classmethod
    def validate_login_data(cls, data):
        """Valida dados de login"""
        errors = []
        
        # validar login (email ou CPF)
        login = data.get('login', '').strip()
        if not login:
            errors.append("Email ou CPF é obrigatório")
        elif not (cls.validate_email(login) or cls.validate_cpf(login)):
            errors.append("Email ou CPF inválido")
        
        #validar senha
        if not data.get('senha'):
            errors.append("Senha é obrigatória")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

