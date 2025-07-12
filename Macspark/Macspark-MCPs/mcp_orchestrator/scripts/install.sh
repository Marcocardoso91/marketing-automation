#!/bin/bash

# MCP Orchestrator - Script de Instalação
# Este script instala e configura o MCP Orchestrator em sistemas Linux/macOS

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para log colorido
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se é root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "Este script não deve ser executado como root"
        exit 1
    fi
}

# Verificar sistema operacional
check_os() {
    log "Verificando sistema operacional..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        log "Sistema Linux detectado"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        log "Sistema macOS detectado"
    else
        error "Sistema operacional não suportado: $OSTYPE"
        exit 1
    fi
}

# Verificar dependências do sistema
check_dependencies() {
    log "Verificando dependências do sistema..."
    
    # Python
    if ! command -v python3 &> /dev/null; then
        error "Python 3 não está instalado"
        log "Instalando Python 3..."
        if [[ "$OS" == "linux" ]]; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv
        elif [[ "$OS" == "macos" ]]; then
            if ! command -v brew &> /dev/null; then
                error "Homebrew não está instalado. Instale em: https://brew.sh/"
                exit 1
            fi
            brew install python3
        fi
    else
        log "✓ Python 3 encontrado"
    fi
    
    # Git
    if ! command -v git &> /dev/null; then
        error "Git não está instalado"
        log "Instalando Git..."
        if [[ "$OS" == "linux" ]]; then
            sudo apt-get install -y git
        elif [[ "$OS" == "macos" ]]; then
            brew install git
        fi
    else
        log "✓ Git encontrado"
    fi
    
    # Docker (opcional)
    if ! command -v docker &> /dev/null; then
        warn "Docker não está instalado (opcional para LLMs locais)"
        log "Para instalar Docker, visite: https://docs.docker.com/get-docker/"
    else
        log "✓ Docker encontrado"
    fi
    
    # Ollama (opcional)
    if ! command -v ollama &> /dev/null; then
        warn "Ollama não está instalado (opcional para LLMs locais)"
        log "Para instalar Ollama, visite: https://ollama.ai/"
    else
        log "✓ Ollama encontrado"
    fi
}

# Criar ambiente virtual
setup_venv() {
    log "Configurando ambiente virtual Python..."
    
    if [[ -d "venv" ]]; then
        warn "Ambiente virtual já existe. Removendo..."
        rm -rf venv
    fi
    
    python3 -m venv venv
    source venv/bin/activate
    
    log "✓ Ambiente virtual criado"
}

# Instalar dependências Python
install_python_deps() {
    log "Instalando dependências Python..."
    
    # Atualizar pip
    pip install --upgrade pip
    
    # Instalar dependências principais
    pip install -r requirements.txt
    
    # Instalar dependências de desenvolvimento (opcional)
    if [[ -f "requirements-dev.txt" ]]; then
        log "Instalando dependências de desenvolvimento..."
        pip install -r requirements-dev.txt
    fi
    
    # Instalar em modo desenvolvimento
    pip install -e .
    
    log "✓ Dependências Python instaladas"
}

# Configurar arquivo .env
setup_env() {
    log "Configurando arquivo .env..."
    
    if [[ ! -f ".env.example" ]]; then
        error "Arquivo .env.example não encontrado"
        exit 1
    fi
    
    if [[ ! -f ".env" ]]; then
        cp .env.example .env
        log "✓ Arquivo .env criado a partir de .env.example"
        warn "Edite o arquivo .env com suas chaves de API"
    else
        warn "Arquivo .env já existe"
    fi
}

# Configurar diretórios
setup_directories() {
    log "Criando diretórios necessários..."
    
    mkdir -p logs
    mkdir -p data/cache
    mkdir -p data/examples
    mkdir -p data/models
    mkdir -p config
    
    # Criar arquivos .gitkeep para manter diretórios vazios no git
    touch data/cache/.gitkeep
    touch data/examples/.gitkeep
    touch data/models/.gitkeep
    
    log "✓ Diretórios criados"
}

# Configurar LLMs locais (opcional)
setup_local_llms() {
    log "Configurando LLMs locais..."
    
    # Ollama
    if command -v ollama &> /dev/null; then
        log "Configurando Ollama..."
        
        # Verificar se Ollama está rodando
        if ! curl -f http://localhost:11434/api/tags &> /dev/null; then
            log "Iniciando Ollama..."
            ollama serve &
            sleep 5
        fi
        
        # Baixar modelos populares
        log "Baixando modelos Ollama..."
        ollama pull llama3.1:8b || warn "Falha ao baixar llama3.1:8b"
        ollama pull codellama:7b || warn "Falha ao baixar codellama:7b"
        ollama pull mistral:7b || warn "Falha ao baixar mistral:7b"
        
        log "✓ Ollama configurado"
    else
        warn "Ollama não está instalado. Pule esta etapa ou instale em: https://ollama.ai/"
    fi
    
    # LM Studio (se Docker estiver disponível)
    if command -v docker &> /dev/null; then
        log "Configurando LM Studio via Docker..."
        
        # Verificar se container já está rodando
        if ! docker ps | grep -q lm-studio; then
            log "Iniciando LM Studio..."
            docker run -d --name lm-studio -p 1234:1234 lmstudio/lmstudio:latest || warn "Falha ao iniciar LM Studio"
        fi
        
        log "✓ LM Studio configurado"
    else
        warn "Docker não está instalado. LM Studio não será configurado"
    fi
}

# Configurar CLIs (opcional)
setup_clis() {
    log "Configurando CLIs..."
    
    # Claude CLI
    if ! command -v claude &> /dev/null; then
        warn "Claude CLI não está instalado"
        log "Para instalar: npm install -g @anthropic-ai/claude"
    else
        log "✓ Claude CLI encontrado"
    fi
    
    # Gemini CLI (se disponível)
    if ! command -v gemini &> /dev/null; then
        warn "Gemini CLI não está instalado"
        log "Para instalar: pip install google-generativeai[cli]"
    else
        log "✓ Gemini CLI encontrado"
    fi
}

# Executar testes
run_tests() {
    log "Executando testes..."
    
    if command -v pytest &> /dev/null; then
        pytest tests/unit/ -v || warn "Alguns testes falharam"
        log "✓ Testes executados"
    else
        warn "pytest não está disponível. Testes não executados"
    fi
}

# Configurar systemd service (Linux)
setup_systemd() {
    if [[ "$OS" == "linux" ]]; then
        log "Configurando serviço systemd..."
        
        SERVICE_FILE="/etc/systemd/system/mcp-orchestrator.service"
        
        if [[ ! -f "$SERVICE_FILE" ]]; then
            sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=MCP Orchestrator
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python -m mcp_orchestrator.server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
            log "✓ Serviço systemd criado"
            log "Para ativar: sudo systemctl enable mcp-orchestrator"
            log "Para iniciar: sudo systemctl start mcp-orchestrator"
        else
            warn "Serviço systemd já existe"
        fi
    fi
}

# Mostrar informações finais
show_info() {
    log "=== Instalação Concluída ==="
    echo
    log "Para iniciar o servidor:"
    echo "  source venv/bin/activate"
    echo "  python -m mcp_orchestrator.server"
    echo
    log "Ou use o Makefile:"
    echo "  make run"
    echo
    log "Para desenvolvimento:"
    echo "  make dev"
    echo
    log "Para Docker:"
    echo "  make docker-run"
    echo
    log "Documentação:"
    echo "  https://github.com/seu-usuario/mcp-orchestrator"
    echo
    warn "Lembre-se de editar o arquivo .env com suas chaves de API!"
    echo
}

# Função principal
main() {
    echo -e "${BLUE}=== MCP Orchestrator - Instalação ===${NC}"
    echo
    
    check_root
    check_os
    check_dependencies
    setup_venv
    install_python_deps
    setup_env
    setup_directories
    setup_local_llms
    setup_clis
    run_tests
    setup_systemd
    show_info
    
    echo -e "${GREEN}✓ Instalação concluída com sucesso!${NC}"
}

# Executar função principal
main "$@" 