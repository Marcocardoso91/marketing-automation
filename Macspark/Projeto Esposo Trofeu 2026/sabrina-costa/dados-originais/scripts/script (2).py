
import pandas as pd
from datetime import datetime, timedelta

# Criar cronograma de 4 semanas completo
# Data inicial: 21 de outubro de 2025
start_date = datetime(2025, 10, 21)

# Criar lista de posts para 4 semanas
cronograma = []

# SEMANA 1 (21-27 outubro) - Consolidação pós-engajamento
semana1 = [
    {"Data": "21/10 (Seg)", "Formato": "Reel", "Tema": "Transformação (Antes/Depois)", "Hook": "Olha só o que 7 dias fizeram...", "CTA": "Me segue pra ver mais transformações", "Objetivo": "Migração Tráfego + Seguidores", "Stories": "3-5 stories: Bastidores da gravação + Enquete 'Você cuida do seu cabelo?'"},
    {"Data": "22/10 (Ter)", "Formato": "Stories", "Tema": "Rotina matinal", "Hook": "Você começa o dia assim também?", "CTA": "Responde aqui", "Objetivo": "Engajamento Stories", "Stories": "Sequência de 5-7 stories mostrando rotina"},
    {"Data": "23/10 (Qua)", "Formato": "Reel", "Tema": "Autocuidado Real", "Hook": "Hoje escolhi ME CUIDAR...", "CTA": "Salva pra lembrar", "Objetivo": "Salvamentos + Alcance", "Stories": "Behind the scenes do Reel + Caixinha de perguntas"},
    {"Data": "24/10 (Qui)", "Formato": "Stories", "Tema": "Dica rápida capilar", "Hook": "Você está fazendo isso ERRADO", "CTA": "Testa e me conta", "Objetivo": "Interação DM", "Stories": "Tutorial em 3 passos"},
    {"Data": "25/10 (Sex)", "Formato": "Reel", "Tema": "Recomeços + Reflexão", "Hook": "Desisti várias vezes, mas...", "CTA": "Esse perfil é seu lugar", "Objetivo": "Conexão Emocional", "Stories": "Mensagem inspiradora + Música"},
    {"Data": "26/10 (Sáb)", "Formato": "Carrossel", "Tema": "Hidratação Passo a Passo", "Hook": "3 passos pro cabelo dos sonhos", "CTA": "Salva e compartilha", "Objetivo": "Educação + Salvamentos", "Stories": "Resultado da hidratação"},
    {"Data": "27/10 (Dom)", "Formato": "Stories", "Tema": "Descanso e reflexão", "Hook": "Domingos também são importantes", "CTA": "Como foi sua semana?", "Objetivo": "Proximidade", "Stories": "Momento pessoal + Playlist"}
]

# SEMANA 2 (28 out - 3 nov) - Consolidação de tráfego
semana2 = [
    {"Data": "28/10 (Seg)", "Formato": "Reel TESTE A", "Tema": "Segredo que ninguém conta", "Hook": "Ninguém te conta isso sobre cabelo...", "CTA": "Testa no seu cabelo hoje", "Objetivo": "Teste A/B Hook", "Stories": "Enquete: 'Você sabia disso?'"},
    {"Data": "29/10 (Ter)", "Formato": "Stories", "Tema": "Dia a dia real", "Hook": "Um dia na minha vida", "CTA": "Quer ver mais?", "Objetivo": "Humanização", "Stories": "Vlog Stories 7-10 cards"},
    {"Data": "30/10 (Qua)", "Formato": "Reel TESTE B", "Tema": "Erros comuns (Carrossel em vídeo)", "Hook": "3 erros que TODOS cometem", "CTA": "Curta e siga pra mais", "Objetivo": "Teste A/B Formato", "Stories": "Complemento dos erros"},
    {"Data": "31/10 (Qui)", "Formato": "Stories", "Tema": "Interação direta", "Hook": "Me pergunta QUALQUER coisa", "CTA": "Caixinha aberta", "Objetivo": "Engajamento DM", "Stories": "Caixinha de perguntas + respostas"},
    {"Data": "01/11 (Sex)", "Formato": "Reel", "Tema": "Conteúdo Viral (melhor da semana)", "Hook": "Isso mudou TUDO pra mim", "CTA": "Compartilha com quem precisa", "Objetivo": "Compartilhamentos", "Stories": "Agradecimento + Meta de seguidores"},
    {"Data": "02/11 (Sáb)", "Formato": "Carrossel", "Tema": "Produtos que uso (Recomendação)", "Hook": "5 produtos que VALEM a pena", "CTA": "Salva pra não esquecer", "Objetivo": "Autoridade", "Stories": "Detalhes de cada produto"},
    {"Data": "03/11 (Dom)", "Formato": "Stories", "Tema": "Enquete + Poll", "Hook": "Qual seu maior desafio capilar?", "CTA": "Vote aqui", "Objetivo": "Research de audiência", "Stories": "Série de enquetes"}
]

# SEMANA 3 (4-10 nov) - Escalonamento
semana3 = [
    {"Data": "04/11 (Seg)", "Formato": "Reel", "Tema": "Resultado comprovado", "Hook": "A prova está aqui...", "CTA": "Me segue pra acompanhar", "Objetivo": "Social Proof", "Stories": "Depoimentos (se houver)"},
    {"Data": "05/11 (Ter)", "Formato": "Stories", "Tema": "Tutorial completo", "Hook": "Passo a passo COMPLETO", "CTA": "Salva nos destaques", "Objetivo": "Conteúdo de valor", "Stories": "Tutorial em 10+ cards"},
    {"Data": "06/11 (Qua)", "Formato": "Reel", "Tema": "Tendência/Áudio viral", "Hook": "[Áudio em alta]", "CTA": "Faz o seu também", "Objetivo": "Alcance algorítmico", "Stories": "Bastidores da tendência"},
    {"Data": "07/11 (Qui)", "Formato": "Stories", "Tema": "Antes & Depois", "Hook": "Transformação real", "CTA": "Desliza pra ver", "Objetivo": "Prova visual", "Stories": "Comparativo em slides"},
    {"Data": "08/11 (Sex)", "Formato": "Reel", "Tema": "Storytelling pessoal", "Hook": "Eu pensei que era impossível até...", "CTA": "Se identifica? Comenta", "Objetivo": "Conexão profunda", "Stories": "Continuação da história"},
    {"Data": "09/11 (Sáb)", "Formato": "Carrossel", "Tema": "Checklist/Guia prático", "Hook": "Checklist: cabelo saudável em 30 dias", "CTA": "Salva e segue o plano", "Objetivo": "Conteúdo salvável", "Stories": "Motivação para começar"},
    {"Data": "10/11 (Dom)", "Formato": "Stories", "Tema": "Recap da semana", "Hook": "Essa semana foi incrível", "CTA": "Qual foi seu post favorito?", "Objetivo": "Feedback", "Stories": "Melhores momentos"}
]

# SEMANA 4 (11-17 nov) - Otimização e relatório
semana4 = [
    {"Data": "11/11 (Seg)", "Formato": "Reel", "Tema": "Melhor conteúdo (repost otimizado)", "Hook": "[Hook com melhor performance]", "CTA": "Não viu? Então vê agora", "Objetivo": "Maximizar melhor criativo", "Stories": "Por que repostei"},
    {"Data": "12/11 (Ter)", "Formato": "Stories", "Tema": "Sessão AMA (Ask Me Anything)", "Hook": "Respondo TUDO hoje", "CTA": "Pergunta o que quiser", "Objetivo": "Proximidade máxima", "Stories": "Sessão de respostas"},
    {"Data": "13/11 (Qua)", "Formato": "Reel", "Tema": "Colaboração (se possível)", "Hook": "Olha quem veio aqui", "CTA": "Segue nós duas", "Objetivo": "Cross-promotion", "Stories": "Bastidores da collab"},
    {"Data": "14/11 (Qui)", "Formato": "Stories", "Tema": "Rotina noturna", "Hook": "Como termino meu dia", "CTA": "E você?", "Objetivo": "Conteúdo de identificação", "Stories": "Vlog noturno"},
    {"Data": "15/11 (Sex)", "Formato": "Reel", "Tema": "Mito vs Verdade", "Hook": "Você acredita nisso? É MITO!", "CTA": "Compartilha pra educar", "Objetivo": "Educação + Viralização", "Stories": "Mais mitos desmistificados"},
    {"Data": "16/11 (Sáb)", "Formato": "Carrossel", "Tema": "Retrospectiva do mês", "Hook": "1 mês de transformação", "CTA": "Acompanha a jornada", "Objetivo": "Celebração", "Stories": "Gratidão + Números"},
    {"Data": "17/11 (Dom)", "Formato": "Stories", "Tema": "Planejamento próxima semana", "Hook": "Semana que vem vem novidade", "CTA": "Ativa as notificações", "Objetivo": "Antecipação", "Stories": "Teaser de conteúdos"}
]

# Combinar todas as semanas
cronograma.extend(semana1)
cronograma.extend(semana2)
cronograma.extend(semana3)
cronograma.extend(semana4)

# Criar DataFrame
df_cronograma = pd.DataFrame(cronograma)

# Salvar como CSV
df_cronograma.to_csv("cronograma_4_semanas_sabrina.csv", index=False, encoding='utf-8-sig')

print("Cronograma de 4 semanas criado com sucesso!")
print(f"\nTotal de posts planejados: {len(cronograma)}")
print(f"Total de Reels: {len([p for p in cronograma if 'Reel' in p['Formato']])}")
print(f"Total de Carrosséis: {len([p for p in cronograma if 'Carrossel' in p['Formato']])}")
print(f"Total de dias com Stories: {len([p for p in cronograma if 'Stories' in p['Formato']])}")
