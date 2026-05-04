# notifications_service/services/redis_consumer.py
import redis
import json
import threading
from notifications_service.config import settings

def listen_for_reservations():
    try:
        redis_client = redis.from_url(settings.redis_url)
        pubsub = redis_client.pubsub()
        pubsub.subscribe("reserva.confirmada")

        print("Notifications Service: Listening for reserva.confirmada events...")
        for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                print(f"Notifications Service: Received confirmation for reservation {data.get('reservation_id')}")
                print(f"Simulating email sent to guest {data.get('guest_id')} for room {data.get('room_id')}")
    except Exception as e:
        print(f"Redis consumer error: {e}")

def start_consumer():
    thread = threading.Thread(target=listen_for_reservations, daemon=True)
    thread.start()
