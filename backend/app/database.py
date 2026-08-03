from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from app.config import settings 


from sqlalchemy import create_engine

sync_engine = create_engine(settings.POSTGRES_URL_SYNC,echo=False)
sync_session_local = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

def sync_get_db():
    with sync_session_local() as db:
        try:
            yield db
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()


engine = create_async_engine(settings.POSTGRES_URL, echo=settings.POSTGRES_ECHO)

async_session_local = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session_local() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


