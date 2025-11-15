class CarrinhoManager {
    constructor() {
        this.carrinho = this.carregarCarrinho();
    }

    carregarCarrinho() {
        const carrinhoSalvo = localStorage.getItem('carrinho');
        return carrinhoSalvo ? JSON.parse(carrinhoSalvo) : [];
    }

    salvarCarrinho() {
        localStorage.setItem('carrinho', JSON.stringify(this.carrinho));
    }

    adicionarProduto(produto) {
        const produtoExistente = this.carrinho.find(item => item.id === produto.id);
        
        if (produtoExistente) {
            produtoExistente.quantidade += produto.quantidade;
        } else {
            this.carrinho.push(produto);
        }
        
        this.salvarCarrinho();
        this.atualizarContadorCarrinho();
        return true;
    }

    removerProduto(produtoId) {
        this.carrinho = this.carrinho.filter(item => item.id !== produtoId);
        this.salvarCarrinho();
        this.atualizarContadorCarrinho();
    }

    atualizarQuantidade(produtoId, novaQuantidade) {
        const produto = this.carrinho.find(item => item.id === produtoId);
        if (produto && novaQuantidade > 0) {
            produto.quantidade = novaQuantidade;
            this.salvarCarrinho();
            this.atualizarContadorCarrinho();
            return true;
        }
        return false;
    }

    obterProdutos() {
        return this.carrinho;
    }

    calcularTotal() {
        return this.carrinho.reduce((total, item) => {
            return total + (item.preco * item.quantidade);
        }, 0);
    }

    calcularQuantidadeTotal() {
        return this.carrinho.reduce((total, item) => total + item.quantidade, 0);
    }

    limparCarrinho() {
        this.carrinho = [];
        this.salvarCarrinho();
        this.atualizarContadorCarrinho();
    }

    atualizarContadorCarrinho() {
        const contador = document.querySelector('.carrinho-contador');
        const quantidadeTotal = this.calcularQuantidadeTotal();
        
        if (contador) {
            if (quantidadeTotal > 0) {
                contador.textContent = quantidadeTotal;
                contador.style.display = 'block';
            } else {
                contador.style.display = 'none';
            }
        }
    }

    formatarPreco(preco) {
        return preco.toLocaleString('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        });
    }
}

const carrinhoManager = new CarrinhoManager();

function mostrarNotificacao(mensagem, tipo = 'sucesso') {
    const notificacaoExistente = document.querySelector('.notificacao');
    if (notificacaoExistente) {
        notificacaoExistente.remove();
    }

    const notificacao = document.createElement('div');
    notificacao.className = `notificacao notificacao-${tipo}`;
    notificacao.textContent = mensagem;
    
    //css da notificação
    notificacao.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${tipo === 'sucesso' ? '#4CAF50' : '#f44336'};
        color: white;
        padding: 15px 20px;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 1000;
        font-family: Arial, sans-serif;
        font-size: 14px;
        animation: slideIn 0.3s ease-out;
    `;

    //adicionar animação CSS
    if (!document.querySelector('#notificacao-styles')) {
        const styles = document.createElement('style');
        styles.id = 'notificacao-styles';
        styles.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(styles);
    }

    document.body.appendChild(notificacao);

    setTimeout(() => {
        notificacao.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => {
            if (notificacao.parentNode) {
                notificacao.remove();
            }
        }, 300);
    }, 3000);
}

document.addEventListener('DOMContentLoaded', function() {
    carrinhoManager.atualizarContadorCarrinho();
});
