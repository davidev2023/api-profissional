from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine('postgresql://vagas_ysqy_user:l2xODoTlGZ31TOrqEU9kgqKx4JKit26A@dpg-d3grpqbipnbc7385ge10-a.oregon-postgres.render.com:5432/vagas_ysqy')
SessionLocal = sessionmaker(autocommit=False ,autoflush=False, bind = engine )

Base = declarative_base()