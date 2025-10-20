# 🧪 PLANO DE TESTES COMPLETO
## Dashboard Sabrina Costa

**Data:** 20 de Outubro de 2025  
**Servidor Rodando:** http://localhost:8000 ✅  
**Status:** Pronto para testes

---

## 📋 SUMÁRIO

1. [Testes de Frontend](#testes-de-frontend)
2. [Testes de Backend](#testes-de-backend)
3. [Testes de Integração](#testes-de-integração)
4. [Testes de n8n](#testes-de-n8n)
5. [Testes End-to-End](#testes-end-to-end)

---

## 🎨 TESTES DE FRONTEND

### ✅ Teste 1: Página de Login
**URL:** http://localhost:8000/index.html

**Casos de Teste:**

| # | Teste | Passos | Resultado Esperado |
|---|-------|--------|-------------------|
| 1.1 | Login bem-sucedido | 1. Email: gerente@macspark.dev<br>2. Senha: Sabrina2025!<br>3. Clicar "Entrar" | ✅ Mensagem de sucesso<br>✅ Redirecionamento para dashboard |
| 1.2 | Login com credenciais inválidas | 1. Email: errado@test.com<br>2. Senha: errada<br>3. Clicar "Entrar" | ✅ Mensagem de erro<br>❌ Não redireciona |
| 1.3 | Validação de formulário | 1. Deixar campos vazios<br>2. Tentar submit | ✅ Validação HTML5 impede submit |
| 1.4 | Mostrar/esconder senha | 1. Digitar senha<br>2. Clicar ícone olho | ✅ Senha fica visível/oculta |
| 1.5 | Lembrar-me (checkbox) | 1. Marcar "Lembrar-me"<br>2. Fazer login | ✅ Checkbox funciona |
| 1.6 | Responsividade | 1. Redimensionar janela<br>2. Testar em mobile (DevTools) | ✅ Layout adapta corretamente |

---

### ✅ Teste 2: Dashboard Principal
**URL:** http://localhost:8000/dashboard.html

**Casos de Teste:**

| # | Teste | Passos | Resultado Esperado |
|---|-------|--------|-------------------|
| 2.1 | Carregar métricas | 1. Acessar dashboard | ✅ 4 KPIs carregam<br>✅ Gráficos aparecem |
| 2.2 | Filtro de período | 1. Alterar dropdown (7d→30d→90d) | ✅ Gráficos atualizam<br>✅ Dados mudam |
| 2.3 | Botão refresh | 1. Clicar botão refresh | ✅ Ícone gira<br>✅ Dados recarregam |
| 2.4 | Gráfico CTR interativo | 1. Hover sobre pontos do gráfico | ✅ Tooltip mostra valores |
| 2.5 | Gráfico Seguidores | 1. Hover sobre barras | ✅ Tooltip mostra valores |
| 2.6 | Alertas recentes | 1. Verificar seção de alertas | ✅ Lista de alertas ou mensagem vazia |
| 2.7 | Navegação | 1. Clicar em cada link do menu | ✅ Navega para página correta |
| 2.8 | Menu usuário | 1. Clicar no avatar<br>2. Ver dropdown | ✅ Menu abre/fecha<br>✅ Links funcionam |
| 2.9 | Logout | 1. Menu usuário → Sair | ✅ Confirmação<br>✅ Redireciona para login |
| 2.10 | Auto-refresh | 1. Aguardar 5 minutos | ✅ Dados recarregam automaticamente |

---

### ✅ Teste 3: Cronograma
**URL:** http://localhost:8000/cronograma.html

| # | Teste | Passos | Resultado Esperado |
|---|-------|--------|-------------------|
| 3.1 | Carregar cronograma | 1. Acessar página | ✅ Timeline das 4 semanas carrega |
| 3.2 | Filtro por semana | 1. Selecionar semana | ✅ Mostra apenas posts da semana |
| 3.3 | Filtro por formato | 1. Filtrar "Reel" | ✅ Mostra apenas Reels |
| 3.4 | Busca por palavra | 1. Buscar "transformação" | ✅ Filtra posts com palavra |
| 3.5 | Marcar como postado | 1. Clicar checkbox/botão | ✅ Status muda para "postado" |
| 3.6 | Cards visuais | 1. Ver diferenciação de formato | ✅ Cores/ícones diferentes |

---

### ✅ Teste 4: Ganchos Virais
**URL:** http://localhost:8000/ganchos.html

| # | Teste | Passos | Resultado Esperado |
|---|-------|--------|-------------------|
| 4.1 | Listar 50 ganchos | 1. Acessar página | ✅ 50 cards de ganchos aparecem |
| 4.2 | Filtrar por categoria | 1. Clicar "Curiosidade" | ✅ Mostra apenas 5 ganchos da categoria |
| 4.3 | Busca textual | 1. Buscar "NINGUÉM" | ✅ Filtra ganchos com palavra |
| 4.4 | Copiar gancho | 1. Clicar "Copiar" | ✅ Texto copiado para clipboard<br>✅ Feedback visual |
| 4.5 | Limpar filtros | 1. Aplicar filtro<br>2. Clicar "Limpar" | ✅ Volta a mostrar todos |
| 4.6 | Contador de uso | 1. Copiar gancho | ✅ Contador incrementa (se backend conectado) |

---

### ✅ Teste 5: Checklist
**URL:** http://localhost:8000/checklist.html

| # | Teste | Passos | Resultado Esperado |
|---|-------|--------|-------------------|
| 5.1 | Carregar checklist | 1. Acessar página | ✅ 6 fases com itens aparecem |
| 5.2 | Marcar item | 1. Clicar checkbox | ✅ Item marca como feito |
| 5.3 | Progresso visual | 1. Marcar vários itens | ✅ Barra de progresso atualiza |
| 5.4 | Persistência | 1. Marcar itens<br>2. Recarregar página | ✅ Itens permanecem marcados |
| 5.5 | Reset checklist | 1. Clicar "Resetar" | ✅ Confirmação<br>✅ Todos desmarcados |

---

### ✅ Teste 6: Relatórios
**URL:** http://localhost:8000/relatorios.html

| # | Teste | Passos | Resultado Esperado |
|---|-------|--------|-------------------|
| 6.1 | Carregar relatório | 1. Acessar página | ✅ Resumo semanal aparece |
| 6.2 | Gráficos | 1. Visualizar gráficos | ✅ Charts renderizam |
| 6.3 | Comparação | 1. Ver "vs Meta" | ✅ Indicadores de status |
| 6.4 | Top 3 posts | 1. Ver seção "Melhores Posts" | ✅ Lista com 3 posts |
| 6.5 | Export PDF | 1. Clicar "Exportar PDF" | ✅ PDF baixado |

---

### ✅ Teste 7: Configurações
**URL:** http://localhost:8000/configuracoes.html

| # | Teste | Passos | Resultado Esperado |
|---|-------|--------|-------------------|
| 7.1 | Carregar configurações | 1. Acessar página | ✅ Form com valores atuais |
| 7.2 | Editar threshold | 1. Mudar CTR min para 2.0<br>2. Salvar | ✅ Mensagem de sucesso |
| 7.3 | Configurar WhatsApp | 1. Alterar número<br>2. Salvar | ✅ Número atualizado |
| 7.4 | Validação | 1. Inserir valor inválido<br>2. Tentar salvar | ✅ Mensagem de erro |

---

## ⚙️ TESTES DE BACKEND

**Pré-requisito:** Backend rodando em http://localhost:3000

### ✅ Teste 8: API de Autenticação

| # | Teste | cURL | Resultado Esperado |
|---|-------|------|-------------------|
| 8.1 | Health check | `curl http://localhost:3000/api/health` | ✅ Status 200<br>✅ JSON com status:online |
| 8.2 | Login | `curl -X POST http://localhost:3000/api/auth/login -H "Content-Type: application/json" -d '{"email":"gerente@macspark.dev","password":"Sabrina2025!"}'` | ✅ Status 200<br>✅ Token JWT retornado |
| 8.3 | Login inválido | `curl -X POST http://localhost:3000/api/auth/login -H "Content-Type: application/json" -d '{"email":"test@test.com","password":"wrong"}'` | ❌ Status 401<br>❌ Erro "Credenciais inválidas" |
| 8.4 | Get me | `curl http://localhost:3000/api/auth/me -H "Authorization: Bearer {token}"` | ✅ Status 200<br>✅ Dados do usuário |

---

### ✅ Teste 9: API de Métricas

| # | Teste | cURL | Resultado Esperado |
|---|-------|------|-------------------|
| 9.1 | Listar métricas | `curl http://localhost:3000/api/metrics?period=7d -H "Authorization: Bearer {token}"` | ✅ Array de métricas |
| 9.2 | Criar métrica | `curl -X POST http://localhost:3000/api/metrics -H "Authorization: Bearer {token}" -d '{"date":"2025-10-21","ctr":7.5,"cpc":0.09,"cost":20}'` | ✅ Status 201<br>✅ Métrica criada |
| 9.3 | Métrica duplicada | Repetir 9.2 com mesma data | ❌ Status 409<br>❌ Erro "já existe" |
| 9.4 | Data futura | Data: "2026-01-01" | ❌ Status 400<br>❌ Erro "data futura" |
| 9.5 | CTR inválido | CTR: 150 | ❌ Status 400<br>❌ Erro "0-100" |

---

### ✅ Teste 10: Webhook n8n

| # | Teste | cURL | Resultado Esperado |
|---|-------|------|-------------------|
| 10.1 | Webhook JSON | `curl -X POST http://localhost:3000/api/webhook/metrics -H "X-Webhook-Token: {secret}" -d '{"date":"2025-10-22","ctr":8,"cpc":0.08,"cost":20}'` | ✅ Status 200<br>✅ Métrica salva |
| 10.2 | Webhook CSV | `curl -X POST http://localhost:3000/api/webhook/metrics/csv -H "X-Webhook-Token: {secret}" --data-binary @data.csv` | ✅ Status 200<br>✅ CSV parsed e salvo |
| 10.3 | Token inválido | Sem header X-Webhook-Token | ❌ Status 401 |

---

## 🔗 TESTES DE INTEGRAÇÃO

### ✅ Teste 11: Frontend + Backend

| # | Teste | Passos | Resultado Esperado |
|---|-------|--------|-------------------|
| 11.1 | Login real | 1. Frontend chama /api/auth/login<br>2. Backend responde | ✅ Token recebido<br>✅ Redirecionamento |
| 11.2 | Dashboard com dados reais | 1. GET /api/metrics<br>2. Renderizar gráficos | ✅ Dados carregam<br>✅ Gráficos aparecem |
| 11.3 | Timeout handling | 1. Backend lento/offline<br>2. Frontend espera | ✅ Loading spinner<br>✅ Mensagem de timeout |

---

### ✅ Teste 12: n8n + Backend

| # | Teste | Passos | Resultado Esperado |
|---|-------|--------|-------------------|
| 12.1 | Workflow 1 | 1. POST webhook com CSV<br>2. n8n processa<br>3. Salva no banco | ✅ Métrica no banco<br>✅ Log de sucesso |
| 12.2 | Workflow 2 | 1. Métrica com CTR < 1.5%<br>2. n8n verifica às 18h | ✅ Alerta gerado<br>✅ WhatsApp enviado |
| 12.3 | Workflow 3 | 1. Cron 18h05<br>2. n8n compila dados | ✅ Relatório gerado<br>✅ WhatsApp enviado |
| 12.4 | Workflow 4 | 1. Cron 11h/17h30<br>2. n8n verifica cronograma | ✅ Lembrete enviado se houver post |

---

## 🎯 TESTES END-TO-END

### ✅ Cenário 1: Fluxo Completo de Atualização de Métricas

**Narrativa:** Gerente recebe relatório do Meta Ads e atualiza dashboard

**Passos:**
1. Exportar CSV do Meta Ads
2. Enviar POST para webhook n8n (Workflow 1)
3. n8n processa e salva no banco
4. n8n verifica thresholds
5. Se CTR < 1.5%, dispara alerta WhatsApp (Workflow 2)
6. Dashboard atualiza automaticamente (refresh)
7. Gerente visualiza métricas atualizadas

**Validações:**
- [ ] CSV parseado corretamente
- [ ] Dados validados
- [ ] Salvos no PostgreSQL
- [ ] Alertas disparados se necessário
- [ ] WhatsApp recebido
- [ ] Dashboard atualizado

---

### ✅ Cenário 2: Relatório Diário Automático

**Narrativa:** Sistema envia relatório diário às 18h05

**Passos:**
1. n8n Cron dispara às 18h05 (ou execução manual)
2. n8n busca métricas do dia (GET /api/metrics)
3. n8n calcula comparações (vs ontem, vs meta)
4. n8n formata relatório
5. n8n envia via Evolution API
6. Sabrina recebe WhatsApp

**Validações:**
- [ ] Cron executa no horário
- [ ] Métricas corretas buscadas
- [ ] Cálculos precisos
- [ ] Mensagem bem formatada
- [ ] WhatsApp enviado
- [ ] Log registrado no banco

---

### ✅ Cenário 3: Lembrete de Postagem

**Narrativa:** Sistema lembra Sabrina de postar às 17h30

**Passos:**
1. n8n Cron dispara às 17h30
2. n8n busca posts planejados para hoje (GET /api/schedule)
3. n8n filtra posts para próximas 2 horas
4. n8n formata lembrete com hook e CTA
5. n8n envia via WhatsApp
6. n8n cria notificação no dashboard
7. Sabrina recebe e posta
8. Sabrina marca como "postado" no dashboard

**Validações:**
- [ ] Cron executa
- [ ] Post correto identificado
- [ ] Lembrete enviado
- [ ] Notificação no dashboard
- [ ] Status atualizado

---

## 🔧 TESTES MANUAIS (CHECKLIST)

### Frontend

**index.html:**
- [ ] Abre sem erros console
- [ ] Design carrega corretamente
- [ ] Formulário funciona
- [ ] Login mock funciona
- [ ] Responsivo em mobile/tablet/desktop

**dashboard.html:**
- [ ] Abre sem erros console
- [ ] Navegação funciona
- [ ] 4 KPIs aparecem
- [ ] 2 gráficos renderizam
- [ ] Filtro de período funciona
- [ ] Auto-refresh funciona
- [ ] Logout funciona

**cronograma.html:**
- [ ] Timeline visual aparece
- [ ] Filtros funcionam
- [ ] Busca funciona
- [ ] Marcar como postado funciona

**ganchos.html:**
- [ ] 50 ganchos carregam
- [ ] Filtros por categoria funcionam
- [ ] Busca funciona
- [ ] Copiar para clipboard funciona

**checklist.html:**
- [ ] Fases aparecem
- [ ] Checkboxes funcionam
- [ ] Progresso atualiza
- [ ] Persistência funciona
- [ ] Reset funciona

**relatorios.html:**
- [ ] Resumo carrega
- [ ] Gráficos aparecem
- [ ] Export PDF funciona

**configuracoes.html:**
- [ ] Form carrega com valores
- [ ] Edição funciona
- [ ] Validação funciona
- [ ] Salvamento funciona

---

### Backend

**Servidor:**
- [ ] Inicia sem erros
- [ ] Conecta ao banco
- [ ] Health check responde

**Autenticação:**
- [ ] Login funciona
- [ ] Token válido
- [ ] Logout funciona
- [ ] Proteção de rotas funciona

**Métricas:**
- [ ] GET lista métricas
- [ ] POST cria métrica
- [ ] PUT atualiza métrica
- [ ] DELETE remove métrica
- [ ] Validações funcionam

**Webhook:**
- [ ] Recebe JSON
- [ ] Recebe CSV
- [ ] Valida dados
- [ ] Salva no banco
- [ ] Verifica thresholds

---

## 📊 RESULTADO DOS TESTES

**Execute este checklist e marque:**

```
Frontend:       [  ] de 42 testes passaram
Backend:        [  ] de 25 testes passaram
Integração:     [  ] de 12 testes passaram
End-to-End:     [  ] de 3 cenários completos

TOTAL:          [  ] de 82 testes
```

---

## 🚀 PRÓXIMOS PASSOS

1. ✅ Marcar todos testes acima
2. ✅ Documentar falhas (se houver)
3. ✅ Corrigir bugs encontrados
4. ✅ Re-testar
5. ✅ Aprovar para produção

---

**📝 Por favor, revise o code_summary.json gerado e execute os testes acima!**

**Servidor rodando em:** http://localhost:8000 ✅

