from pydantic import BaseModel


class Msg(BaseModel):
    message: str
    class Config:
        from_attributes = True

class VagaResponse(BaseModel):
    id_vaga: int
    nome_vaga: str
    diaria: float
    data_inicio:str   
    



class VagaCreate(BaseModel):
    nome_vaga: str
    diaria: float
    data_inicio:str 



