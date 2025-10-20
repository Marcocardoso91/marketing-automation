"""
Testes de Carga com Locust
Simula múltiplos usuários acessando a API simultaneamente
"""

from locust import HttpUser, task, between
import random

class FacebookAdsAPIUser(HttpUser):
    """Simula usuário fazendo requisições à API"""

    wait_time = between(1, 3)  # Espera entre 1-3 segundos entre requests

    def on_start(self):
        """Executado quando o usuário inicia"""
        # Simular login/autenticação se necessário
        pass

    @task(3)
    def get_campaigns(self):
        """Buscar campanhas (tarefa mais comum - peso 3)"""
        statuses = ['ACTIVE', 'PAUSED', 'ALL']
        status = random.choice(statuses)

        self.client.get(
            f"/api/v1/campaigns",
            params={'status': status, 'limit': 50},
            name="/api/v1/campaigns"
        )

    @task(2)
    def get_campaign_insights(self):
        """Buscar insights de campanha (peso 2)"""
        campaign_ids = ['123456', '789012', '345678']
        campaign_id = random.choice(campaign_ids)
        date_presets = ['last_7d', 'last_14d', 'last_30d']
        date_preset = random.choice(date_presets)

        self.client.get(
            f"/api/v1/campaigns/{campaign_id}/insights",
            params={'date_preset': date_preset},
            name="/api/v1/campaigns/:id/insights"
        )

    @task(2)
    def get_analytics_dashboard(self):
        """Acessar dashboard (peso 2)"""
        self.client.get(
            "/api/v1/analytics/dashboard",
            name="/api/v1/analytics/dashboard"
        )

    @task(1)
    def get_performance_analysis(self):
        """Análise de performance (peso 1 - mais pesada)"""
        self.client.get(
            "/api/v1/analytics/performance",
            params={'limit': 10},
            name="/api/v1/analytics/performance"
        )

    @task(1)
    def chat_query(self):
        """Consulta via chat (peso 1)"""
        queries = [
            "Liste campanhas ativas",
            "Como está a performance?",
            "Quanto gastei hoje?",
            "Quais campanhas têm CTR baixo?"
        ]
        query = random.choice(queries)

        self.client.post(
            "/api/v1/chat",
            json={'message': query},
            name="/api/v1/chat"
        )

    @task(1)
    def health_check(self):
        """Health check (peso 1)"""
        self.client.get("/health", name="/health")

# Executar: locust -f scripts/locustfile.py --host=http://localhost:8000
