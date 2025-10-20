# Contributing to Facebook Ads AI Agent

Obrigado por considerar contribuir para o Facebook Ads AI Agent! 🎉

## 📋 Como Contribuir

### 1. Setup do Ambiente

```bash
# Clone o repositório
git clone <repo-url>
cd facebook-ads-ai-agent

# Crie um virtualenv
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o .env
cp .env.example .env
# Edite .env com suas credenciais de teste
```

### 2. Desenvolvimento

```bash
# Crie uma branch para sua feature
git checkout -b feature/minha-feature

# Faça suas alterações
# ...

# Execute os testes
pytest

# Execute o linter
black src/ tests/
flake8 src/ tests/

# Execute scans de segurança
bandit -r src/ -ll
```

### 3. Commit

Siga o padrão de commits:

```bash
git commit -m "feat: adiciona nova funcionalidade X"
git commit -m "fix: corrige bug Y"
git commit -m "docs: atualiza documentação"
git commit -m "test: adiciona testes para Z"
git commit -m "refactor: melhora código W"
```

### 4. Pull Request

1. Push sua branch: `git push origin feature/minha-feature`
2. Abra um Pull Request no GitHub
3. Descreva suas mudanças claramente
4. Aguarde review

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
pytest

# Testes unitários
pytest tests/unit -v

# Testes com coverage
pytest --cov=src --cov-report=html
```

### Adicionar Novos Testes

Sempre adicione testes para novas funcionalidades:

```python
# tests/unit/test_nova_feature.py
import pytest

def test_minha_nova_feature():
    """Testa minha nova feature"""
    # Arrange
    input_data = {...}
    
    # Act
    result = minha_funcao(input_data)
    
    # Assert
    assert result == expected
```

## 📝 Code Style

### Python

Seguimos o PEP 8 com algumas adaptações:

- **Linhas:** Máximo 100 caracteres
- **Imports:** Ordenados alfabeticamente
- **Docstrings:** Google style
- **Type hints:** Sempre que possível

### Exemplo

```python
"""
Módulo de exemplo
"""
from typing import List, Dict, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ExampleRequest(BaseModel):
    """Request schema para exemplo"""
    name: str
    value: int


def process_data(data: Dict[str, Any]) -> Optional[List[str]]:
    """
    Processa dados de entrada
    
    Args:
        data: Dicionário com dados
        
    Returns:
        Lista de strings processadas ou None se erro
    """
    try:
        # Implementação
        return processed_data
    except Exception as e:
        logger.error(f"Erro ao processar: {e}")
        return None
```

## 🔒 Segurança

### Checklist de Segurança

Antes de submeter seu PR, verifique:

- [ ] Nenhuma credencial hardcoded
- [ ] Inputs validados com Pydantic
- [ ] Queries SQL parametrizadas
- [ ] Logs não expõem dados sensíveis
- [ ] Testes de segurança passando

### Security Scans

```bash
# Bandit (SAST)
bandit -r src/ -ll

# Safety (vulnerabilidades)
safety check

# Validação completa
python scripts/security_validation.py
```

## 📚 Documentação

### Docstrings

Use Google style:

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Breve descrição da função
    
    Descrição mais detalhada se necessário.
    
    Args:
        param1: Descrição do param1
        param2: Descrição do param2
        
    Returns:
        True se sucesso, False caso contrário
        
    Raises:
        ValueError: Se param2 for negativo
        
    Example:
        >>> example_function("test", 42)
        True
    """
    pass
```

### README

Atualize o README.md se:
- Adicionar novos endpoints
- Adicionar novas features
- Mudar configurações
- Adicionar novos scripts

## 🐛 Reportando Bugs

### Template de Issue

```markdown
**Descrição do Bug**
Descrição clara do que está acontecendo.

**Como Reproduzir**
1. Vá para '...'
2. Execute '...'
3. Veja erro

**Comportamento Esperado**
O que deveria acontecer.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
- OS: [Windows/Linux/Mac]
- Python: [3.12]
- Versão: [1.0.0]

**Logs**
```
Cole logs relevantes aqui
```
```

## 🎯 Roadmap

Veja [ROADMAP-MELHORIAS.md](./ROADMAP-MELHORIAS.md) para features planejadas.

Prioridades:
- 🔴 Alta: Dependency Injection, Testes
- 🟡 Média: LangChain, Circuit Breakers, Cache
- 🟢 Baixa: Features avançadas, Backup

## ❓ Dúvidas

- **Documentação:** [docs/](./docs/)
- **Issues:** GitHub Issues
- **Discussões:** GitHub Discussions

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto.

---

**Obrigado por contribuir! 🚀**
