import requests
import os

# Carregar .env
with open(".env", "r") as f:
    for line in f:
        if "=" in line and not line.startswith("#"):
            key, value = line.strip().split("=", 1)
            os.environ[key] = value

# Testar Facebook API
token = os.getenv("FACEBOOK_ACCESS_TOKEN")
account_id = os.getenv("FACEBOOK_AD_ACCOUNT_ID")

print("🔍 Testando credenciais do Facebook...")
print(f"Token encontrado: {'✅' if token else '❌'}")
print(f"Account ID encontrado: {'✅' if account_id else '❌'}")

if token and account_id:
    print(f"\n📊 Testando API com Account ID: {account_id}")

    # Testar endpoint de campanhas
    url = f"https://graph.facebook.com/v21.0/{account_id}/campaigns"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ Conexão com Facebook API funcionando!")
            print(f"Campanhas encontradas: {len(data.get('data', []))}")
            if data.get('data'):
                print(
                    f"Primeira campanha: {data['data'][0].get('name', 'N/A')}")
        else:
            print(f"❌ Erro na API: {response.text}")

    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
else:
    print("❌ Credenciais não encontradas no .env")
    print("Verifique se o arquivo .env contém:")
    print("- FACEBOOK_ACCESS_TOKEN")
    print("- FACEBOOK_AD_ACCOUNT_ID")
