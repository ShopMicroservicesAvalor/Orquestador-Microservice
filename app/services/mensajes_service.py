import json
import pika
from sqlalchemy.orm import Session
from fastapi import Depends
from dependencies import get_db
from services.producto_service import get_all_productos


async def procesar_mensaje(
    channel, method, properties, body, db: Session = Depends(get_db)
):
    """
    Procesa los mensajes recibidos de RabbitMQ
    """
    try:
        mensaje = json.loads(body)
        print(f"Mensaje recibido: {mensaje}")

        if mensaje.get("accion") == "listar_productos":
            productos = await get_all_productos(
                db,
                skip=mensaje.get("skip", 0),
                limit=mensaje.get("limit", 100),
                activo=mensaje.get("activo", None),
            )

            resultado = [
                {
                    "id": str(p.id),
                    "nombre": p.nombre,
                    "precio": p.precio,
                    "stock": p.stock,
                    "activo": p.activo,
                    "created_at": p.created_at.isoformat(),
                    "updated_at": p.updated_at.isoformat(),
                }
                for p in productos
            ]

            print(f"Productos encontrados: {len(resultado)}")

            if properties.reply_to:
                channel.basic_publish(
                    exchange="",
                    routing_key=properties.reply_to,
                    properties=pika.BasicProperties(
                        correlation_id=properties.correlation_id
                    ),
                    body=json.dumps({"status": "success", "data": resultado}),
                )

        channel.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error procesando mensaje: {str(e)}")
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
