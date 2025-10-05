from fastapi import FastAPI, APIRouter, status
#from database import Base, engine
from routes import vagas
import uvicorn
from schemas import Msg


app = FastAPI(title='Api Vagas')

@app.get('/',status_code=status.HTTP_200_OK,response_model=Msg)
async def home():
    return {'message': 'Bem Vindo'}

app.include_router(vagas.router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=3443, reload=True)