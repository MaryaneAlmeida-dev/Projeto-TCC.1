

1. **Navegue até o diretório do projeto:**
   ```bash
   cd PROJETO_PERFUME
   ```

2. **Execute o servidor:**
   ```bash
   python run.py
   ```

3. **Acesse no navegador:**
   ```
   http://localhost:8000
   ```

### 🎯 Pronto! O sistema está funcionando!

## 📁 Estrutura do Projeto

```
PROJETO_PERFUME/
├── backend/
│   ├── server.py      # Servidor HTTP principal
│   ├── database.py    # Gerenciamento do banco SQLite
│   ├── auth.py        # Validações e autenticação
│   ├── session.py     # Sistema de sessões
│   └── utils.py       # Utilitários HTTP
├── static/js/
│   ├── auth.js        # JavaScript para login/cadastro
│   ├── header.js      # Controle dinâmico do header
│   └── profile.js     # JavaScript da página de perfil
├── *.html             # Páginas HTML
├── *.css              # Estilos CSS
├── run.py             # Script de inicialização
└── users.db           # Banco de dados SQLite (criado automaticamente)
```

## 🔗 Endpoints da API

### POST /api/register
Cadastra novo usuário
```json
{
  "nome": "João",
  "sobrenome": "Silva",
  "cpf": "12345678901",
  "telefone": "11999999999",
  "data_nascimento": "1990-01-01",
  "email": "joao@email.com",
  "senha": "minhasenha",
  "confirmar_senha": "minhasenha"
}
```

### POST /api/login
Autentica usuário
```json
{
  "login": "joao@email.com",  // ou CPF
  "senha": "minhasenha"
}
```

### POST /api/logout
Faz logout do usuário (remove sessão)

### GET /api/profile
Retorna dados do perfil do usuário logado

### GET /api/check-auth
Verifica se usuário está autenticado

## 🎨 Como Funciona

### 1. **Cadastro de Usuário**
- Usuário preenche formulário em `/cadastro.html`
- JavaScript intercepta submissão e envia via AJAX
- Backend valida todos os dados
- Se válido, cria usuário no banco SQLite
- Redireciona para página de login

### 2. **Login**
- Usuário preenche email/CPF e senha em `/loginpage.html`
- Backend autentica credenciais
- Se válido, cria sessão com cookie HTTP
- Redireciona para página principal

### 3. **Controle de Acesso**
- Header verifica status de login via `/api/check-auth`
- Se logado: ícone de perfil leva para `/profile.html`
- Se não logado: ícone de perfil leva para `/loginpage.html`

### 4. **Página de Perfil**
- Mostra informações completas do usuário
- Botão de logout
- Protegida por autenticação

## 🛡️ Segurança

- **Senhas**: Hash SHA-256
- **Sessões**: Tokens únicos com expiração
- **Validações**: Client-side e server-side
- **Cookies**: HttpOnly para segurança
- **Limpeza automática**: Sessões expiradas removidas

## 🎯 Recursos Avançados

### Formatação Automática
- **CPF**: 123.456.789-01
- **Telefone**: (11) 99999-9999

### Sistema de Mensagens
- Feedback visual para todas as ações
- Loading states durante requisições
- Mensagens de erro detalhadas




## 📱 Testando o Sistema

1. **Acesse** `http://localhost:8000`
2. **Clique** no ícone de perfil (deve ir para login)
3. **Cadastre-se** com dados válidos
4. **Faça login** com as credenciais
5. **Clique** no ícone de perfil (agora vai para perfil)
6. **Veja** suas informações na página de perfil
7. **Faça logout** e teste novamente


