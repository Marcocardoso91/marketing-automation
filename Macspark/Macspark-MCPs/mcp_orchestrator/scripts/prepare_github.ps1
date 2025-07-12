# Script para preparar o MCP Orchestrator para GitHub (Windows)
# Este script limpa arquivos desnecessários, verifica a estrutura e inicializa o Git

# Funções de log colorido
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Verificar se estamos no diretório correto
function Test-Directory {
    if (-not (Test-Path "README.md") -or -not (Test-Path "pyproject.toml")) {
        Write-Error "Execute este script no diretório raiz do projeto (mcp_orchestrator/)"
        exit 1
    }
    Write-Info "Diretório correto detectado"
}

# Limpar arquivos desnecessários
function Clear-Files {
    Write-Info "Limpando arquivos desnecessários..."
    
    # Remover arquivos Python compilados
    Get-ChildItem -Recurse -Include "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Recurse -Include "__pycache__" -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Recurse -Include "*.egg-info" -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    
    # Remover arquivos de build
    $buildDirs = @("build", "dist", ".pytest_cache", ".coverage", "htmlcov")
    foreach ($dir in $buildDirs) {
        if (Test-Path $dir) {
            Remove-Item -Recurse -Force $dir
        }
    }
    
    # Remover logs
    if (Test-Path "logs") {
        Get-ChildItem "logs" -Include "*.log" | Remove-Item -Force -ErrorAction SilentlyContinue
    }
    
    # Remover arquivo .env se existir
    if (Test-Path ".env") {
        Write-Warn "Arquivo .env encontrado - será removido (não deve ser commitado)"
        Remove-Item ".env" -Force
    }
    
    Write-Info "✓ Limpeza concluída"
}

# Verificar estrutura do projeto
function Test-Structure {
    Write-Info "Verificando estrutura do projeto..."
    
    $requiredFiles = @(
        "README.md",
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "Dockerfile",
        "docker-compose.yml",
        "Makefile",
        ".gitignore",
        "LICENSE",
        "env.example",
        "src/mcp_orchestrator/server.py",
        "config/agents.yaml",
        "scripts/install.sh",
        "tests/unit/test_server.py"
    )
    
    $missingFiles = @()
    
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            $missingFiles += $file
        }
    }
    
    if ($missingFiles.Count -gt 0) {
        Write-Error "Arquivos obrigatórios não encontrados:"
        foreach ($file in $missingFiles) {
            Write-Host "  - $file" -ForegroundColor Red
        }
        exit 1
    }
    
    Write-Info "✓ Estrutura do projeto verificada"
}

# Inicializar Git
function Initialize-Git {
    if (-not (Test-Path ".git")) {
        Write-Info "Inicializando repositório Git..."
        git init
        
        # Verificar se .gitignore existe
        if (-not (Test-Path ".gitignore")) {
            Write-Error ".gitignore não encontrado"
            exit 1
        }
        
        # Fazer commit inicial
        git add .
        git commit -m "feat: initial commit - MCP Orchestrator v3.0.0"
        
        Write-Info "✓ Repositório Git inicializado"
    }
    else {
        Write-Info "Repositório Git já existe"
    }
}

# Criar arquivos de documentação
function Create-Documentation {
    Write-Info "Criando arquivos de documentação..."
    
    # RELEASE_NOTES.md
    $releaseNotes = @"
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
"@
    
    Set-Content -Path "RELEASE_NOTES.md" -Value $releaseNotes
    
    Write-Info "✓ Documentação criada"
}

# Verificar se tudo está pronto
function Test-FinalCheck {
    Write-Info "Verificação final..."
    
    # Verificar se não há arquivos sensíveis
    if (Test-Path ".env") {
        Write-Error "Arquivo .env ainda existe - remova antes de fazer commit"
        exit 1
    }
    
    # Verificar se README está atualizado
    $readmeContent = Get-Content "README.md" -Raw
    if ($readmeContent -notmatch "MCP Orchestrator") {
        Write-Error "README.md não parece estar atualizado"
        exit 1
    }
    
    Write-Info "✓ Verificação final concluída"
}

# Mostrar próximos passos
function Show-NextSteps {
    Write-Host ""
    Write-Host "=== Próximos Passos para GitHub ===" -ForegroundColor Blue
    Write-Host ""
    Write-Host "1. Crie um repositório no GitHub:"
    Write-Host "   https://github.com/new"
    Write-Host ""
    Write-Host "2. Adicione o remote origin:"
    Write-Host "   git remote add origin https://github.com/seu-usuario/mcp-orchestrator.git"
    Write-Host ""
    Write-Host "3. Faça push para GitHub:"
    Write-Host "   git push -u origin main"
    Write-Host ""
    Write-Host "4. Configure GitHub Actions (opcional):"
    Write-Host "   - Crie .github/workflows/ci.yml"
    Write-Host "   - Configure secrets para testes"
    Write-Host ""
    Write-Host "5. Crie uma release:"
    Write-Host "   - Vá para Releases no GitHub"
    Write-Host "   - Crie uma nova release v3.0.0"
    Write-Host "   - Use o conteúdo de RELEASE_NOTES.md"
    Write-Host ""
    Write-Host "✓ Projeto pronto para GitHub!" -ForegroundColor Green
}

# Função principal
function Main {
    Write-Host "=== Preparando MCP Orchestrator para GitHub ===" -ForegroundColor Blue
    Write-Host ""
    
    Test-Directory
    Clear-Files
    Test-Structure
    Create-Documentation
    Initialize-Git
    Test-FinalCheck
    Show-NextSteps
}

# Executar função principal
Main 