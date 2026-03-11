import pika
from .mensajes_service import procesar_mensaje
import time
from dependencies import get_rabbitmq_config


def consumir_mensajes():
    """
    Inicia el consumidor de RabbitMQ
    """
    while True:  # Bucle infinito para reconexión automática
        try:
            config = get_rabbitmq_config()
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=config["host"],
                    port=config["port"],
                    credentials=pika.PlainCredentials(
                        config["user"], config["password"]
                    ),
                    heartbeat=600,
                    blocked_connection_timeout=300,
                )
            )
            channel = connection.channel()

            # Declarar cola
            channel.queue_declare(queue="productos_queue", durable=True)

            # Configurar consumidor
            channel.basic_consume(
                queue="productos_queue", on_message_callback=procesar_mensaje
            )

            print("✅ Conectado a RabbitMQ - Esperando mensajes...")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("❌ Conexión a RabbitMQ perdida. Reintentando en 5 segundos...")
            time.sleep(5)
        except Exception as e:
            print(f"❌ Error en RabbitMQ: {str(e)}")
            time.sleep(5)
