from flask import Flask
from repositories.devices_repository import DeviceRepository
from controllers.devices_management_rest_controller import devices_bp
from tests.connection_test import test_bp

app = Flask(__name__)

DeviceRepository()
app.register_blueprint(devices_bp)
app.register_blueprint(test_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)
