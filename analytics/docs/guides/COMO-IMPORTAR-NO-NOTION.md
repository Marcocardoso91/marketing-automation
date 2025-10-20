# 📥 Como Importar Páginas no Notion

## Páginas Criadas Como Arquivos

Como o MCP do Notion foi desconectado, criei 2 páginas adicionais como arquivos markdown que você pode importar manualmente:

---

## 📄 Arquivos para Importar

### 1. Dashboard Campanhas Ativas
**Arquivo:** `notion-pages/dashboard-campanhas-ativas.md`
**Onde criar:** Dentro da página principal do Projeto Sabrina

### 2. Template Métricas Manuais
**Arquivo:** `notion-pages/template-metricas-manuais.md`
**Onde criar:** Dentro da página principal do Projeto Sabrina

---

## 🔧 Método 1: Copiar e Colar (Mais Rápido)

### Passo a Passo:

1. **Abrir arquivo local:**
   - Usar editor de texto
   - Abrir `notion-pages/dashboard-campanhas-ativas.md`

2. **Copiar conteúdo:**
   - Selecionar TUDO (Ctrl+A)
   - Copiar (Ctrl+C)

3. **No Notion:**
   - Abrir [Dashboard Principal](https://www.notion.so/290a4e7a770481a1bd19e595253012a6)
   - Criar nova página filho (+ New Page)
   - Colar (Ctrl+V)
   - Notion converte markdown automaticamente!

4. **Ajustar:**
   - Adicionar ícone 📊
   - Renomear se necessário
   - Formatar se quiser

5. **Repetir** para `template-metricas-manuais.md`

---

## 🔧 Método 2: Importação Markdown (Mais Preciso)

### Passo a Passo:

1. **No Notion:**
   - Abrir [Dashboard Principal](https://www.notion.so/290a4e7a770481a1bd19e595253012a6)
   - Clicar em **"..."** (menu)
   - Selecionar **"Import"**

2. **Escolher arquivo:**
   - Clicar em **"Markdown"**
   - Selecionar `notion-pages/dashboard-campanhas-ativas.md`
   - Importar

3. **Resultado:**
   - Notion cria página automaticamente
   - Mantém formatação
   - Links preservados

4. **Repetir** para segundo arquivo

---

## ✅ Após Importar

### Adicionar Links no Dashboard Principal:

1. Abrir Dashboard Principal
2. Editar página
3. Na seção "🚀 Acesso Rápido", adicionar:

```markdown
### 📊 Dashboard - Campanhas Ativas HOJE
Visão em tempo real com alertas e ações recomendadas.

### 📝 Template - Métricas Manuais
Backup manual caso automação falhe (3-5 min/dia).
```

4. Linkar para as páginas importadas

---

## 🎯 Resultado Final

Você terá:
- ✅ Dashboard Principal atualizado
- ✅ 2 páginas novas importadas
- ✅ Links funcionando
- ✅ Estrutura completa

---

## 📊 Melhorias nos Databases

**NOTA:** Como não consigo modificar databases existentes via MCP, as melhorias sugeridas (campos adicionais) precisam ser feitas manualmente no Notion:

### No Database "Calendário de Conteúdo":

**Adicionar colunas:**
1. Abrir database
2. Clicar em **"+ "** (adicionar propriedade)
3. Adicionar:
   - `Deadline Criação` (Date)
   - `Status Produção` (Select): Ideia, Roteiro, Gravando, Editando, Pronto, Publicado
   - `Prioridade` (Select): 🔴 Alta, 🟡 Média, 🟢 Baixa
   - `Responsável` (Text)
   - `Link Post Publicado` (URL)

### No Database "Campanhas de Ads":

**Adicionar colunas:**
1. Abrir database
2. Adicionar:
   - `Status Campanha` (Select): 🟢 Ativa, ⏸️ Pausada, ✅ Concluída, 📝 Rascunho
   - `Data Última Atualização` (Date)
   - `Alertas` (Select): 🟢 Normal, 🟡 Atenção, 🔴 Crítico
   - `Frequência Atual` (Number)
   - `Link Ads Manager` (URL)

**Tempo:** ~5 minutos por database

---

## 🎁 Bônus: Como Organizar

### Estrutura Recomendada no Notion:

```
💄 PROJETO SABRINA (Principal)
├── 📍 Resumo Executivo ← Visão rápida
├── 📊 Linha de Base ← Preencher primeiro!
├── 🔄 Antes x Depois ← Comparação futura
│
├── 🎯 PLANEJAMENTO
│   ├── Metas e Objetivos
│   ├── Estratégia Completa
│   ├── Cronograma Diário
│   └── Plano Original
│
├── 🛠️ EXECUTAR
│   ├── Guia Passo a Passo
│   ├── Templates Posts
│   ├── Tutoriais Vídeo
│   └── Dashboard Campanhas ← IMPORTAR
│
└── 📊 DATABASES
    ├── Calendário Conteúdo
    ├── Métricas & KPIs
    ├── Campanhas Ads
    └── Banco Ideias
```

---

## ✅ Checklist Importação

- [ ] Copiar `dashboard-campanhas-ativas.md`
- [ ] Importar no Notion
- [ ] Copiar `template-metricas-manuais.md`
- [ ] Importar no Notion
- [ ] Adicionar campos nos databases
- [ ] Linkar no Dashboard Principal
- [ ] Testar navegação
- [ ] Está tudo funcionando!

---

**Tempo total:** 10-15 minutos

**💡 Dica:** Use Método 1 (copiar/colar) - é mais rápido!

---

**Criado:** 18 de Outubro, 2025

