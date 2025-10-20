#!/usr/bin/env python3
"""
YouTube Metrics Collector
Coleta métricas do YouTube via Data API v3 e Analytics API
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List


class YouTubeCollector:
    """Coletor de métricas do YouTube"""

    def __init__(self):
        self.channel_id = os.getenv("YOUTUBE_CHANNEL_ID")
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.data_api_url = "https://www.googleapis.com/youtube/v3"
        self.analytics_api_url = "https://youtubeanalytics.googleapis.com/v2"

    def get_channel_statistics(self) -> Optional[Dict[str, Any]]:
        """
        Buscar estatísticas gerais do canal
        Usa YouTube Data API v3 (requer apenas API Key)
        """
        if not self.channel_id or not self.api_key:
            print("⚠️  YouTube: Credenciais não configuradas")
            return None

        print("🔄 Buscando estatísticas do canal YouTube...")

        url = f"{self.data_api_url}/channels"
        params = {
            "part": "statistics,snippet",
            "id": self.channel_id,
            "key": self.api_key
        }

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if data.get("items"):
                    item = data["items"][0]
                    stats = item["statistics"]
                    snippet = item["snippet"]

                    result = {
                        "channel_title": snippet.get("title"),
                        "subscriber_count": int(stats.get("subscriberCount", 0)),
                        "view_count": int(stats.get("viewCount", 0)),
                        "video_count": int(stats.get("videoCount", 0)),
                        "hidden_subscriber_count": stats.get("hiddenSubscriberCount", False)
                    }

                    print(f"✅ YouTube: {result['subscriber_count']:,} inscritos, {result['view_count']:,} views totais")
                    return result
                else:
                    print("❌ YouTube: Canal não encontrado")
                    return None
            else:
                error_data = response.json()
                print(f"❌ YouTube Error: {error_data.get('error', {}).get('message', 'Unknown')}")
                return None

        except Exception as e:
            print(f"❌ YouTube Exception: {str(e)}")
            return None

    def get_recent_videos(self, max_results: int = 5) -> Optional[List[Dict[str, Any]]]:
        """
        Buscar vídeos recentes do canal
        """
        if not self.channel_id or not self.api_key:
            return None

        url = f"{self.data_api_url}/search"
        params = {
            "part": "snippet",
            "channelId": self.channel_id,
            "order": "date",
            "type": "video",
            "maxResults": max_results,
            "key": self.api_key
        }

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                videos = []

                for item in data.get("items", []):
                    videos.append({
                        "video_id": item["id"]["videoId"],
                        "title": item["snippet"]["title"],
                        "published_at": item["snippet"]["publishedAt"]
                    })

                return videos
            else:
                return None

        except Exception as e:
            print(f"❌ YouTube Videos Exception: {str(e)}")
            return None

    def get_video_statistics(self, video_ids: List[str]) -> Optional[Dict[str, Any]]:
        """
        Buscar estatísticas de vídeos específicos
        """
        if not video_ids or not self.api_key:
            return None

        url = f"{self.data_api_url}/videos"
        params = {
            "part": "statistics",
            "id": ",".join(video_ids),
            "key": self.api_key
        }

        try:
            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                total_views = 0
                total_likes = 0
                total_comments = 0

                for item in data.get("items", []):
                    stats = item["statistics"]
                    total_views += int(stats.get("viewCount", 0))
                    total_likes += int(stats.get("likeCount", 0))
                    total_comments += int(stats.get("commentCount", 0))

                return {
                    "total_views": total_views,
                    "total_likes": total_likes,
                    "total_comments": total_comments,
                    "video_count": len(data.get("items", []))
                }
            else:
                return None

        except Exception as e:
            print(f"❌ YouTube Video Stats Exception: {str(e)}")
            return None

    def estimate_daily_metrics(self, channel_stats: Dict[str, Any], recent_videos: Optional[List[Dict]]) -> Dict[str, Any]:
        """
        Estimar métricas diárias baseado em estatísticas do canal
        Nota: YouTube Data API v3 não fornece métricas diárias precisas
        Para dados precisos, use YouTube Analytics API (requer OAuth 2.0)
        """
        view_count = channel_stats.get("view_count", 0)
        subscriber_count = channel_stats.get("subscriber_count", 0)

        # Estimativa conservadora: 0.5% das views totais ocorreram ontem
        estimated_daily_views = round(view_count * 0.005)

        # Estimativa: 0.05% dos inscritos totais ocorreram ontem
        estimated_daily_subscribers = round(subscriber_count * 0.0005)

        # Se temos vídeos recentes (últimos 7 dias), fazer estimativa melhor
        if recent_videos:
            recent_video_ids = [v["video_id"] for v in recent_videos]
            video_stats = self.get_video_statistics(recent_video_ids)

            if video_stats:
                # Média de views por dia dos vídeos recentes
                days_period = 7
                estimated_daily_views = max(
                    estimated_daily_views,
                    round(video_stats["total_views"] / days_period)
                )

        return {
            "estimated_views": estimated_daily_views,
            "estimated_subscribers": estimated_daily_subscribers,
            "estimated_watch_time_hours": round(estimated_daily_views * 0.05),  # Assumindo 3min/view
            "total_subscribers": subscriber_count,
            "total_videos": channel_stats.get("video_count", 0)
        }

    def process_metrics(self, channel_stats: Optional[Dict], daily_estimates: Optional[Dict]) -> Optional[Dict[str, Any]]:
        """Processar métricas do YouTube"""
        if not channel_stats:
            return None

        yesterday = datetime.now() - timedelta(days=1)

        estimated = daily_estimates or {}

        return {
            "data": yesterday.strftime("%Y-%m-%d"),
            "source": "youtube",
            "spend": 0.0,  # Orgânico (sem gastos)
            "reach": estimated.get("estimated_views", 0),
            "impressions": estimated.get("estimated_views", 0),
            "views": estimated.get("estimated_views", 0),
            "subscribers_gained": estimated.get("estimated_subscribers", 0),
            "new_followers": estimated.get("estimated_subscribers", 0),
            "watch_time_hours": estimated.get("estimated_watch_time_hours", 0),
            "notes": (
                f"YouTube: ~{estimated.get('estimated_views', 0):,} views estimadas ontem, "
                f"{channel_stats.get('subscriber_count', 0):,} inscritos totais"
            ),
            "raw_data": {
                "channel_stats": channel_stats,
                "daily_estimates": estimated
            }
        }


def get_youtube_metrics() -> Optional[Dict[str, Any]]:
    """
    Função helper para buscar métricas do YouTube

    Returns:
        Dicionário com métricas processadas ou None
    """
    collector = YouTubeCollector()

    # Buscar estatísticas do canal
    channel_stats = collector.get_channel_statistics()

    if not channel_stats:
        return None

    # Buscar vídeos recentes para melhorar estimativas
    recent_videos = collector.get_recent_videos(max_results=5)

    # Estimar métricas diárias
    daily_estimates = collector.estimate_daily_metrics(channel_stats, recent_videos)

    return collector.process_metrics(channel_stats, daily_estimates)
