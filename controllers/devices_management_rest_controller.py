from flask import Blueprint, request, jsonify
from models.dto import DeviceDto, DeviceResponseDto
from models.domain.device import Device
from repositories.devices_repository import DeviceRepository
import json
import requests as http_request
from components.celery_worker import send_new_measurement, send_measurements_task
from utils.token_utils import get_auth_params

devices_bp = Blueprint("devices", __name__)
devices_repository = DeviceRepository()


@devices_bp.route("/devices/<device_id>", methods=["GET"])
def get_device_infos(device_id):
    token = get_auth_params(request)
    if not token.get("role") == "ADMIN" :
        return jsonify({"msg":"Token non valido"}), 403
    try:
        device = devices_repository.find_by_device_id(device_id) 
        dto = DeviceDto.from_domain(device)
        return jsonify(DeviceResponseDto(response=0, message="Info recuperate", payload=dto).to_dict()), 201
    except Exception as e:
        return jsonify(DeviceResponseDto(response=1, message=f"Errore nella get: {e}").to_dict()), 500



@devices_bp.route("/devices", methods=["GET"])
def get_all_devices():
    token = get_auth_params(request)
    if not token.get("role") == "ADMIN" :
        return jsonify({"msg":"Token non valido"}), 403
    
    try:
        devices = devices_repository.find_all()  # lista di Device
        dto = [DeviceDto.from_domain(device) for device in devices]  # lista di DeviceDto

        return jsonify(DeviceResponseDto(
            response=0,
            message="Info recuperate",
            payload=dto
        ).to_dict()), 200

    except Exception as e:
        return jsonify(DeviceResponseDto(
            response=1,
            message=f"Errore nel recupero: {e}",
            payload=[]
        ).to_dict()), 500


@devices_bp.route("/devices", methods=["POST"])
def add_device(): 
    

    try:
        data = request.get_json()
        dto = DeviceDto.from_dict(data)
        domain_model = dto.to_domain()
        devices_repository.save(domain_model) 
        return jsonify(DeviceResponseDto(response=0, message="Salvataggio effettuato correttamente").to_dict()), 201
    except Exception as e:
        return jsonify(DeviceResponseDto(response=1, message=f"Errore nel salvataggio: {e}").to_dict()), 500



@devices_bp.route("/devices/<device_id>", methods=["DELETE"])
def delete_device(device_id):
    token = get_auth_params(request)
    if not token.get("role") == "ADMIN" :
        return jsonify({"msg":"Token non valido"}), 403
    try:
        device: Device = devices_repository.find_by_device_id(device_id)
        if not device:
            return jsonify(DeviceResponseDto(response=1, message="Device non trovato").to_dict()), 404

        url = f"http://{device.ipv4}:80/wifi/options"
        payload = {"message": "disconnect"}

        try:
            response = http_request.post(url, json=payload, timeout=5)
        except http_request.RequestException as e:
            return jsonify(DeviceResponseDto(response=1, message=f"Errore connessione al device: {e}").to_dict()), 502

        if response.status_code == 200:
            devices_repository.delete_by_id(device_id=device_id)
            return jsonify(DeviceResponseDto(response=0, message="Device disconnesso e cancellato correttamente").to_dict()), 200
        else:
            return jsonify(DeviceResponseDto(response=1, message=f"Errore dal device: {response.status_code} - {response.text}").to_dict()), 502

    except Exception as e:
        return jsonify(DeviceResponseDto(response=1, message=f"Errore interno: {e}").to_dict()), 500



@devices_bp.route("/test/new_measurement_from_device", methods=["POST"])
def new_measurement_from_device():
    try:
        data = request.get_json()
        send_new_measurement(json.dumps(data))
        return jsonify({"status": "Message sent", "message": data})
    except Exception as e:
        return jsonify({"status": "bad", "message": f"{e}"}), 500
        

@devices_bp.route("/test/celery", methods=["POST"])
def test_celery():
        send_measurements_task()
        return jsonify({"status": "Message sent"})
    # try:
    # except Exception as e:
    #     return jsonify({"status": "bad", "message": f"{e}"}), 500
        