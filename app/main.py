from fastapi import FastAPI
import threading
from services.consumer_services import consumir_mensajes

app = FastAPI(title="Productos Microservice", version="1.0.0")


@app.on_event("startup")
async def startup_event():
    """
    Se ejecuta al iniciar la aplicación
    """
    print("🚀 Iniciando Productos Microservice...")
    # Iniciar consumidor en un hilo separado
    consumidor_thread = threading.Thread(target=consumir_mensajes)
    consumidor_thread.daemon = True
    consumidor_thread.start()


@app.get("/health")
async def health_check():
    """
    Endpoint para verificar que la app está viva
    """
    return {"status": "healthy", "service": "productos-microservice"}


if __name__ == "__main__":
    import uvicorn

    print("🌐 Iniciando servidor FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
