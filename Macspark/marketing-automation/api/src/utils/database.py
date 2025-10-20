"""
Setup SQLAlchemy async para PostgreSQL
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.utils.config import settings
from src.utils.exceptions import DatabaseQueryError
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Base declarativa para modelos
Base = declarative_base()

# Engine async
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Session maker async
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def get_async_session() -> AsyncSession:
    """
    Dependency para obter sessão async do banco

    Yields:
        AsyncSession: Sessão do banco de dados
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.error(f"Database session error: {e}")
            #
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Inicializa banco de dados criando todas as tabelas"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Fecha conexões com banco de dados"""
    await engine.dispose()
