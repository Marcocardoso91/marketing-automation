#!/bin/bash

# Script para configurar o MCP Orchestrator no GitHub
# Este script automatiza o processo de criação do repositório e push inicial

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

# Verificar dependências
check_dependencies() {
    log "Verificando dependências..."
    
    if ! command -v git &> /dev/null; then
        error "Git não está instalado"
        exit 1
    fi
    
    if ! command -v gh &> /dev/null; then
        warn "GitHub CLI não está instalado"
        log "Instale em: https://cli.github.com/"
        log "Ou configure manualmente o repositório"
    fi
    
    log "✓ Dependências verificadas"
}

# Verificar se estamos no diretório correto
check_directory() {
    if [[ ! -f "README.md" ]] || [[ ! -f "pyproject.toml" ]]; then
        error "Execute este script no diretório raiz do projeto (mcp_orchestrator/)"
        exit 1
    fi
    log "Diretório correto detectado"
}

# Verificar status do Git
check_git_status() {
    if [[ ! -d ".git" ]]; then
        error "Repositório Git não inicializado"
        log "Execute primeiro: ./scripts/prepare_github.sh"
        exit 1
    fi
    
    # Verificar se há mudanças não commitadas
    if [[ -n "$(git status --porcelain)" ]]; then
        warn "Há mudanças não commitadas"
        git status --short
        read -p "Deseja fazer commit das mudanças? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git add .
            git commit -m "feat: prepare for GitHub upload"
        else
            error "Faça commit das mudanças antes de continuar"
            exit 1
        fi
    fi
    
    log "✓ Status do Git verificado"
}

# Criar repositório no GitHub (se GitHub CLI estiver disponível)
create_github_repo() {
    if command -v gh &> /dev/null; then
        log "Criando repositório no GitHub..."
        
        # Verificar se já está logado
        if ! gh auth status &> /dev/null; then
            log "Faça login no GitHub CLI primeiro:"
            log "gh auth login"
            exit 1
        fi
        
        # Ler nome do repositório
        read -p "Nome do repositório (mcp-orchestrator): " repo_name
        repo_name=${repo_name:-mcp-orchestrator}
        
        # Ler descrição
        read -p "Descrição do repositório: " repo_description
        repo_description=${repo_description:-"Hybrid AI Orchestrator MCP Server with local LLMs, APIs, and CLI tools"}
        
        # Criar repositório
        gh repo create "$repo_name" \
            --description "$repo_description" \
            --public \
            --source=. \
            --remote=origin \
            --push
        
        log "✓ Repositório criado: https://github.com/$(gh api user --jq .login)/$repo_name"
    else
        warn "GitHub CLI não está disponível"
        log "Crie o repositório manualmente em: https://github.com/new"
        log "Depois execute os comandos Git mostrados abaixo"
    fi
}

# Configurar remote manualmente
setup_remote_manual() {
    if ! command -v gh &> /dev/null; then
        log "Configurando remote manualmente..."
        
        read -p "URL do repositório GitHub: " repo_url
        
        if [[ -z "$repo_url" ]]; then
            error "URL do repositório é obrigatória"
            exit 1
        fi
        
        # Adicionar remote
        git remote add origin "$repo_url"
        
        # Fazer push
        git push -u origin main
        
        log "✓ Remote configurado e push realizado"
    fi
}

# Configurar branch protection (se GitHub CLI estiver disponível)
setup_branch_protection() {
    if command -v gh &> /dev/null; then
        log "Configurando proteção da branch main..."
        
        # Obter nome do repositório
        repo_name=$(git remote get-url origin | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1\/\2/')
        
        # Configurar branch protection
        gh api repos/$repo_name/branches/main/protection \
            --method PUT \
            --field required_status_checks='{"strict":true,"contexts":["test"]}' \
            --field enforce_admins=true \
            --field required_pull_request_reviews='{"required_approving_review_count":1}' \
            --field restrictions=null || warn "Não foi possível configurar proteção da branch"
        
        log "✓ Proteção da branch configurada"
    fi
}

# Configurar secrets para GitHub Actions
setup_secrets() {
    if command -v gh &> /dev/null; then
        log "Configurando secrets para GitHub Actions..."
        
        read -p "Deseja configurar secrets para Docker Hub? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -p "Docker Hub username: " docker_username
            read -s -p "Docker Hub password/token: " docker_password
            echo
            
            if [[ -n "$docker_username" && -n "$docker_password" ]]; then
                gh secret set DOCKER_USERNAME --body "$docker_username"
                gh secret set DOCKER_PASSWORD --body "$docker_password"
                log "✓ Secrets do Docker Hub configurados"
            fi
        fi
        
        read -p "Deseja configurar secrets para PyPI? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            read -s -p "PyPI API token: " pypi_token
            echo
            
            if [[ -n "$pypi_token" ]]; then
                gh secret set PYPI_API_TOKEN --body "$pypi_token"
                log "✓ Secret do PyPI configurado"
            fi
        fi
    else
        warn "GitHub CLI não está disponível"
        log "Configure secrets manualmente em: Settings > Secrets and variables > Actions"
    fi
}

# Configurar GitHub Pages
setup_github_pages() {
    if command -v gh &> /dev/null; then
        log "Configurando GitHub Pages..."
        
        read -p "Deseja configurar GitHub Pages? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Obter nome do repositório
            repo_name=$(git remote get-url origin | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1\/\2/')
            
            # Configurar GitHub Pages
            gh api repos/$repo_name/pages \
                --method POST \
                --field source='{"branch":"gh-pages","path":"/"}' || warn "Não foi possível configurar GitHub Pages"
            
            log "✓ GitHub Pages configurado"
        fi
    else
        warn "GitHub CLI não está disponível"
        log "Configure GitHub Pages manualmente em: Settings > Pages"
    fi
}

# Criar primeira release
create_first_release() {
    if command -v gh &> /dev/null; then
        log "Criando primeira release..."
        
        read -p "Deseja criar uma release v3.0.0? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            # Criar tag
            git tag -a v3.0.0 -m "Release v3.0.0"
            git push origin v3.0.0
            
            # Criar release
            gh release create v3.0.0 \
                --title "MCP Orchestrator v3.0.0" \
                --notes-file RELEASE_NOTES.md \
                --latest
            
            log "✓ Release v3.0.0 criada"
        fi
    else
        warn "GitHub CLI não está disponível"
        log "Crie a release manualmente em: Releases"
    fi
}

# Configurar labels e templates
setup_templates() {
    if command -v gh &> /dev/null; then
        log "Configurando templates e labels..."
        
        # Criar diretórios para templates
        mkdir -p .github/ISSUE_TEMPLATE
        mkdir -p .github/PULL_REQUEST_TEMPLATE
        
        # Template para issues
        cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: Bug report
about: Create a report to help us improve
title: ''
labels: 'bug'
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g. Ubuntu 20.04]
 - Python Version: [e.g. 3.11]
 - MCP Orchestrator Version: [e.g. 3.0.0]

**Additional context**
Add any other context about the problem here.
EOF

        # Template para feature requests
        cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: Feature request
about: Suggest an idea for this project
title: ''
labels: 'enhancement'
assignees: ''

---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.
EOF

        # Template para pull requests
        cat > .github/PULL_REQUEST_TEMPLATE.md << 'EOF'
## Description
Please include a summary of the change and which issue is fixed. Please also include relevant motivation and context.

Fixes # (issue)

## Type of change
Please delete options that are not relevant.

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] This change requires a documentation update

## How Has This Been Tested?
Please describe the tests that you ran to verify your changes. Provide instructions so we can reproduce. Please also list any relevant details for your test configuration.

- [ ] Test A
- [ ] Test B

## Checklist:
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published in downstream modules
EOF

        # Adicionar templates ao Git
        git add .github/
        git commit -m "feat: add issue and PR templates"
        git push
        
        log "✓ Templates configurados"
    else
        warn "GitHub CLI não está disponível"
        log "Configure templates manualmente"
    fi
}

# Mostrar próximos passos
show_next_steps() {
    echo
    echo -e "${BLUE}=== Próximos Passos ===${NC}"
    echo
    echo "1. Verifique o repositório no GitHub:"
    echo "   https://github.com/seu-usuario/mcp-orchestrator"
    echo
    echo "2. Configure GitHub Actions (se necessário):"
    echo "   - Vá para Actions no GitHub"
    echo "   - Configure secrets se necessário"
    echo
    echo "3. Configure proteção da branch main:"
    echo "   - Settings > Branches > Add rule"
    echo "   - Require pull request reviews"
    echo "   - Require status checks to pass"
    echo
    echo "4. Configure GitHub Pages (opcional):"
    echo "   - Settings > Pages"
    echo "   - Source: Deploy from a branch"
    echo "   - Branch: gh-pages"
    echo
    echo "5. Adicione badges ao README:"
    echo "   - Build status"
    echo "   - Test coverage"
    echo "   - License"
    echo
    echo "6. Configure dependabot (opcional):"
    echo "   - Settings > Security > Dependabot"
    echo "   - Enable for Python"
    echo
    echo -e "${GREEN}✓ Repositório configurado com sucesso!${NC}"
}

# Função principal
main() {
    echo -e "${BLUE}=== Configurando MCP Orchestrator no GitHub ===${NC}"
    echo
    
    check_dependencies
    check_directory
    check_git_status
    
    if command -v gh &> /dev/null; then
        create_github_repo
        setup_branch_protection
        setup_secrets
        setup_github_pages
        create_first_release
        setup_templates
    else
        setup_remote_manual
    fi
    
    show_next_steps
}

# Executar função principal
main "$@" 