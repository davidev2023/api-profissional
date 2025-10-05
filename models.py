from sqlalchemy import Integer, Column, String, Float, DateTime
from database import Base




class Vaga(Base):
    __tablename__='vagas'
    id_vaga = Column(Integer,primary_key=True, index=True, autoincrement= True)
    nome_vaga = Column(String)
    diaria = Column(Float)
    data_inicio = Column(String)
    

