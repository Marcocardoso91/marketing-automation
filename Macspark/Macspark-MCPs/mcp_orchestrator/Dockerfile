# Multi-stage build para otimizar tamanho da imagem
FROM python:3.11-slim as builder

# Instalar dependências do sistema necessárias para build
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Criar ambiente virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar arquivos de dependências
COPY requirements.txt .
COPY pyproject.toml .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage final
FROM python:3.11-slim

# Criar usuário não-root para segurança
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

# Instalar dependências do sistema necessárias para runtime
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copiar ambiente virtual do builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Definir diretório de trabalho
WORKDIR /app

# Copiar código fonte
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/

# Criar diretórios necessários
RUN mkdir -p logs data/cache data/examples data/models && \
    chown -R mcpuser:mcpuser /app

# Mudar para usuário não-root
USER mcpuser

# Expor porta (se necessário para HTTP)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Comando padrão
CMD ["python", "-m", "mcp_orchestrator.server"] 