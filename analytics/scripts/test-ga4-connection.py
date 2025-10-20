#!/usr/bin/env python3
"""Testar conexão com Google Analytics 4"""

import os
from typing import Optional
import sys


def test_ga4_connection() -> bool:
    """Testa conexão e coleta básica do GA4"""
    property_id = os.getenv("GA4_PROPERTY_ID")

    if not property_id:
        print("❌ GA4_PROPERTY_ID não configurado no .env")
        return False

    try:
        # Verificar se google-analytics-data está instalado
        try:
            from google.analytics.data_v1beta import BetaAnalyticsDataClient
            from google.analytics.data_v1beta.types import (
                DateRange,
                Dimension,
                Metric,
                RunReportRequest,
            )
        except ImportError:
            print("❌ google-analytics-data não instalado")
            print("Execute: pip install google-analytics-data google-auth")
            return False

        # Inicializar cliente
        client = BetaAnalyticsDataClient()

        # Request básico: usuários dos últimos 7 dias
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="date")],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="sessions"),
            ],
            date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
        )

        # Executar
        response = client.run_report(request)

        # Mostrar resultados
        print("✅ Conexão GA4 OK!")
        print(f"\n📊 Dados coletados dos últimos 7 dias:")

        for row in response.rows:
            date = row.dimension_values[0].value
            users = row.metric_values[0].value
            sessions = row.metric_values[1].value
            print(f"   {date}: {users} usuários, {sessions} sessões")

        return True

    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_ga4_connection()
    sys.exit(0 if success else 1)
