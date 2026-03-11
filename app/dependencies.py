from db.database import SessionLocal
from core.config import settings


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apartado de la configuracion de rabbitmq
def get_rabbitmq_config():

    print("Configurando rabbitmq")
    print("User:", settings.rabbitmq_user)
    print("Password:", settings.rabbitmq_pass)
    return {
        "host": "localhost",
        "port": 5673,
        "user": settings.rabbitmq_user,
        "password": settings.rabbitmq_pass,
    }
