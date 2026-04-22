from fastapi import Depends, HTTPException
from http import HTTPStatus
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db, User
from sqlalchemy.orm import sessionmaker
from jose import jwt, JWTError


# Cria e gerencia a sessão com o banco de dados
def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


# Verifica e valida o token JWT
def verify_token(token: str= Depends(oauth2_schema), session=Depends(get_session)):
    try:
        # Decodifica o token e extrai o ID do usuário
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = dic_info.get('sub')

    except JWTError:
        # Token inválido ou expirado
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="ACCESS_DENIED"
            )

    # Busca o usuário no banco com base no ID do token
    user = session.query(User).filter(User.id == int(user_id)).first()

    if not user:
        # Usuário não encontrado no banco
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='5453543534'
            )

    # Retorna o usuário autenticado
    return user
