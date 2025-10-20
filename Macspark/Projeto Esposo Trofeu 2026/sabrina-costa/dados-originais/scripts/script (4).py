
# Criar lista de 50 ganchos virais categorizados

ganchos_virais = {
    "Categoria": [],
    "Gancho": [],
    "Quando Usar": []
}

# Categoria 1: Curiosidade/Segredo
curiosidade = [
    ("O que NINGUÉM te conta sobre [tema]...", "Educação, revelação"),
    ("Esse segredo mudou TUDO para mim", "Transformação, resultado"),
    ("Você não vai acreditar no que descobri", "Surpresa, revelação"),
    ("Por que ninguém fala sobre isso?", "Polêmica leve, discussão"),
    ("A verdade que escondem de você", "Revelação, mito vs verdade"),
]

# Categoria 2: Urgência/Alerta
urgencia = [
    ("PARE de fazer isso AGORA", "Correção de erro comum"),
    ("Se você faz isso, ESTÁ ERRANDO", "Alerta, correção"),
    ("Você está fazendo isso ERRADO (e eu vou te mostrar)", "Tutorial, correção"),
    ("Último aviso: não faça mais isso", "Urgência, importância"),
    ("Se continuar assim, NUNCA vai conseguir [resultado]", "Motivação, solução"),
]

# Categoria 3: Transformação/Resultado
transformacao = [
    ("Como eu fui de [antes] para [depois]", "Jornada pessoal"),
    ("Isso mudou minha vida em [X dias/meses]", "Resultado, prova social"),
    ("Olha só o que [X dias] fizeram...", "Transformação visual"),
    ("Antes eu era assim... Hoje sou assim", "Evolução, inspiração"),
    ("A transformação que você precisa ver", "Motivação, prova"),
]

# Categoria 4: Identificação/Empatia
identificacao = [
    ("Se você também é assim, me segue", "Conexão, comunidade"),
    ("Quem nunca passou por isso?", "Identificação, empatia"),
    ("Eu pensei que era só EU...", "Vulnerabilidade, conexão"),
    ("Você também se sente assim às vezes?", "Emoção, identificação"),
    ("Se identifica? Então esse perfil é pra você", "Comunidade, pertencimento"),
]

# Categoria 5: Lista/Número
listas = [
    ("3 coisas que NINGUÉM te conta", "Educação, revelação"),
    ("5 erros que TODO MUNDO comete", "Educação, correção"),
    ("7 sinais de que você precisa [ação]", "Checklist, diagnóstico"),
    ("Os 3 segredos de [resultado]", "Tutorial, método"),
    ("10 coisas que eu faria diferente", "Aprendizado, dica"),
]

# Categoria 6: Desafio/Ação
desafio = [
    ("Você tem CORAGEM de tentar?", "Provocação, desafio"),
    ("Faz isso HOJE e me conta o resultado", "Ação imediata, teste"),
    ("Testa isso e me agradeça depois", "Confiança, dica valiosa"),
    ("Se fizer isso, sua vida muda", "Promessa, resultado"),
    ("Grave esse vídeo EXATAMENTE assim", "Tutorial, replicação"),
]

# Categoria 7: Comparação/Vs
comparacao = [
    ("Você faz assim OU assim?", "Escolha, identificação"),
    ("O jeito CERTO vs o jeito ERRADO", "Educação, comparação"),
    ("Antes eu fazia assim... Hoje faço ASSIM", "Evolução, aprendizado"),
    ("Rico faz assim, pobre faz assim (adaptar ao nicho)", "Polêmica, discussão"),
    ("Profissional vs Amador", "Comparação, aspiração"),
]

# Categoria 8: História/Storytelling
historia = [
    ("Deixa eu te contar uma história...", "Storytelling, conexão"),
    ("Eu nunca vou esquecer o dia que...", "História pessoal, lição"),
    ("Era uma vez... (no meu caso foi assim)", "Narrativa, jornada"),
    ("Lembro como se fosse hoje...", "Memória, emoção"),
    ("A história que mudou tudo", "Transformação, inspiração"),
]

# Categoria 9: Pergunta/Reflexão
pergunta = [
    ("Você já parou pra pensar nisso?", "Reflexão, profundidade"),
    ("Por que [situação] acontece?", "Explicação, educação"),
    ("Qual o seu maior desafio com [tema]?", "Pesquisa, conexão"),
    ("Me responde com sinceridade...", "Intimidade, conexão"),
    ("Se pudesse voltar no tempo, você...?", "Reflexão, arrependimento"),
]

# Categoria 10: Autoridade/Prova
autoridade = [
    ("Depois de [X anos/meses] fazendo isso...", "Experiência, autoridade"),
    ("Testei TUDO e só isso funcionou", "Prova, método validado"),
    ("A ciência comprova: [afirmação]", "Embasamento, educação"),
    ("Isso que vou te contar NINGUÉM sabe", "Exclusividade, autoridade"),
    ("Como profissional, eu te garanto...", "Credibilidade, confiança"),
]

# Preencher dicionário
for categoria, hooks in [
    ("Curiosidade/Segredo", curiosidade),
    ("Urgência/Alerta", urgencia),
    ("Transformação/Resultado", transformacao),
    ("Identificação/Empatia", identificacao),
    ("Lista/Número", listas),
    ("Desafio/Ação", desafio),
    ("Comparação/Vs", comparacao),
    ("História/Storytelling", historia),
    ("Pergunta/Reflexão", pergunta),
    ("Autoridade/Prova", autoridade),
]:
    for gancho, quando in hooks:
        ganchos_virais["Categoria"].append(categoria)
        ganchos_virais["Gancho"].append(gancho)
        ganchos_virais["Quando Usar"].append(quando)

df_ganchos = pd.DataFrame(ganchos_virais)
df_ganchos.to_csv("50_ganchos_virais_instagram.csv", index=False, encoding='utf-8-sig')

print("Lista de 50 ganchos virais criada!")
print(f"\nTotal de ganchos: {len(df_ganchos)}")
print(f"\nCategorias disponíveis:")
for cat in df_ganchos['Categoria'].unique():
    qtd = len(df_ganchos[df_ganchos['Categoria'] == cat])
    print(f"  • {cat}: {qtd} ganchos")
