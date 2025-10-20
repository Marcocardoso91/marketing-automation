
# Criar guia de cenários e configurações técnicas para gravação

cenarios_gravacao = {
    "Tipo de Vídeo": [
        "Reel Transformação",
        "Reel Autocuidado/Espelho",
        "Reel Reflexão/Externo",
        "Reel Tutorial",
        "Reel Storytelling",
        "Reel Tendência/Dança",
        "Stories Rotina",
        "Stories Tutorial",
        "Carrossel Educativo",
        "Reel Antes/Depois"
    ],
    "Cenário Ideal": [
        "Luz natural (janela) + fundo neutro/clean",
        "Espelho com boa iluminação frontal + ambiente organizado",
        "Área externa com luz dourada (fim de tarde) ou sombra clara",
        "Mesa ou bancada com produtos visíveis + fundo clean",
        "Ambiente aconchegante (sofá, poltrona) + luz suave",
        "Parede lisa neutra (branca, bege) com iluminação uniforme",
        "Ambiente real (quarto, cozinha) + luz natural",
        "Close-up com luz direta + fundo desfocado",
        "Mesa ou prancheta + luz lateral para evitar sombra",
        "Mesmo cenário para antes/depois + mesma luz e ângulo"
    ],
    "Iluminação": [
        "Ring light ou janela lateral (10h-15h)",
        "Ring light frontal + luz ambiente",
        "Golden hour (16h-18h) ou luz difusa (nublado)",
        "Ring light + luz de cima para evitar sombras nos produtos",
        "Luz suave indireta (abajur ou janela com cortina)",
        "Ring light ou softbox frontal + luz de fundo",
        "Luz natural sem necessidade de extra",
        "Ring light próxima ou luz natural forte",
        "Luz uniforme (overhead ou janela lateral)",
        "Mesma iluminação nos 2 momentos (crucial!)"
    ],
    "Equipamento": [
        "Celular com tripé + ring light 10' ou 12'",
        "Celular na mão ou tripé pequeno",
        "Celular com tripé alto + estabilizador (opcional)",
        "Celular com tripé de mesa",
        "Celular com tripé + microfone de lapela (opcional)",
        "Celular com tripé + controle remoto",
        "Celular na mão",
        "Celular com tripé de mesa ou apoio",
        "Celular para fotos ou scanner de documentos",
        "Celular com tripé FIXO (não mover!)"
    ],
    "Ângulo da Câmera": [
        "Altura dos olhos ou ligeiramente acima (5-10cm)",
        "Frontal na altura do rosto",
        "Altura dos olhos ou ligeiramente abaixo (dramático)",
        "Top-down (90°) ou 45° frontal",
        "Altura dos olhos (conversacional)",
        "Centralizado na altura do peito",
        "Natural (altura dos olhos)",
        "Close (45° frontal ou top-down)",
        "90° de cima (flat lay)",
        "EXATAMENTE o mesmo ângulo e distância"
    ],
    "Formato Vídeo": [
        "9:16 vertical",
        "9:16 vertical",
        "9:16 vertical",
        "9:16 vertical ou 1:1",
        "9:16 vertical",
        "9:16 vertical",
        "9:16 vertical",
        "9:16 vertical",
        "1:1 quadrado ou 4:5",
        "9:16 vertical"
    ],
    "Duração Recomendada": [
        "10-15 seg",
        "10-13 seg",
        "12-18 seg",
        "15-25 seg",
        "18-30 seg",
        "7-15 seg",
        "3-7 seg cada card",
        "5-10 seg cada card",
        "5-7 slides",
        "8-12 seg"
    ],
    "Dicas Extras": [
        "Transição suave (dissolve) entre antes/depois",
        "Mostrar gesto natural (ajeitar cabelo, sorriso)",
        "Movimento lento (caminhada, vento no cabelo)",
        "Hands-on: mostrar AS MÃOS fazendo o processo",
        "Olhar para a câmera (intimidade) + pausas dramáticas",
        "Sincronia perfeita com o áudio (marcar batidas)",
        "Movimento natural, sem encenação",
        "Foco no processo, não no rosto",
        "Espaço para texto (1/3 superior livre)",
        "Mesma roupa, mesmo horário, mesmo local"
    ]
}

df_cenarios = pd.DataFrame(cenarios_gravacao)
df_cenarios.to_csv("guia_cenarios_gravacao.csv", index=False, encoding='utf-8-sig')

print("Guia de cenários e configurações técnicas criado!")
print("\n📹 CONFIGURAÇÕES ESSENCIAIS PARA CADA TIPO:\n")

for i in range(len(cenarios_gravacao["Tipo de Vídeo"])):
    print(f"{'='*70}")
    print(f"🎬 {cenarios_gravacao['Tipo de Vídeo'][i].upper()}")
    print(f"{'='*70}")
    print(f"📍 Cenário: {cenarios_gravacao['Cenário Ideal'][i]}")
    print(f"💡 Luz: {cenarios_gravacao['Iluminação'][i]}")
    print(f"📱 Equipamento: {cenarios_gravacao['Equipamento'][i]}")
    print(f"📐 Ângulo: {cenarios_gravacao['Ângulo da Câmera'][i]}")
    print(f"⏱️ Duração: {cenarios_gravacao['Duração Recomendada'][i]}")
    print(f"💡 Dica: {cenarios_gravacao['Dicas Extras'][i]}")
    print()
    
    if i == 2:  # Parar depois de 3 exemplos para não ficar muito longo
        print(f"\n... (veja o arquivo CSV completo para todas as {len(cenarios_gravacao['Tipo de Vídeo'])} configurações)\n")
        break
