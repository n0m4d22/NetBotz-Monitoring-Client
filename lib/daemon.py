"""Temperature and humidity monitor, threshold definitions."""

import datetime as dt 
import time
from . import alerts, client

# warning thresholds
DEFAULT_TEMPERATURE_WARNING_HIGH = 23.0 # °C
DEFAULT_TEMPERATURE_WARNING_LOW = 21.0 # °C
DEFAULT_HUMIDITY_WARNING_HIGH = 60.0 # RH%
DEFAULT_HUMIDITY_WARNING_LOW = 40.0 # RH%
# critical thresholds
DEFAULT_TEMPERATURE_CRITICAL_HIGH = 23.5 # °C
DEFAULT_TEMPERATURE_CRITICAL_LOW = 20.5 # °C
DEFAULT_HUMIDITY_CRITICAL_HIGH = 63.0 # RH%
DEFAULT_HUMIDITY_CRITICAL_LOW = 38.0 # RH%

global _active
_active = False

# start monitoring changes
def start(NETBOTZ_NODES, NETBOTZ_CREDENTIALS):
    global _active
    _active = True
    node_objects = client.nodify(NETBOTZ_NODES, NETBOTZ_CREDENTIALS)

    while (_active):
        timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for node in node_objects:
            node_data = client.get_data(node, NETBOTZ_CREDENTIALS)
            if node_data:
                node.temperature = node_data['temperature']['value']
                node.humidity = node_data['humidity']['value']

                # Warnings
                if (node.temperature <= DEFAULT_TEMPERATURE_WARNING_LOW):
                    print(f"[{timestamp}]: {node.label}: Temperature decreased to abnormal levels. ({node.temperature})")
                elif (node.temperature >= DEFAULT_TEMPERATURE_WARNING_HIGH):
                    print(f"[{timestamp}]: {node.label}: Temperature increased to abnormal levels. ({node.temperature})") 
                else:
                    print(f"[{timestamp}]: {node.label}: Temperature: {node.temperature} °C")
                if (node.humidity <= DEFAULT_HUMIDITY_WARNING_LOW):
                    print(f"[{timestamp}]: {node.label}: Humidity decreased to abnormal levels. ({node.humidity})")
                elif (node.humidity >= DEFAULT_HUMIDITY_WARNING_HIGH):
                    print(f"[{timestamp}]: {node.label}: Humidity increased to abnormal levels. ({node.humidity})")
                else:
                    print(f"[{timestamp}]: {node.label}: Humidity: {node.humidity} RH%")            

                # Alerts
                if (node.temperature <= DEFAULT_TEMPERATURE_CRITICAL_LOW):
                    print(f"[{timestamp}]: {node.label}: Temperature decreased to critical levels. ({node.temperature})")
                    alerts.alert(node, "temperature")
                if (node.temperature >= DEFAULT_TEMPERATURE_CRITICAL_HIGH):
                    print(f"[{timestamp}]: {node.label}: Temperature increased to critical levels. ({node.temperature})")
                    alerts.alert(node, "temperature") 
                if (node.humidity <= DEFAULT_HUMIDITY_CRITICAL_LOW):
                    print(f"[{timestamp}]: {node.label}: Humidity decreased to critical levels. ({node.humidity})")
                    alerts.alert(node, "humidity")
                if (node.humidity >= DEFAULT_HUMIDITY_CRITICAL_HIGH):
                    print(f"[{timestamp}]: {node.label}: Humidity increased to critical levels. ({node.humidity})")
                    alerts.alert(node, "humidity")   
        print("---------------------------------------------------------------")
        time.sleep(10)

def stop():
    global _active
    if (_active == True):
        print("Terminating thread...")
        _active = False
    else:
        print("The daemon is not running...")
