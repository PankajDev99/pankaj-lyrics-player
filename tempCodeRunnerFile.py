
from flask import send_from_directory


def service_worker():
        return send_from_directory('static', 'sw.js')