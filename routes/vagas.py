from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from database import SessionLocal
from sqlalchemy.orm import Session
from models import Vaga
from schemas import VagaCreate, VagaResponse

router = APIRouter(prefix='/vagas', tags=['vagas'])

#Função para criar e fechar a sessão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

# -------------------- LISTAR TODAS AS VAGAS --------------------
@router.get('/' ,status_code=status.HTTP_200_OK )
async def listar_vagas(db: Session = Depends(get_db)):
    vaga = db.query(Vaga).all()
    return vaga
# -------------------- BUSCAR VAGA POR ID --------------------
@router.get('/{id_vaga}', status_code=status.HTTP_200_OK)
async def vagas_id(id_vaga: int, db: Session = Depends(get_db)):
    vaga = db.query(Vaga).filter(Vaga.id_vaga == id_vaga).first() # type: ignore
    if not vaga:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vaga nao encontrada')
    return vaga

# -------------------- CRIAR NOVA VAGA --------------------
@router.post('/', response_model=VagaResponse, status_code=status.HTTP_201_CREATED)
async def criar_vaga(vaga: VagaCreate, db: Session = Depends(get_db)):
    nova_vaga = Vaga(nome_vaga= vaga.nome_vaga, diaria=vaga.diaria, data_inicio=vaga.data_inicio)
    db.add(nova_vaga) #vai adicionar uma nova vaga no banco de dados
    db.commit() # confirma a transação
    db.refresh(nova_vaga) # atualiza com o ID gerado no banco

    return nova_vaga

# -------------------- ATUALIZAR VAGA (PUT) --------------------
@router.put("/{id_vaga}", response_model=VagaResponse, status_code=status.HTTP_200_OK)
async def atualizar_vaga(id_vaga: int, vaga_atualizada: VagaCreate, db: Session = Depends(get_db)):
    vaga = db.query(Vaga).filter(Vaga.id_vaga == id_vaga).first()

    if not vaga:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vaga não encontrada")

    setattr(vaga, "nome_vaga", vaga_atualizada.nome_vaga)
    setattr(vaga, "diaria", vaga_atualizada.diaria)
    setattr(vaga, "data_inicio", vaga_atualizada.data_inicio)

    db.commit()
    db.refresh(vaga)
    return vaga

# -------------------- DELETAR VAGA --------------------
@router.delete("/{id_vaga}", status_code=status.HTTP_200_OK)
async def deletar_vaga(id_vaga: int, db: Session = Depends(get_db)):
    vaga = db.query(Vaga).filter(Vaga.id_vaga == id_vaga).first()

    if not vaga:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vaga não encontrada")

    db.delete(vaga)
    db.commit()
    return {"mensagem": "Vaga deletada com sucesso!"}

@router.post('/lotes', response_model=VagaResponse, status_code=status.HTTP_201_CREATED)
async def criar_vagas_lotes(vagas: List[VagaCreate], db: Session = Depends(get_db)):
    try:
        lista = [Vaga(**vaga.model_dump()) for vaga in vagas]
        db.add_all(lista)
        db.commit()  # <-- corrigido
        return {"mensagem": f"{len(vagas)} vagas criadas com sucesso"}
    except Exception as e:
        db.rollback()
        return {"erro": f"Falha ao inserir vagas: {str(e)}"}