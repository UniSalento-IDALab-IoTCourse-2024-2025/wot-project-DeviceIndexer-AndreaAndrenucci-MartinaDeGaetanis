import json
import paho.mqtt.client as mqtt
from models.domain.air_quality_measurement import AirQualityMeasurement
from models.domain.device import Device
from repositories.measurement_repository import PollutionMeasurementsRepository
from repositories.devices_repository import DeviceRepository

'''
    Subscriber MQTT che prende i dati dai topic
    e li salva nel DB con expire di 50 minuti

    Si occupa solo e soltanto di salvare i dati.
'''

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883


MQTT_TOPICS = [
    ("digitair/devices", 0),
    ("digitair/devices/heartbeat", 0),
    ("digitair/measurements", 0),
]

measurementsRepository = PollutionMeasurementsRepository()
devicesRepository = DeviceRepository()

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("[MQTT] Connesso al broker")
        client.subscribe(MQTT_TOPICS)
        print("[MQTT] Sottoscritto ai topic:")
        for t, _ in MQTT_TOPICS:
            print(f"   - {t}")
    else:
        print(f"[MQTT] Connessione fallita, codice: {rc}")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print(f"\n[MQTT] Messaggio ricevuto su {msg.topic}: {payload}")

    if msg.topic == "digitair/measurements":
        handleAirQualityTopic(payload)

    elif msg.topic == "digitair/devices":
        handleDeviceRegistration(payload)

    elif msg.topic == "digitair/devices/heartbeat":
        handleDeviceHeartbeat(payload)
    # TODO sostituire con try catch
    # try:
    #     payload = msg.payload.decode("utf-8")
    #     print(f"\n[MQTT] Messaggio ricevuto su {msg.topic}: {payload}")

    #     if msg.topic == "digitair/measurements":
    #         handleAirQualityTopic(payload)

    #     elif msg.topic == "digitair/devices":
    #         handleDeviceRegistration(payload)

    #     elif msg.topic == "digitair/devices/heartbeat":
    #         handleDeviceHeartbeat()

    # except Exception as e:
    #     print(f"[ERRORE] Impossibile decodificare il messaggio: {e}")


def handleAirQualityTopic(payload):
    data = json.loads(payload)

    if isinstance(data, dict):
        measurements = [AirQualityMeasurement.from_dict(data)]
    elif isinstance(data, list):
        measurements = [AirQualityMeasurement.from_dict(measure) for measure in data]
    else:
        print("[ERRORE] Formato JSON non valido:", type(data))
        return

    measurementsRepository.save_all(measurements)

def handleDeviceRegistration(payload):
    data = json.loads(payload)
    print("[RECIVED DEVICE]", data)
    device = Device.from_dict(data)
    devicesRepository.saveWithOverwrite(device)

def handleDeviceHeartbeat(payload):
    print("MESSAGGIO SU HEARTBEAT")
    data = json.loads(payload)
    if(not data.get("status")):
        device = devicesRepository.find_by_device_id(data.get("device_id"))
        device.status = False
        devicesRepository.saveWithOverwrite(device)



if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"[MQTT] Connessione a {MQTT_BROKER}:{MQTT_PORT} ...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()
