"""
Cliente HTTP para comunicação com facebook-ads-ai-agent API.
Inclui retry logic, timeouts e tratamento de erros.
"""
import requests
import logging
from typing import Dict, Union
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import date as Date

logger = logging.getLogger(__name__)


class AgentAPIError(Exception):
    """Exceção customizada para erros da API"""
    pass


class AgentAPIClient:
    """Cliente HTTP para comunicação com facebook-ads-ai-agent"""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.session = self._create_session(max_retries)

    def _create_session(self, max_retries: int) -> requests.Session:
        """Cria sessão com retry logic"""
        session = requests.Session()

        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,  # 1s, 2s, 4s
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session

    def get_metrics(
        self,
        date_from: Union[str, Date],
        date_until: Union[str, Date]
    ) -> Dict:
        """
        Busca métricas do agent API.

        Args:
            date_from: Data inicial (YYYY-MM-DD ou date object)
            date_until: Data final (YYYY-MM-DD ou date object)

        Returns:
            Dict com dados da resposta

        Raises:
            AgentAPIError: Se houver erro na comunicação ou validação
        """
        # Converter dates para string se necessário
        if isinstance(date_from, Date):
            date_from = date_from.isoformat()
        if isinstance(date_until, Date):
            date_until = date_until.isoformat()

        logger.info(f"Buscando métricas de {date_from} até {date_until}")

        try:
            response = self.session.get(
                f"{self.base_url}/api/v1/metrics/export",
                headers={"X-API-Key": self.api_key},
                params={"date_from": date_from, "date_until": date_until},
                timeout=self.timeout
            )

            response.raise_for_status()
            data = response.json()

            logger.info(
                f"✅ Recebidas {data.get('total_campaigns', 0)} campanhas")
            return data

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AgentAPIError("API key inválida ou expirada")
            elif e.response.status_code == 429:
                raise AgentAPIError(
                    "Rate limit excedido. Tente novamente em alguns minutos")
            else:
                raise AgentAPIError(
                    f"Erro HTTP {e.response.status_code}: {e.response.text}")

        except requests.exceptions.Timeout:
            raise AgentAPIError(
                f"Timeout após {self.timeout}s. Servidor pode estar sobrecarregado")

        except requests.exceptions.ConnectionError:
            raise AgentAPIError(
                f"Erro de conexão. Verifique se o servidor está rodando em {self.base_url}")

        except Exception as e:
            raise AgentAPIError(f"Erro inesperado: {str(e)}")

    def health_check(self) -> bool:
        """
        Verifica se API está saudável.

        Returns:
            True se API está respondendo, False caso contrário
        """
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
