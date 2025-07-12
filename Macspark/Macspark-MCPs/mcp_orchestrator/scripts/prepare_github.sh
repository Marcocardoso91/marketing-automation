#!/bin/bash

# Script para preparar o MCP Orchestrator para GitHub
# Este script limpa arquivos desnecessários, verifica a estrutura e inicializa o Git

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se estamos no diretório correto
check_directory() {
    if [[ ! -f "README.md" ]] || [[ ! -f "pyproject.toml" ]]; then
        error "Execute este script no diretório raiz do projeto (mcp_orchestrator/)"
        exit 1
    fi
    log "Diretório correto detectado"
}

# Limpar arquivos desnecessários
clean_files() {
    log "Limpando arquivos desnecessários..."
    
    # Remover arquivos temporários
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Remover arquivos de build
    rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/ 2>/dev/null || true
    
    # Remover logs (se existirem)
    rm -f logs/*.log 2>/dev/null || true
    
    # Remover arquivo .env se existir (não deve ser commitado)
    if [[ -f ".env" ]]; then
        warn "Arquivo .env encontrado - será removido (não deve ser commitado)"
        rm .env
    fi
    
    log "✓ Limpeza concluída"
}

# Verificar estrutura do projeto
check_structure() {
    log "Verificando estrutura do projeto..."
    
    required_files=(
        "README.md"
        "pyproject.toml"
        "requirements.txt"
        "requirements-dev.txt"
        "Dockerfile"
        "docker-compose.yml"
        "Makefile"
        ".gitignore"
        "LICENSE"
        "env.example"
        "src/mcp_orchestrator/server.py"
        "config/agents.yaml"
        "scripts/install.sh"
        "tests/unit/test_server.py"
    )
    
    missing_files=()
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        error "Arquivos obrigatórios não encontrados:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        exit 1
    fi
    
    log "✓ Estrutura do projeto verificada"
}

# Verificar qualidade do código
check_code_quality() {
    log "Verificando qualidade do código..."
    
    # Verificar se Python está disponível
    if ! command -v python3 &> /dev/null; then
        warn "Python3 não encontrado - pulando verificações de código"
        return
    fi
    
    # Verificar sintaxe Python
    log "Verificando sintaxe Python..."
    find src/ -name "*.py" -exec python3 -m py_compile {} \; || {
        error "Erros de sintaxe encontrados"
        exit 1
    }
    
    # Verificar imports
    log "Verificando imports..."
    python3 -c "import sys; sys.path.insert(0, 'src'); import mcp_orchestrator" || {
        error "Erros de import encontrados"
        exit 1
    }
    
    log "✓ Qualidade do código verificada"
}

# Inicializar Git (se não estiver inicializado)
init_git() {
    if [[ ! -d ".git" ]]; then
        log "Inicializando repositório Git..."
        git init
        
        # Configurar .gitignore se não existir
        if [[ ! -f ".gitignore" ]]; then
            error ".gitignore não encontrado"
            exit 1
        fi
        
        # Fazer commit inicial
        git add .
        git commit -m "feat: initial commit - MCP Orchestrator v3.0.0"
        
        log "✓ Repositório Git inicializado"
    else
        log "Repositório Git já existe"
    fi
}

# Criar arquivo de release notes
create_release_notes() {
    log "Criando release notes..."
    
    cat > RELEASE_NOTES.md << 'EOF'
# MCP Orchestrator v3.0.0 - Release Notes

## 🎉 Nova Versão

Esta é a primeira versão pública do MCP Orchestrator, um servidor MCP híbrido para orquestração de múltiplos agentes de IA.

## ✨ Funcionalidades Principais

### 🤖 Agentes Suportados
- **APIs**: Claude, Gemini, OpenAI, Mistral, Cohere, Perplexity
- **CLIs**: Claude CLI, Gemini CLI  
- **LLMs Locais**: Ollama, LM Studio

### 🔄 Fallback Inteligente
- Cadeias de fallback configuráveis
- Retry com backoff exponencial
- Priorização de agentes gratuitos

### 📊 Monitoramento Completo
- Métricas Prometheus
- Dashboard Grafana
- Logs estruturados
- Health checks

### 🛡️ Segurança
- Validação de entrada
- Sanitização de resposta
- Rate limiting
- Usuário não-root (Docker)

### 🚀 Deploy
- Docker Compose
- Systemd service
- Script de instalação automatizado
- Makefile com comandos úteis

## 🛠️ Instalação

### Método 1: Local
```bash
git clone <repository-url>
cd mcp_orchestrator
make install-dev
make setup-local-llms
make run
```

### Método 2: Docker
```bash
git clone <repository-url>
cd mcp_orchestrator
make docker-run
```

## 📋 Configuração

1. Copie `env.example` para `.env`
2. Configure suas chaves de API (opcional)
3. Ajuste configurações em `config/agents.yaml`

## 📚 Documentação

- [README.md](README.md) - Documentação principal
- [docs/](docs/) - Documentação detalhada
- [scripts/](scripts/) - Scripts de automação

## 🐛 Problemas Conhecidos

- Nenhum problema conhecido nesta versão

## 🔮 Próximas Versões

- Suporte a mais LLMs locais
- Interface web de administração
- Integração com mais clientes MCP
- Otimizações de performance

## 🤝 Contribuição

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.
EOF

    log "✓ Release notes criadas"
}

# Criar arquivo CONTRIBUTING.md
create_contributing() {
    log "Criando guia de contribuição..."
    
    cat > CONTRIBUTING.md << 'EOF'
# Contribuindo para o MCP Orchestrator

Obrigado por considerar contribuir para o MCP Orchestrator! 🎉

## 🚀 Como Contribuir

### 1. Fork e Clone
```bash
# Fork o repositório no GitHub
# Clone seu fork
git clone https://github.com/seu-usuario/mcp-orchestrator.git
cd mcp-orchestrator
```

### 2. Configurar Ambiente
```bash
# Instalar dependências
make install-dev

# Configurar pre-commit hooks
pre-commit install
```

### 3. Criar Branch
```bash
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b fix/correcao-bug
```

### 4. Desenvolver
- Escreva código limpo e bem documentado
- Adicione testes para novas funcionalidades
- Siga as convenções do projeto

### 5. Testar
```bash
# Executar testes
make test

# Verificar qualidade do código
make lint

# Executar todos os checks
make dev
```

### 6. Commit e Push
```bash
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feature/nova-funcionalidade
```

### 7. Pull Request
- Crie um Pull Request no GitHub
- Descreva as mudanças claramente
- Aguarde review e feedback

## 📋 Diretrizes

### Código
- Use type hints em todas as funções
- Documente funções e classes
- Siga PEP 8 (usando black)
- Mantenha cobertura de testes alta

### Commits
- Use conventional commits
- Exemplos: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`

### Pull Requests
- Título descritivo
- Descrição detalhada das mudanças
- Referência a issues relacionadas
- Screenshots para mudanças visuais

## 🧪 Testes

### Executar Testes
```bash
# Todos os testes
make test

# Apenas unitários
make test-unit

# Com cobertura
make coverage
```

### Adicionar Testes
- Testes unitários em `tests/unit/`
- Testes de integração em `tests/integration/`
- Use pytest e unittest.mock

## 🔧 Desenvolvimento

### Estrutura do Projeto
```
src/mcp_orchestrator/
├── config/          # Configurações
├── utils/           # Utilitários
├── agents/          # Implementações de agentes
└── server.py        # Servidor principal
```

### Comandos Úteis
```bash
make dev          # Modo desenvolvimento
make format       # Formatar código
make lint         # Verificar código
make test         # Executar testes
make run          # Executar servidor
```

## 🐛 Reportar Bugs

### Antes de Reportar
1. Verifique se o bug já foi reportado
2. Teste na versão mais recente
3. Tente reproduzir o problema

### Template de Bug Report
```markdown
**Descrição do Bug**
Descrição clara e concisa do bug.

**Reprodução**
1. Vá para '...'
2. Clique em '...'
3. Veja erro

**Comportamento Esperado**
O que deveria acontecer.

**Screenshots**
Se aplicável.

**Ambiente**
- OS: [ex: Ubuntu 20.04]
- Python: [ex: 3.11]
- Versão: [ex: 3.0.0]

**Logs**
Logs relevantes.
```

## 💡 Sugestões de Funcionalidades

### Antes de Sugerir
1. Verifique se já foi sugerido
2. Pesquise se é viável
3. Considere o impacto

### Template de Feature Request
```markdown
**Problema**
Descrição do problema que a funcionalidade resolveria.

**Solução Proposta**
Descrição da funcionalidade desejada.

**Alternativas Consideradas**
Outras soluções que você considerou.

**Contexto Adicional**
Qualquer contexto adicional.
```

## 📚 Recursos

- [Documentação Python](https://docs.python.org/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## 🤝 Código de Conduta

- Seja respeitoso e inclusivo
- Mantenha discussões construtivas
- Foque no código e nas ideias

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a MIT License.

---

Obrigado por contribuir! 🙏
EOF

    log "✓ Guia de contribuição criado"
}

# Criar arquivo CHANGELOG.md
create_changelog() {
    log "Criando changelog..."
    
    cat > CHANGELOG.md << 'EOF'
# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [3.0.0] - 2024-01-XX

### Adicionado
- Servidor MCP híbrido com múltiplos agentes de IA
- Suporte a APIs: Claude, Gemini, OpenAI, Mistral, Cohere, Perplexity
- Suporte a CLIs: Claude CLI, Gemini CLI
- Suporte a LLMs locais: Ollama, LM Studio
- Sistema de fallback inteligente com retry e backoff
- Configuração centralizada via YAML e variáveis de ambiente
- Logging estruturado com rotação de arquivos
- Tratamento de erros unificado com exceções customizadas
- Validação e sanitização de entrada/saída
- Rate limiting configurável
- Cache de respostas com TTL
- Métricas Prometheus para monitoramento
- Dashboard Grafana para visualização
- Health checks para todos os agentes
- Docker e Docker Compose para containerização
- Script de instalação automatizado para Linux/macOS
- Makefile com comandos úteis para desenvolvimento
- Testes unitários com cobertura
- Linting e formatação automática de código
- Type hints em todo o código
- Documentação completa com exemplos
- Sistema de backup automático
- Otimização de custos com priorização de agentes gratuitos
- Configuração de systemd para deploy em produção
- Arquitetura modular e extensível

### Alterado
- N/A (primeira versão)

### Removido
- N/A (primeira versão)

### Corrigido
- N/A (primeira versão)

### Segurança
- Validação de entrada para prevenir ataques
- Sanitização de resposta para remover caracteres perigosos
- Rate limiting para prevenir abuso
- Usuário não-root em containers Docker
- Configuração segura de variáveis de ambiente

## [Unreleased]

### Adicionado
- N/A

### Alterado
- N/A

### Removido
- N/A

### Corrigido
- N/A

---

## Tipos de Mudanças

- **Adicionado** para novas funcionalidades
- **Alterado** para mudanças em funcionalidades existentes
- **Removido** para funcionalidades removidas
- **Corrigido** para correções de bugs
- **Segurança** para correções de vulnerabilidades
EOF

    log "✓ Changelog criado"
}

# Verificar se tudo está pronto
final_check() {
    log "Verificação final..."
    
    # Verificar se não há arquivos sensíveis
    if [[ -f ".env" ]]; then
        error "Arquivo .env ainda existe - remova antes de fazer commit"
        exit 1
    fi
    
    # Verificar se .gitignore está correto
    if ! grep -q ".env" .gitignore; then
        warn ".env não está no .gitignore"
    fi
    
    # Verificar se README está atualizado
    if ! grep -q "MCP Orchestrator" README.md; then
        error "README.md não parece estar atualizado"
        exit 1
    fi
    
    log "✓ Verificação final concluída"
}

# Mostrar próximos passos
show_next_steps() {
    echo
    echo -e "${BLUE}=== Próximos Passos para GitHub ===${NC}"
    echo
    echo "1. Crie um repositório no GitHub:"
    echo "   https://github.com/new"
    echo
    echo "2. Adicione o remote origin:"
    echo "   git remote add origin https://github.com/seu-usuario/mcp-orchestrator.git"
    echo
    echo "3. Faça push para GitHub:"
    echo "   git push -u origin main"
    echo
    echo "4. Configure GitHub Actions (opcional):"
    echo "   - Crie .github/workflows/ci.yml"
    echo "   - Configure secrets para testes"
    echo
    echo "5. Crie uma release:"
    echo "   - Vá para Releases no GitHub"
    echo "   - Crie uma nova release v3.0.0"
    echo "   - Use o conteúdo de RELEASE_NOTES.md"
    echo
    echo "6. Configure GitHub Pages (opcional):"
    echo "   - Vá para Settings > Pages"
    echo "   - Configure para branch gh-pages"
    echo
    echo -e "${GREEN}✓ Projeto pronto para GitHub!${NC}"
}

# Função principal
main() {
    echo -e "${BLUE}=== Preparando MCP Orchestrator para GitHub ===${NC}"
    echo
    
    check_directory
    clean_files
    check_structure
    check_code_quality
    create_release_notes
    create_contributing
    create_changelog
    init_git
    final_check
    show_next_steps
}

# Executar função principal
main "$@" 