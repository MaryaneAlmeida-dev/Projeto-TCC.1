"""
Script de inicialização do Belle Parfum
Sistema de login e cadastro integrado
"""

import os
import sys
import signal
import threading
import time
from backend.server import start_server
from backend.database import Database

def setup_database():
    """Inicializa o banco de dados"""
    print("🗄️  Inicializando banco de dados...")
    try:
        db = Database()
        print("✅ Banco de dados inicializado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        return False

def cleanup_sessions():
    """Limpa sessões expiradas periodicamente"""
    from backend.server import BelleHTTPRequestHandler
    
    while True:
        try:
            time.sleep(300)  # 5 minutos
            expired = BelleHTTPRequestHandler.session_manager.cleanup_expired_sessions()
            if expired > 0:
                print(f"🧹 Limpeza automática: {expired} sessões expiradas removidas")
        except Exception as e:
            print(f"⚠️  Erro na limpeza de sessões: {e}")

def signal_handler(signum, frame):
    """Manipula sinais do sistema para encerramento gracioso"""
    print("\n🛑 Encerrando servidor...")
    sys.exit(0)

def main():
    """Função principal"""
    print("🌟 Belle Parfum - Sistema de Autenticação")
    print("=" * 50)
    
    if not os.path.exists('index.html'):
        print("❌ Erro: Execute este script no diretório PROJETO_PERFUME")
        print("💡 Dica: cd PROJETO_PERFUME && python run.py")
        sys.exit(1)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Inicializar banco de dados
    if not setup_database():
        sys.exit(1)
    
    cleanup_thread = threading.Thread(target=cleanup_sessions, daemon=True)
    cleanup_thread.start()
    print("🧹 Sistema de limpeza automática de sessões iniciado")
    
    print("\n📋 Informações do Sistema:")
    print("   • Backend: Python HTTP Server")
    print("   • Banco de Dados: SQLite")
    print("   • Autenticação: Sessões com Cookies")
    print("   • Validações: CPF, Email, Telefone")
    
    print("\n🔗 Endpoints da API:")
    print("   • POST /api/register - Cadastro de usuário")
    print("   • POST /api/login - Login de usuário")
    print("   • POST /api/logout - Logout de usuário")
    print("   • GET /api/profile - Dados do perfil")
    print("   • GET /api/check-auth - Verificar autenticação")
    
    print("\n📱 Páginas Disponíveis:")
    print("   • / - Página principal")
    print("   • /loginpage.html - Login")
    print("   • /cadastro.html - Cadastro")
    print("   • /profile.html - Perfil do usuário")
    
    #definir porta
    port = int(os.environ.get('PORT', 8000))
    
    print(f"\n🚀 Iniciando servidor na porta {port}...")
    print("=" * 50)
    
    try:
        start_server(port)
    except KeyboardInterrupt:
        print("\n🛑 Servidor encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no servidor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

