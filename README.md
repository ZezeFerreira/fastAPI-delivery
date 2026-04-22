## 🍕 FastAPI Pizza Delivery API

API REST para gerenciamento de pedidos de uma pizzaria, desenvolvida com **FastAPI**, utilizando autenticação JWT e controle de usuários.

---

## 🚀 Tecnologias

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT (JSON Web Token)
- Passlib (bcrypt)
- Alembic (migrations)

---

## 📌 Funcionalidades

- Cadastro de usuários  
- Autenticação com JWT (access e refresh token)  
- Criação de pedidos  
- Adição e remoção de itens no pedido  
- Cálculo automático do valor total  
- Cancelamento e finalização de pedidos  
- Controle de acesso (usuário e administrador)  

---

## ⚙️ Como executar o projeto

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/fastapi-delivery-api.git

# Acesse a pasta
cd fastapi-delivery-api

# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente (Windows)
.venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute as migrations
alembic upgrade head

# Inicie a aplicação
uvicorn main:app --reload
```

## 📖 Documentação da API

Após rodar o projeto, acesse:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 📄 Licença
Este projeto está sob a licença MIT.
