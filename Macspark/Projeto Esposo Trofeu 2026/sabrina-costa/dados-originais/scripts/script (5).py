
# Criar guia de Stories com ideias diárias

stories_ideias = {
    "Tipo de Story": [
        "Bom dia motivacional",
        "Bastidores da gravação",
        "Dica rápida (15seg)",
        "Enquete/Pergunta",
        "Rotina matinal",
        "Tutorial rápido",
        "Transformação antes/depois",
        "Produto favorito",
        "Reflexão pessoal",
        "Sessão de perguntas",
        "Dia na vida (vlog)",
        "Meme/Humor",
        "Citação inspiradora",
        "Progresso/Resultado",
        "Erro comum",
        "Repost de seguidor",
        "Link importante",
        "Countdown/Antecipação",
        "Agradecimento",
        "Boa noite/Encerramento",
    ],
    "Melhor Horário": [
        "8h-9h",
        "Durante o dia",
        "12h-13h",
        "13h-14h",
        "8h-10h",
        "11h-12h",
        "18h-19h",
        "14h-15h",
        "20h-21h",
        "19h-20h",
        "Durante o dia",
        "12h ou 19h",
        "9h ou 21h",
        "18h-19h",
        "11h-12h",
        "15h-16h",
        "10h ou 15h",
        "Vários momentos",
        "20h-21h",
        "21h-22h",
    ],
    "Objetivo": [
        "Conexão inicial do dia",
        "Transparência, humanização",
        "Valor, educação rápida",
        "Engajamento, interação",
        "Identificação, lifestyle",
        "Educação, valor",
        "Prova social, resultado",
        "Recomendação, autoridade",
        "Conexão emocional",
        "Interação massiva",
        "Humanização, identificação",
        "Engajamento leve",
        "Inspiração, motivação",
        "Prova, motivação",
        "Educação, correção",
        "Comunidade, UGC",
        "Direcionamento",
        "Expectativa, curiosidade",
        "Reciprocidade",
        "Despedida, conexão",
    ],
    "Exemplo": [
        "'Bom dia! Hoje é dia de autocuidado ☀️'",
        "'Olha os bastidores do Reel de hoje'",
        "'Dica: NUNCA durma com o cabelo molhado'",
        "'Você prefere: cabelo solto ou preso?'",
        "'Minha rotina matinal: skincare + café'",
        "'Como fazer chapinha sem danificar'",
        "'7 dias usando isso: veja o resultado'",
        "'Esse shampoo mudou meu cabelo'",
        "'Hoje acordei pensando em desistir...'",
        "'Me pergunte qualquer coisa sobre cabelo'",
        "'Um dia comigo: da manhã até a noite'",
        "'Quando o cabelo não coopera 😂'",
        "'Seja gentil com você mesma ✨'",
        "'1 mês de projeto: olha a evolução'",
        "'Pare de lavar o cabelo TODO dia'",
        "'Olha o resultado da @seguidora 💕'",
        "'Link do produto nos destaques'",
        "'Novidade chegando em 3...2...1...'",
        "'Obrigada por estar aqui 💛'",
        "'Boa noite! Amanhã tem conteúdo novo'",
    ]
}

df_stories = pd.DataFrame(stories_ideias)
df_stories.to_csv("ideias_stories_instagram.csv", index=False, encoding='utf-8-sig')

print("Guia de Stories com 20 ideias criado!")
print("\nExemplos de Stories para cada momento do dia:")
print("\n📅 MANHÃ (8h-12h):")
for i in [0, 4, 5, 10]:
    print(f"  • {stories_ideias['Tipo de Story'][i]} - {stories_ideias['Exemplo'][i]}")
    
print("\n📅 TARDE (12h-18h):")
for i in [2, 3, 7, 14]:
    print(f"  • {stories_ideias['Tipo de Story'][i]} - {stories_ideias['Exemplo'][i]}")
    
print("\n📅 NOITE (18h-22h):")
for i in [6, 8, 9, 18, 19]:
    print(f"  • {stories_ideias['Tipo de Story'][i]} - {stories_ideias['Exemplo'][i]}")
