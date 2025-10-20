# PRD - Product Requirements Document
## Dashboard Sabrina Costa + Automação n8n

**Versão:** 1.0  
**Data:** 20 de Outubro de 2025  
**Autor:** Macspark Team  
**Status:** Aprovado para Implementação

---

## 1. VISÃO GERAL DO PRODUTO

### 1.1 Objetivo
Criar uma solução web completa para gerenciar e automatizar o projeto de crescimento da Sabrina Costa no Instagram, incluindo:
- Dashboard executivo com métricas em tempo real
- Sistema de automação de alertas via WhatsApp
- Gestão de cronograma de conteúdo
- Biblioteca de ganchos virais
- Relatórios automáticos diários

### 1.2 Problema que Resolve
- **Dispersão de informações**: Dados em múltiplos arquivos (CSV, MD, TXT)
- **Monitoramento manual**: Necessidade de verificar métricas manualmente
- **Falta de alertas**: Sem notificações quando métricas saem do padrão
- **Pouca visibilidade**: Cliente não tem acesso visual aos dados
- **Trabalho repetitivo**: Relatórios diários feitos manualmente

### 1.3 Público-Alvo
- **Primário**: Gerente do projeto (você) - controle total, acesso a todas funcionalidades
- **Secundário**: Sabrina (cliente) - visualização de métricas e cronograma
- **Terciário**: Equipe de suporte - monitoramento de alertas

---

## 2. REQUISITOS FUNCIONAIS

### 2.1 Autenticação e Autorização

#### RF-001: Login de Usuário
- **Descrição**: Sistema de login com email e senha
- **Prioridade**: Alta
- **Critérios de Aceitação**:
  - Validação de email e senha
  - Geração de token JWT com validade de 7 dias
  - Mensagem de erro clara em caso de falha
  - Redirecionamento para dashboard após login bem-sucedido
  - Opção "Lembrar-me" para manter sessão

#### RF-002: Logout de Usuário
- **Descrição**: Encerrar sessão do usuário
- **Prioridade**: Alta
- **Critérios de Aceitação**:
  - Remover token JWT do storage
  - Redirecionar para tela de login
  - Limpar todos os dados em cache

#### RF-003: Proteção de Rotas
- **Descrição**: Apenas usuários autenticados podem acessar dashboard
- **Prioridade**: Alta
- **Critérios de Aceitação**:
  - Redirecionar para login se não autenticado
  - Verificar validade do token em cada requisição
  - Renovar token automaticamente se próximo do vencimento

### 2.2 Dashboard Principal

#### RF-004: Exibir KPIs Principais
- **Descrição**: Cards com métricas principais do Instagram
- **Prioridade**: Alta
- **Critérios de Aceitação**:
  - Exibir: Alcance, CTR, CPC, CPM, Frequência, Novos Seguidores
  - Indicador visual de status (verde/amarelo/vermelho)
  - Comparação com meta estabelecida
  - Atualização em tempo real (ou refresh a cada 5 min)

#### RF-005: Gráfico de Evolução de Métricas
- **Descrição**: Gráfico de linha mostrando evolução temporal
- **Prioridade**: Alta
- **Critérios de Aceitação**:
  - Exibir últimos 30 dias de dados
  - Filtro para selecionar métrica (CTR, CPC, seguidores)
  - Hover mostrando valor exato de cada ponto
  - Linha de meta para comparação

#### RF-006: Gráfico de Investimento vs Retorno
- **Descrição**: Gráfico de barras comparando investimento e resultados
- **Prioridade**: Média
- **Critérios de Aceitação**:
  - Eixo X: datas, Eixo Y: valores em R$
  - Barras duplas: gasto vs valor de seguidores adquiridos
  - Cálculo de ROI exibido

#### RF-007: Lista de Alertas Recentes
- **Descrição**: Widget mostrando últimos alertas gerados
- **Prioridade**: Média
- **Critérios de Aceitação**:
  - Mostrar últimos 5 alertas
  - Cor diferenciada por tipo (erro, aviso, info)
  - Link "Ver todos" para página de alertas completa

### 2.3 Cronograma de Posts

#### RF-008: Exibir Timeline Visual
- **Descrição**: Linha do tempo com posts planejados das 4 semanas
- **Prioridade**: Alta
- **Critérios de Aceitação**:
  - Organização por semana e dia
  - Cards com: Data, Formato, Tema, Hook, CTA
  - Diferenciação visual por formato (Reel, Carrossel, Stories)
  - Status do post (planejado, postado, cancelado)

#### RF-009: Filtrar Posts
- **Descrição**: Filtros para facilitar busca
- **Prioridade**: Baixa
- **Critérios de Aceitação**:
  - Filtrar por formato
  - Filtrar por semana
  - Filtrar por status
  - Busca por palavra-chave no tema

#### RF-010: Marcar Post como Concluído
- **Descrição**: Interação para marcar post como postado
- **Prioridade**: Média
- **Critérios de Aceitação**:
  - Checkbox ou botão de ação
  - Alteração visual do card
  - Salvamento persistente no banco

### 2.4 Biblioteca de Ganchos Virais

#### RF-011: Exibir 50 Ganchos em Cards
- **Descrição**: Biblioteca visual dos ganchos organizados
- **Prioridade**: Alta
- **Critérios de Aceitação**:
  - Cards individuais para cada gancho
  - Categoria visível (Curiosidade, Urgência, etc)
  - Texto do gancho legível e destacado

#### RF-012: Filtrar por Categoria
- **Descrição**: Filtros de categoria de gancho
- **Prioridade**: Alta
- **Critérios de Aceitação**:
  - 10 categorias filtráveis
  - Botões ou dropdown de seleção
  - Mostrar quantidade de ganchos por categoria
  - "Limpar filtros" para voltar ao estado inicial

#### RF-013: Copiar Gancho para Clipboard
- **Descrição**: Botão para copiar texto do gancho
- **Prioridade**: Média
- **Critérios de Aceitação**:
  - Botão "Copiar" em cada card
  - Feedback visual de cópia bem-sucedida
  - Funcionar em todos navegadores modernos

#### RF-014: Buscar Gancho por Palavra-chave
- **Descrição**: Campo de busca textual
- **Prioridade**: Média
- **Critérios de Aceitação**:
  - Campo de input com placeholder
  - Busca em tempo real (debounce de 300ms)
  - Destacar termo buscado nos resultados

### 2.5 Checklist de Produção

#### RF-015: Exibir Checklist Interativo
- **Descrição**: Lista de tarefas para produção de conteúdo
- **Prioridade**: Média
- **Critérios de Aceitação**:
  - Organização por fases (Planejamento, Gravação, Edição, etc)
  - Checkboxes funcionais
  - Progresso visual (barra de progresso)
  - Persistência de estado

#### RF-016: Resetar Checklist
- **Descrição**: Botão para iniciar novo ciclo de produção
- **Prioridade**: Baixa
- **Critérios de Aceitação**:
  - Botão visível
  - Confirmação antes de resetar
  - Todos checkboxes desmarcados

### 2.6 Relatórios

#### RF-017: Visualizar Relatórios Semanais
- **Descrição**: Página com relatórios compilados
- **Prioridade**: Média
- **Critérios de Aceitação**:
  - Resumo executivo da semana
  - Gráficos de performance
  - Comparação com metas
  - Destacar top 3 posts

#### RF-018: Exportar Relatório em PDF
- **Descrição**: Botão para gerar PDF do relatório
- **Prioridade**: Baixa
- **Critérios de Aceitação**:
  - Gerar PDF bem formatado
  - Incluir gráficos e tabelas
  - Download automático
  - Nome de arquivo com data

### 2.7 Configurações

#### RF-019: Configurar Metas de Métricas
- **Descrição**: Interface para definir valores de meta
- **Prioridade**: Média
- **Critérios de Aceitação**:
  - Campos editáveis para cada métrica
  - Validação de valores numéricos
  - Salvamento persistente
  - Feedback de sucesso

#### RF-020: Configurar Alertas
- **Descrição**: Definir quando receber alertas
- **Prioridade**: Alta
- **Critérios de Aceitação**:
  - Checkboxes para tipos de alerta
  - Campos para thresholds personalizados
  - Horários de recebimento de alertas
  - Número de WhatsApp de destino

---

## 3. REQUISITOS NÃO-FUNCIONAIS

### 3.1 Performance

#### RNF-001: Tempo de Carregamento
- Dashboard deve carregar em menos de 2 segundos
- Transições entre páginas instantâneas (SPA)
- Gráficos renderizados em menos de 500ms

#### RNF-002: Responsividade
- Funcionar perfeitamente em desktop (1920x1080)
- Funcionar bem em tablet (768x1024)
- Funcionar em mobile (375x667)
- Touch-friendly em dispositivos móveis

### 3.2 Segurança

#### RNF-003: Autenticação
- Tokens JWT com expiração de 7 dias
- Refresh token automático
- Senha hasheada com bcrypt (10 rounds)
- HTTPS obrigatório em produção

#### RNF-004: Proteção de API
- Rate limiting: 100 requests/minuto por IP
- CORS configurado para domínios específicos
- Validação de entrada em todos endpoints
- Sanitização de dados contra XSS/SQL Injection

### 3.3 Usabilidade

#### RNF-005: Acessibilidade
- Contraste de cores adequado (WCAG AA)
- Navegação por teclado funcional
- Labels em todos inputs
- Feedback visual de ações

#### RNF-006: Internacionalização
- Todos textos em português brasileiro
- Formato de data: DD/MM/AAAA
- Moeda: R$ (Real brasileiro)
- Fuso horário: America/Sao_Paulo

### 3.4 Compatibilidade

#### RNF-007: Navegadores Suportados
- Chrome 100+
- Firefox 100+
- Safari 15+
- Edge 100+
- Não suportar IE11

### 3.5 Disponibilidade

#### RNF-008: Uptime
- 99% de uptime mensal
- Deploy sem downtime (Vercel cuida)
- Backup diário do banco de dados

---

## 4. AUTOMAÇÕES n8n

### 4.1 Workflow 1: Processar Métricas

#### A-001: Receber Dados via Webhook
- **Trigger**: HTTP Webhook POST
- **Input**: CSV ou JSON com métricas
- **Processamento**:
  1. Parse CSV/JSON
  2. Validar campos obrigatórios
  3. Converter tipos de dados
  4. Calcular campos derivados (ex: custo por seguidor)
- **Output**: JSON estruturado

#### A-002: Salvar no Banco de Dados
- **Ação**: POST para API /api/metrics
- **Validações**:
  - Data não pode ser futura
  - CTR entre 0 e 100
  - CPC maior que 0
  - Não duplicar registros da mesma data
- **Tratamento de Erro**: Log e notificação se falhar

#### A-003: Atualizar Dashboard
- **Ação**: Emitir evento WebSocket (ou SSE)
- **Payload**: Dados atualizados
- **Resultado**: Dashboard atualiza automaticamente

### 4.2 Workflow 2: Alertas WhatsApp

#### A-004: Verificar Métricas Diariamente
- **Trigger**: Cron (todo dia 18h)
- **Ação**: GET /api/metrics?date=today
- **Verificações**:
  - CTR < 1.5% → Alerta
  - CPC > R$0.70 → Alerta
  - Frequência > 3.0 → Alerta
  - Custo por seguidor > R$1.30 → Alerta

#### A-005: Enviar Mensagem WhatsApp
- **Integração**: Evolution API (HTTP Request)
- **Formato da Mensagem**:
```
⚠️ ALERTA DE MÉTRICAS - [DATA]

[Emoji] [Métrica]: [Valor]
Meta: [Valor Meta]
Status: [Acima/Abaixo da Meta]

[Recomendação de ação]

---
Dashboard: [URL]
```
- **Tratamento**: Retry 3x em caso de falha

#### A-006: Registrar Alerta Enviado
- **Ação**: POST /api/alerts
- **Dados**: tipo, mensagem, timestamp, status
- **Finalidade**: Histórico e auditoria

### 4.3 Workflow 3: Relatório Diário

#### A-007: Compilar Dados do Dia
- **Trigger**: Cron (todo dia 18h)
- **Fonte**: GET /api/metrics?date=today
- **Compilação**:
  - Resumo de todas métricas
  - Comparação com dia anterior
  - Comparação com meta
  - Status geral (bom/atenção/crítico)

#### A-008: Formatar Relatório
- **Template**:
```
📊 RELATÓRIO DIÁRIO - [DATA]

✅ MÉTRICAS DO DIA
• Alcance: [valor]
• CTR: [valor]%
• CPC: R$[valor]
• Novos Seguidores: [valor]
• Investimento: R$[valor]

📈 COMPARAÇÃO
• vs Ontem: [+/-X%]
• vs Meta: [status]

🎯 STATUS GERAL: [Emoji + Texto]

---
Ver detalhes: [URL]
```

#### A-009: Enviar via WhatsApp
- **Destinatário**: Número configurado
- **Horário**: 18h (após verificação de alertas)

### 4.4 Workflow 4: Lembretes de Postagem

#### A-010: Verificar Cronograma
- **Trigger**: Cron (múltiplos horários)
  - 11h (posts meio-dia)
  - 17h30 (posts 18h-20h)
- **Ação**: GET /api/schedule?date=today
- **Filtro**: Posts planejados para horário atual ±30min

#### A-011: Enviar Lembrete
- **Mensagem**:
```
🎬 LEMBRETE DE POSTAGEM

Horário: [Hora]
Formato: [Reel/Carrossel/Stories]
Tema: [Tema do Post]
Hook: "[Gancho]"
CTA: "[Call to Action]"

✅ Marcar como concluído: [URL]
```

#### A-012: Notificação no Dashboard
- **Tipo**: Toast/Banner
- **Ação**: Destacar post no cronograma
- **Persistência**: Até ser marcado como concluído

---

## 5. CASOS DE USO

### UC-001: Gerente Monitora Métricas
**Ator**: Gerente do Projeto  
**Pré-condição**: Estar autenticado  
**Fluxo Principal**:
1. Gerente acessa dashboard
2. Sistema exibe KPIs atualizados
3. Gerente visualiza gráfico de evolução
4. Gerente identifica métrica fora do padrão
5. Sistema já enviou alerta via WhatsApp
6. Gerente toma ação corretiva

**Pós-condição**: Decisão informada tomada

### UC-002: Sistema Envia Alerta Automático
**Ator**: Sistema (n8n)  
**Trigger**: Cron diário 18h  
**Fluxo Principal**:
1. n8n busca métricas do dia
2. n8n verifica cada métrica contra threshold
3. n8n identifica CTR abaixo de 1.5%
4. n8n formata mensagem de alerta
5. n8n envia via Evolution API para WhatsApp
6. n8n registra alerta no banco de dados
7. Gerente recebe notificação no celular

**Pós-condição**: Gerente notificado imediatamente

### UC-003: Sabrina Consulta Cronograma
**Ator**: Sabrina (Cliente)  
**Pré-condição**: Estar autenticada  
**Fluxo Principal**:
1. Sabrina acessa página de cronograma
2. Sistema exibe timeline de 4 semanas
3. Sabrina visualiza post de amanhã
4. Sabrina lê gancho e CTA
5. Sabrina se prepara para gravação

**Pós-condição**: Cliente informada sobre próximo post

### UC-004: Gerente Atualiza Métricas Manualmente
**Ator**: Gerente  
**Pré-condição**: Ter arquivo CSV de métricas  
**Fluxo Principal**:
1. Gerente exporta CSV do Meta Ads
2. Gerente envia POST para webhook n8n
3. n8n processa CSV
4. n8n valida dados
5. n8n salva no banco via API
6. Dashboard atualiza automaticamente
7. n8n verifica se há alertas
8. n8n envia alertas se necessário

**Fluxo Alternativo 4a**: Dados inválidos
- Sistema retorna erro
- Gerente corrige CSV
- Reinicia processo

**Pós-condição**: Métricas atualizadas e visíveis

### UC-005: Sistema Envia Lembrete de Postagem
**Ator**: Sistema (n8n)  
**Trigger**: Cron às 17h30  
**Fluxo Principal**:
1. n8n verifica cronograma do dia
2. n8n identifica Reel planejado para 18h
3. n8n busca detalhes do post
4. n8n formata lembrete
5. n8n envia via WhatsApp
6. n8n cria notificação no dashboard
7. Sabrina recebe lembrete no celular
8. Sabrina posta no horário certo

**Pós-condição**: Post publicado no horário planejado

---

## 6. TECNOLOGIAS E DEPENDÊNCIAS

### 6.1 Frontend
- **HTML5**: Estrutura semântica
- **Tailwind CSS 3.4**: Estilização utilitária
- **Alpine.js 3.x**: Reatividade leve
- **Chart.js 4.x**: Gráficos interativos
- **Axios**: HTTP client
- **Day.js**: Manipulação de datas

### 6.2 Backend
- **Node.js 18+**: Runtime JavaScript
- **Express 4.x**: Framework web
- **PostgreSQL 15**: Banco de dados relacional
- **jsonwebtoken**: Geração de JWT
- **bcryptjs**: Hash de senhas
- **dotenv**: Variáveis de ambiente
- **cors**: Configuração CORS
- **helmet**: Segurança HTTP headers

### 6.3 Automação
- **n8n**: Plataforma de automação (já instalado)
- **Evolution API**: Integração WhatsApp

### 6.4 Infraestrutura
- **Vercel**: Hospedagem frontend e serverless functions
- **Supabase/Railway**: Banco PostgreSQL
- **GitHub**: Versionamento de código

---

## 7. MÉTRICAS DE SUCESSO

### 7.1 Adoção
- 100% das métricas sendo atualizadas diariamente
- Login diário do gerente
- Login 3x/semana da Sabrina

### 7.2 Eficiência
- Redução de 80% do tempo de monitoramento manual
- 100% dos alertas críticos enviados em até 5 minutos
- 0 posts esquecidos (todos lembretes enviados)

### 7.3 Técnicas
- Tempo de resposta de API < 200ms (p95)
- 0 erros críticos em produção
- 99% de uptime

### 7.4 Negócio
- Melhoria de 20% nas métricas de Instagram (CTR, seguidores)
- Cliente satisfeita (NPS > 9)
- Projeto replicável para outros clientes

---

## 8. CRONOGRAMA DE ENTREGA

### Sprint 1 (Dia 1-2): Fundação
- ✅ Documentação completa
- ✅ Estrutura de pastas
- ✅ Setup de repositório
- ✅ Frontend base (HTML/CSS)
- ✅ Sistema de autenticação

### Sprint 2 (Dia 3-4): Core Features
- ✅ Dashboard com gráficos
- ✅ Página de cronograma
- ✅ Página de ganchos virais
- ✅ Backend API completo
- ✅ Conexão com banco de dados

### Sprint 3 (Dia 5-6): Automação
- ✅ 4 Workflows n8n criados e testados
- ✅ Integração WhatsApp configurada
- ✅ Webhook receiver funcionando
- ✅ Testes de integração completos

### Sprint 4 (Dia 7): Deploy e Documentação
- ✅ Deploy Vercel
- ✅ Configuração de produção
- ✅ Testes end-to-end
- ✅ PDF executivo
- ✅ README completo

---

## 9. RISCOS E MITIGAÇÕES

### Risco 1: Evolution API Offline
- **Probabilidade**: Média
- **Impacto**: Alto (sem alertas WhatsApp)
- **Mitigação**: 
  - Implementar fallback para email
  - Monitorar health da Evolution API
  - Retry automático com backoff exponencial

### Risco 2: Limite da Vercel (Serverless)
- **Probabilidade**: Baixa
- **Impacto**: Médio
- **Mitigação**:
  - Otimizar cold starts
  - Cache agressivo de dados estáticos
  - Plano pago se necessário

### Risco 3: n8n com Alta Latência
- **Probabilidade**: Baixa
- **Impacto**: Médio (alertas atrasados)
- **Mitigação**:
  - Workflows otimizados
  - Timeout configurado
  - Logs para debug

### Risco 4: Dados Sensíveis Vazados
- **Probabilidade**: Baixa
- **Impacto**: Crítico
- **Mitigação**:
  - Todas credenciais em variáveis de ambiente
  - Tokens com expiração curta
  - HTTPS obrigatório
  - Auditoria de segurança antes do deploy

---

## 10. GLOSSÁRIO

- **CTR**: Click-Through Rate (Taxa de Cliques)
- **CPC**: Custo Por Clique
- **CPM**: Custo Por Mil Impressões
- **JWT**: JSON Web Token (token de autenticação)
- **n8n**: Plataforma de automação de workflows
- **Evolution API**: API para integração com WhatsApp
- **Webhook**: Endpoint HTTP que recebe dados de sistemas externos
- **Serverless**: Arquitetura onde backend roda on-demand
- **SPA**: Single Page Application (aplicação de página única)
- **SSE**: Server-Sent Events (eventos enviados pelo servidor)

---

## 11. APROVAÇÕES

| Papel | Nome | Data | Assinatura |
|-------|------|------|------------|
| Product Owner | Marco | 20/10/2025 | ✅ Aprovado |
| Tech Lead | Macspark Team | 20/10/2025 | ✅ Aprovado |
| Cliente | Sabrina | Pendente | - |

---

**Documento vivo**: Este PRD será atualizado conforme necessário durante a implementação.

