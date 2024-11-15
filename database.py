from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from config import DBSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import *

 

# engine_e = create_engine(
#     url = DBSettings.DATABSE_URL_psycopg(),
#     echo=True,
#     pool_size=5,
#     max_overflow=10
# )

# with engine_e.connect() as connection:
#     res = connection.execute(text("SELECT VERSION()"))
#     print(f"{res=}")


with DBSettings.get_session() as conn:
    # print([user.name for user in conn.query(User).all()])
    # print([role.name for role in conn.query(Role).all()])
    roleDB = conn.query(Role).filter(Role.name == "admin").first()
    print(roleDB.id)

