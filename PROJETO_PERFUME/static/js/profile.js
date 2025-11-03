
class ProfileManager {
    constructor() {
        this.init();
    }

    async init() {
        await this.loadProfile();
        this.setupEventListeners();
    }

    async loadProfile() {
        try {
            const response = await fetch('/api/profile');
            const result = await response.json();

            if (result.success) {
                this.displayProfile(result.data);
            } else {
                this.displayError(result.message || 'Erro ao carregar perfil');
                
                // Se não autenticado, redirecionar para login
                if (response.status === 401) {
                    setTimeout(() => {
                        window.location.href = '/loginpage.html';
                    }, 2000);
                }
            }
        } catch (error) {
            console.error('Erro ao carregar perfil:', error);
            this.displayError('Erro de conexão. Tente novamente.');
        }
    }

    displayProfile(userData) {
        const profileInfo = document.getElementById('profileInfo');
        
        // Formatar data de nascimento
        const dataNascimento = new Date(userData.data_nascimento).toLocaleDateString('pt-BR');
        
        // Formatar data de cadastro
        const dataCadastro = new Date(userData.created_at).toLocaleDateString('pt-BR');
        
        // Formatar CPF
        const cpfFormatado = this.formatCPF(userData.cpf);
        
        // Formatar telefone
        const telefoneFormatado = this.formatPhone(userData.telefone);

        profileInfo.innerHTML = `
            <div class="info-grid">
                <div class="info-card">
                    <h3>
                        <span>👤</span>
                        Informações Pessoais
                    </h3>
                    <p><strong>Nome:</strong> ${userData.nome} ${userData.sobrenome}</p>
                    <p><strong>Data de Nascimento:</strong> ${dataNascimento}</p>
                    <p><strong>CPF:</strong> ${cpfFormatado}</p>
                </div>

                <div class="info-card">
                    <h3>
                        <span>📞</span>
                        Contato
                    </h3>
                    <p><strong>Email:</strong> ${userData.email}</p>
                    <p><strong>Telefone:</strong> ${telefoneFormatado}</p>
                </div>

                <div class="info-card">
                    <h3>
                        <span>📅</span>
                        Informações da Conta
                    </h3>
                    <p><strong>Cliente desde:</strong> ${dataCadastro}</p>
                    <p><strong>ID da Conta:</strong> #${userData.id.toString().padStart(6, '0')}</p>
                </div>

                <div class="info-card">
                    <h3>
                        <span>🎁</span>
                        Benefícios
                    </h3>
                    <p><strong>Status:</strong> <span style="color: #4CAF50;">Cliente Ativo</span></p>
                    <p><strong>Desconto Primeira Compra:</strong> <span style="color: #ff6b6b;">10% OFF</span></p>
                </div>
            </div>
        `;
    }

    displayError(message) {
        const profileInfo = document.getElementById('profileInfo');
        profileInfo.innerHTML = `
            <div class="profile-error">
                <h3>😔 Ops! Algo deu errado</h3>
                <p>${message}</p>
                <a href="/loginpage.html" class="btn btn-secondary">
                    <span>🔑</span>
                    Fazer Login
                </a>
            </div>
        `;
    }

    setupEventListeners() {
        // Botão de logout já é tratado pelo auth.js
        // Apenas garantir que está funcionando
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn && !logoutBtn.hasAttribute('data-listener')) {
            logoutBtn.setAttribute('data-listener', 'true');
            logoutBtn.addEventListener('click', async (e) => {
                e.preventDefault();
                
                if (confirm('Tem certeza que deseja sair da sua conta?')) {
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
            });
        }
    }

    formatCPF(cpf) {
        return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    }

    formatPhone(phone) {
        if (phone.length === 11) {
            return phone.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        } else if (phone.length === 10) {
            return phone.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
        }
        return phone;
    }

    showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'message success';
        successDiv.textContent = message;
        document.body.appendChild(successDiv);
        
        setTimeout(() => {
            successDiv.remove();
        }, 3000);
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message error';
        errorDiv.textContent = message;
        document.body.appendChild(errorDiv);
        
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
}

// Inicializar gerenciador de perfil
document.addEventListener('DOMContentLoaded', () => {
    window.profileManager = new ProfileManager();
});

