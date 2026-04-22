from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações de segurança e autenticação
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

# Inicializa a aplicação FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuração de criptografia para senhas
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Define o esquema OAuth2 para autenticação via token
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

# Importação das rotas
from routes.auth_routes import auth_router
from routes.order_routes import order_router
from routes.product_route import product_router

# Registro das rotas na aplicação
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(product_router)
