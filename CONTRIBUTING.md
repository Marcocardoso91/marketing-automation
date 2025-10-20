# Guia de Contribuição - Marketing Automation Platform

## Como Contribuir

### 1. Setup do Ambiente

```bash
cd C:\Users\marco\Macspark\marketing-automation

# Instalar shared package
cd shared
pip install -e .[dev]
cd ..

# Instalar dependências da API
cd api
pip install -r requirements.txt
cd ..

# Instalar dependências do Analytics
cd analytics/scripts
pip install -r requirements.txt
cd ../..
```

### 2. Fazer Mudanças

#### No Shared Package
```bash
cd shared/marketing_shared/

# Editar schemas ou utils
# Testar: python -c "from marketing_shared.* import *"
```

#### No Agent API
```bash
cd api/src/

# Editar código
# Testar: pytest tests/ -v
```

#### No Analytics
```bash
cd analytics/scripts/

# Editar scripts
# Testar: pytest ../tests/ -v
```

### 3. Testes

```bash
# Testes de integração
pytest tests/integration/ -v

# Validação
python scripts/validate-integration.py
```

### 4. Formatar Código

```bash
# Black formatter
black shared/marketing_shared/ api/src/ analytics/scripts/

# Verificar
black --check .
```

### 5. Commitar

```bash
git add .
git commit -m "feat: descrição da mudança"
```

## Convenções

### Commits
- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Mudanças na documentação
- `refactor:` - Refatoração de código
- `test:` - Adicionar testes

### Código
- Python 3.12+
- Type hints sempre que possível
- Docstrings em funções públicas
- Black para formatação

---

**Versão:** 1.0.0

