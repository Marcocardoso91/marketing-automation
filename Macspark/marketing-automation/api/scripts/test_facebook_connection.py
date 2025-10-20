#!/usr/bin/env python3
from src.agents.facebook_agent import FacebookAdsAgent
import asyncio
import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Carregar .env
env_file = project_root / ".env"
if env_file.exists():
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value


async def test():
    print("Testando conexão com Facebook API...")

    agent = FacebookAdsAgent()

    # Testar listagem de campanhas
    campaigns = await agent.get_campaigns()
    print(f"[OK] Encontradas {len(campaigns)} campanhas")

    if campaigns:
        # Testar insights da primeira campanha
        first = campaigns[0]
        print(f"Campanha: {first['name']} (ID: {first['id']})")

        insights = await agent.get_campaign_insights(first['id'])
        if insights:
            print(
                f"[OK] Insights: CTR={insights.get('ctr')}%, CPA=R${insights.get('cpa')}")

    print("[OK] Facebook API funcionando!")

if __name__ == "__main__":
    asyncio.run(test())
