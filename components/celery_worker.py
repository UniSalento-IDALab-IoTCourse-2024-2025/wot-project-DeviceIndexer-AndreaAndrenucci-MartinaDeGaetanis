from celery import Celery
from models.dto import MeasurementsMessageDTO
from celery.schedules import crontab
from repositories.measurement_repository import PollutionMeasurementsRepository
import json

NEW_MEASUREMENT_QUEUE = "new-measurement-queue"

celery_app = Celery(
    "sender",
    broker="amqp://guest:guest@rabbitmq:5672//"
)

repo = PollutionMeasurementsRepository()

celery_app.conf.beat_schedule = {
    "send-measurements-every-hour-55": {
        "task": "tasks.send_measurements_task",
        "schedule": crontab(minute=47),
    }
}

celery_app.conf.timezone = "UTC"  



def send_new_measurement(body: MeasurementsMessageDTO):
    try:
        celery_app.send_task("process_message", args=[body], queue=NEW_MEASUREMENT_QUEUE)
    except Exception as e:
        print(f"Invio non riuscito con errore {e}")


@celery_app.task(name="tasks.send_measurements_task")
def send_measurements_task():
    """
    Task schedulato da Celery Beat ogni ora alle XX:55.
    Recupera i dati dell'ultima ora e li invia alla coda AMQP.
    """
    measurements = repo.find_all_measurements()

    dto = MeasurementsMessageDTO.from_measurements(measurements)

    payload = [m.to_dict() for m in dto.measurements]
    

    print("[[PAYLOAD]]",payload.__str__())

    celery_app.send_task(
        "process_message",
        args=[json.dumps(payload)],
        queue=NEW_MEASUREMENT_QUEUE,
    )

    print("[TASK] Misurazioni inviate su AMQP!")
    # try:


    #     if measurements:
    #     else:
    #         print("[TASK] Nessuna misurazione da inviare.")

    # except Exception as e:
    #     print(f"[ERRORE] Impossibile inviare misurazioni: {e}")