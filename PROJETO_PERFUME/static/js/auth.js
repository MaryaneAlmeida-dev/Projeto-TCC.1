
class BelleAuth {
    constructor() {
        this.baseURL = '';
        this.init();
    }

    init() {
        // Interceptar formulário de login
        const loginForm = document.querySelector('#loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        }

        // Interceptar formulário de cadastro
        const registerForm = document.querySelector('#registerForm');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => this.handleRegister(e));
        }

        // Botão de logout
        const logoutBtn = document.querySelector('#logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', (e) => this.handleLogout(e));
        }
    }

    async handleLogin(event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        
        const data = {
            login: formData.get('email') || formData.get('login'),
            senha: formData.get('senha')
        };

        try {
            this.showLoading('Fazendo login...');
            
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            this.hideLoading();

            if (result.success) {
                this.showSuccess(result.message);
                // Redirecionar para página principal após 1 segundo
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                this.showError(result.message || 'Erro no login');
                if (result.errors) {
                    result.errors.forEach(error => this.showError(error));
                }
            }
        } catch (error) {
            this.hideLoading();
            this.showError('Erro de conexão. Tente novamente.');
            console.error('Erro no login:', error);
        }
    }

    async handleRegister(event) {
        event.preventDefault();
        
        const form = event.target;
        const formData = new FormData(form);
        
        const data = {
            nome: formData.get('nome'),
            sobrenome: formData.get('sobrenome'),
            cpf: formData.get('cpf'),
            telefone: formData.get('telefone'),
            data_nascimento: formData.get('data'),
            email: formData.get('email'),
            senha: formData.get('senha'),
            confirmar_senha: formData.get('confirmar-senha')
        };

        try {
            this.showLoading('Criando conta...');
            
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            this.hideLoading();

            if (result.success) {
                this.showSuccess(result.message);
                // redirecionar para login após 2 segundos
                setTimeout(() => {
                    window.location.href = '/loginpage.html';
                }, 2000);
            } else {
                this.showError(result.message || 'Erro no cadastro');
                if (result.errors) {
                    result.errors.forEach(error => this.showError(error));
                }
            }
        } catch (error) {
            this.hideLoading();
            this.showError('Erro de conexão. Tente novamente.');
            console.error('Erro no cadastro:', error);
        }
    }

    async handleLogout(event) {
        event.preventDefault();
        
        try {
            const response = await fetch('/api/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const result = await response.json();
            
            if (result.success) {
                this.showSuccess(result.message);
                // redirecionar para pagina principal
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            }
        } catch (error) {
            console.error('Erro no logout:', error);
            // Mesmo com erro, redirecionar
            window.location.href = '/';
        }
    }

    async checkAuth() {
        try {
            const response = await fetch('/api/check-auth');
            const result = await response.json();
            
            if (result.success && result.data.authenticated) {
                return result.data.user;
            }
            return null;
        } catch (error) {
            console.error('Erro ao verificar autenticação:', error);
            return null;
        }
    }

    showLoading(message) {
        this.hideMessages();
        const loadingDiv = document.createElement('div');
        loadingDiv.id = 'loading-message';
        loadingDiv.className = 'message loading';
        loadingDiv.innerHTML = `
            <div class="loading-spinner"></div>
            <span>${message}</span>
        `;
        document.body.appendChild(loadingDiv);
    }

    hideLoading() {
        const loading = document.getElementById('loading-message');
        if (loading) {
            loading.remove();
        }
    }

    showSuccess(message) {
        this.hideMessages();
        const successDiv = document.createElement('div');
        successDiv.id = 'success-message';
        successDiv.className = 'message success';
        successDiv.textContent = message;
        document.body.appendChild(successDiv);
        
        setTimeout(() => {
            successDiv.remove();
        }, 5000);
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message error';
        errorDiv.textContent = message;
        
        // Adicionar ao container de erros ou criar um
        let errorContainer = document.getElementById('error-container');
        if (!errorContainer) {
            errorContainer = document.createElement('div');
            errorContainer.id = 'error-container';
            document.body.appendChild(errorContainer);
        }
        
        errorContainer.appendChild(errorDiv);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }

    hideMessages() {
        const messages = document.querySelectorAll('.message');
        messages.forEach(msg => msg.remove());
    }

    // Utilitário para formatar CPF
    static formatCPF(cpf) {
        return cpf.replace(/\D/g, '')
                 .replace(/(\d{3})(\d)/, '$1.$2')
                 .replace(/(\d{3})(\d)/, '$1.$2')
                 .replace(/(\d{3})(\d{1,2})/, '$1-$2')
                 .replace(/(-\d{2})\d+?$/, '$1');
    }

    // Utilitário para formatar telefone
    static formatPhone(phone) {
        return phone.replace(/\D/g, '')
                   .replace(/(\d{2})(\d)/, '($1) $2')
                   .replace(/(\d{4})(\d)/, '$1-$2')
                   .replace(/(\d{4})-(\d)(\d{4})/, '$1$2-$3')
                   .replace(/(-\d{4})\d+?$/, '$1');
    }
}







// Inicializar sistema de autenticação
document.addEventListener('DOMContentLoaded', () => {
    window.belleAuth = new BelleAuth();
    
    // Adicionar formatação automática aos campos
    const cpfField = document.getElementById('cpf');
    if (cpfField) {
        cpfField.addEventListener('input', (e) => {
            e.target.value = BelleAuth.formatCPF(e.target.value);
        });
    }
    
    const phoneField = document.getElementById('telefone');
    if (phoneField) {
        phoneField.addEventListener('input', (e) => {
            e.target.value = BelleAuth.formatPhone(e.target.value);
        });
    }
});

