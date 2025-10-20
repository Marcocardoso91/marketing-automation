"""
Celery Application Configuration
Background task processing with Celery
"""
from celery import Celery
from celery.schedules import crontab
from src.utils.config import settings

celery_app = Celery(
    'facebook_ads_agent',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

# Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    'collect-metrics-30min': {
        'task': 'src.tasks.collectors.collect_facebook_metrics',
        'schedule': 1800.0,  # Every 30 minutes
    },
    'analyze-performance-hourly': {
        'task': 'src.tasks.processors.analyze_performance',
        'schedule': 3600.0,  # Every hour
    },
    'generate-daily-report': {
        'task': 'src.tasks.processors.generate_daily_report',
        'schedule': crontab(hour=8, minute=0),  # 8am daily
    },
    'cleanup-old-data-weekly': {
        'task': 'src.tasks.processors.cleanup_old_data',
        'schedule': crontab(day_of_week=0, hour=2, minute=0),  # Sunday 2am
    },
}
