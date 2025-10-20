
# Criar planilha de controle de métricas e KPIs

metricas_controle = {
    "Métrica": [
        "CTR (Taxa de Cliques)",
        "CPC (Custo por Clique)",
        "CPM (Custo por 1000 impressões)",
        "Frequência",
        "Visitas ao Perfil/dia",
        "Novos Seguidores/dia",
        "Taxa de Conversão Perfil→Seguidor",
        "Custo por Seguidor",
        "Engajamento nos Reels (%)",
        "Alcance dos Reels",
        "Salvamentos",
        "Compartilhamentos",
        "Visualizações Stories",
        "Taxa de Retenção Stories (%)",
        "Comentários por Post",
        "Mensagens Diretas"
    ],
    "Meta Mínima": [
        "≥ 1,5%",
        "≤ R$ 0,50",
        "R$ 2,00 - R$ 6,00",
        "< 2,5",
        "≥ 40",
        "≥ 20-30",
        "≥ 10%",
        "≤ R$ 1,30",
        "≥ 3%",
        "≥ 5.000",
        "≥ 50",
        "≥ 20",
        "≥ 15% dos seguidores",
        "≥ 70%",
        "≥ 5",
        "≥ 10"
    ],
    "Meta Ideal": [
        "≥ 2,5%",
        "≤ R$ 0,35",
        "R$ 2,00 - R$ 4,00",
        "< 2,0",
        "≥ 60",
        "≥ 40-50",
        "≥ 15%",
        "≤ R$ 1,00",
        "≥ 5%",
        "≥ 10.000",
        "≥ 100",
        "≥ 50",
        "≥ 20% dos seguidores",
        "≥ 80%",
        "≥ 10",
        "≥ 20"
    ],
    "Frequência Monitoramento": [
        "Diário (18h)",
        "Diário (18h)",
        "Diário (18h)",
        "Diário (18h)",
        "A cada 3 dias",
        "A cada 3 dias",
        "Semanal",
        "Semanal",
        "Por post",
        "Por post",
        "Por post",
        "Por post",
        "Diário",
        "Diário",
        "Por post",
        "Diário"
    ],
    "Ferramenta": [
        "Meta Ads Manager",
        "Meta Ads Manager",
        "Meta Ads Manager",
        "Meta Ads Manager",
        "Instagram Insights",
        "Instagram Insights",
        "Instagram Insights",
        "Meta Ads Manager",
        "Instagram Insights",
        "Instagram Insights",
        "Instagram Insights",
        "Instagram Insights",
        "Instagram Insights",
        "Instagram Insights",
        "Instagram Insights",
        "Instagram Direct"
    ]
}

df_metricas = pd.DataFrame(metricas_controle)
df_metricas.to_csv("controle_metricas_kpis.csv", index=False, encoding='utf-8-sig')

print("Planilha de controle de métricas criada!")
print("\nMétricas principais para monitorar:")
for i, metrica in enumerate(metricas_controle["Métrica"][:8]):
    print(f"  {i+1}. {metrica}: {metricas_controle['Meta Ideal'][i]}")
