class HeaderController {
    constructor() {
        this.init();
    }

    async init() {
        await this.updateHeaderBasedOnAuth();
    }

    async updateHeaderBasedOnAuth() {
        try {
            const response = await fetch('/api/check-auth');
            const result = await response.json();
            
            const userIcon = document.querySelector('.usuario');
            const userLink = userIcon ? userIcon.parentElement : null;
            
            if (result.success && result.data.authenticated) {
                // Usuário logado - mostrar link para perfil
                if (userLink) {
                    userLink.href = '/profile.html';
                    userLink.title = `Perfil de ${result.data.user.nome}`;
                }
                
                // indicador visual se tiver logado
                if (userIcon) {
                    userIcon.style.filter = 'brightness(1.2)';
                    userIcon.style.border = '2px solid #4CAF50';
                    userIcon.style.borderRadius = '50%';
                }
            } else {
                // Usuario não logado - mostrar link para login
                if (userLink) {
                    userLink.href = '/loginpage.html';
                    userLink.title = 'Fazer login';
                }
                
                // remove indicadores visuais
                if (userIcon) {
                    userIcon.style.filter = '';
                    userIcon.style.border = '';
                    userIcon.style.borderRadius = '';
                }
            }
        } catch (error) {
            console.error('Erro ao verificar autenticação:', error);
            const userLink = document.querySelector('.usuario')?.parentElement;
            if (userLink) {
                userLink.href = '/loginpage.html';
            }
        }
    }

    async refresh() {
        await this.updateHeaderBasedOnAuth();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.headerController = new HeaderController();
});

window.addEventListener('focus', () => {
    if (window.headerController) {
        window.headerController.refresh();
    }
});

