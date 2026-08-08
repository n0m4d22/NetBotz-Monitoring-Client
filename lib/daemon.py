"""Temperature and humidity monitor, threshold definitions."""

import datetime as dt 
import time
import logging
from . import alerts, client

# set logger
logger = logging.getLogger("daemon")
logging.basicConfig(filename=f"netbotz_{dt.datetime.now().strftime('%y%m%d_%H%M%S')}.log", level=logging.INFO)

# warning thresholds
DEFAULT_TEMPERATURE_WARNING_HIGH = 23.0 # °C
DEFAULT_TEMPERATURE_WARNING_LOW = 21.0 # °C
DEFAULT_HUMIDITY_WARNING_HIGH = 60.0 # RH%
DEFAULT_HUMIDITY_WARNING_LOW = 40.0 # RH%
# critical thresholds
DEFAULT_TEMPERATURE_CRITICAL_HIGH = 24.0 # °C
DEFAULT_TEMPERATURE_CRITICAL_LOW = 20.0 # °C
DEFAULT_HUMIDITY_CRITICAL_HIGH = 65.0 # RH%
DEFAULT_HUMIDITY_CRITICAL_LOW = 35.0 # RH%

# thread state
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
            print("---------------------------------------------------------------")
            if node_data:
                node.temperature = node_data['temperature']['value']
                node.humidity = node_data['humidity']['value']
                
                # Warnings
                if (node.temperature <= DEFAULT_TEMPERATURE_WARNING_LOW):
                    temperature_warning = f"[{timestamp}]: [WARNING]: {node.label}: Temperature decreased to abnormal levels. ({node.temperature})"
                elif (node.temperature >= DEFAULT_TEMPERATURE_WARNING_HIGH):
                    temperature_warning = f"[{timestamp}]: [WARNING]: {node.label}: Temperature increased to abnormal levels. ({node.temperature})" 
                try:
                    print(temperature_warning)
                    logger.warning(temperature_warning)
                except UnboundLocalError:
                    pass
                
                temperature_info = f"[{timestamp}]: {node.label}: Temperature: {node.temperature} °C"
                print(temperature_info)
                logger.info(temperature_info)

                if (node.humidity <= DEFAULT_HUMIDITY_WARNING_LOW):
                    humidity_warning = f"[{timestamp}]: [WARNING]: {node.label}: Humidity decreased to abnormal levels. ({node.humidity})"
                elif (node.humidity >= DEFAULT_HUMIDITY_WARNING_HIGH):
                    humidity_warning = f"[{timestamp}]: [WARNING]: {node.label}: Humidity increased to abnormal levels. ({node.humidity})"
                try:
                    print(humidity_warning)
                    logger.warning(humidity_warning)
                except UnboundLocalError:
                    pass

                humidity_info = f"[{timestamp}]: {node.label}: Humidity: {node.humidity} RH%"
                print(humidity_info)
                logger.info(humidity_info)     

                # Alerts
                if (node.temperature <= DEFAULT_TEMPERATURE_CRITICAL_LOW):
                    temprature_alert = f"[{timestamp}]: [CRITICAL]: {node.label}: Temperature decreased to critical levels. ({node.temperature})"
                elif (node.temperature >= DEFAULT_TEMPERATURE_CRITICAL_HIGH):
                    temprature_alert = f"[{timestamp}]: [CRITICAL]: {node.label}: Temperature increased to critical levels. ({node.temperature})"
                try:
                    print(temprature_alert)
                    logger.critical(temprature_alert)
                    alerts.alert(node, "temperature")
                except UnboundLocalError:
                    pass

                if (node.humidity <= DEFAULT_HUMIDITY_CRITICAL_LOW):
                    humidity_alert = f"[{timestamp}]: [CRITICAL]: {node.label}: Humidity decreased to critical levels. ({node.humidity})"
                elif (node.humidity >= DEFAULT_HUMIDITY_CRITICAL_HIGH):
                    humidity_alert = f"[{timestamp}]: [CRITICAL]: {node.label}: Humidity increased to critical levels. ({node.humidity})"                 
                try:
                    print(humidity_alert)
                    logger.critical(humidity_alert)
                    alerts.alert(node, "humidity")
                except UnboundLocalError:
                    pass
                   
        print("---------------------------------------------------------------")
        print("\n")
        time.sleep(10)

def stop():
    global _active
    if (_active == True):
        print("Terminating thread...")
        _active = False
    else:
        print("The daemon is not running...")
