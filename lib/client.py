"""NetBotz core client transaction logic."""

import requests 
import xml.etree.ElementTree as Et
import urllib3

# disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# define the XML query that requests sensor data from nbAlink_Enc_0, which
# returns as response the values of nbAlink_Enc_0_TEMP and nbAlink_Enc_0_HUMI
XML_QUERY = (
    '<variable-query>'
    '<result-filter incguid="yes">'
    '<incmeta slotid="nbLabel"/>'
    '<incmeta slotid="nbDefLabel"/>'
    '<incmeta slotid="nbUnitsID"/>'
    '<incmeta slotid="nbSensorMonitored"/>'
    '<incmeta slotid="nbSensorPlugged"/>'
    '<incmeta slotid="nbSensorIsUnplugged"/>'
    '</result-filter>'
    '<id-query varid="nbAlinkEnc_0"/>'
    '<result-filter incguid="yes">'
    '<incmeta slotid="nbUnitsID"/>'
    '<incmeta slotid="nbLabel"/>'
    '<incmeta slotid="nbSensorMonitored"/>'
    '<incmeta slotid="nbSensorPlugged"/>'
    '<incmeta slotid="nbSensorIsUnplugged"/>'
    '</result-filter>'
    '<type-class-query class="nbSensor">'
    '<metadata slotid="nbEncID">'
    '<varid-val>nbAlinkEnc_0</varid-val>'
    '</metadata>'
    '</type-class-query>'
    '</variable-query>'
)

# class that defines the properties of each node
class Node:
    def __init__(self, ip, label, temperature, humidity):
        self.ip = ip
        self.label = label
        self.temperature = temperature
        self.humidity = humidity

# creates object of type Node and assigns initial values upon creation
def nodify(NETBOTZ_NODES, NETBOTZ_CREDENTIALS):
    node_objects = []
    for label, ip in NETBOTZ_NODES:
            node = Node(ip, label, 0.0, 0.0)
            data = get_data(node, NETBOTZ_CREDENTIALS) # fetch initial data
            if data:
                node.temperature = data['temperature']['value']
                node.humidity = data['humidity']['value']
                print("Node initialized: ", node.ip, " as ", node.label)
            node_objects.append(node)
    return node_objects

# fetch the live data from the provided nodes 
def get_data(node, credentials):
    parameters = {'QUERY': XML_QUERY}
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        url = "http://" + node.ip + "/xmlQuery" # create the proper request for each node

        # FIXME: requires work-around
        # verify=False: NetBotz units use self-signed certs; acceptable ONLY on isolated LAN
        response = requests.get(url, params=parameters, auth=credentials, headers=headers, verify=False, timeout=10) 

        if response.status_code != 200:
            print(f"Error: HTTP {response.status_code}")
            return None
        
        response_content = Et.fromstring(response.content)
        data = {}

        for variable in response_content.findall('.//variable'):
            varid = variable.get('varid', '')
            if varid.endswith('_TEMP'):
                val_node = variable.find('double-val')
                label_node = variable.find('.//metadata[@slotid="nbLabel"]/nls-string-val')
                if val_node is not None:
                    temperature_string = val_node.text.replace(',', '.')
                    data['temperature'] = {
                        'name': label_node.text if label_node is not None else 'Temperature',
                        'value': float(temperature_string)
                    }
            elif varid.endswith('_HUMI'):
                val_node = variable.find('double-val')
                label_node = variable.find('.//metadata[@slotid="nbLabel"]/nls-string-val')
                if val_node is not None:
                    humidity_string = val_node.text.replace(',', '.')
                    data['humidity'] = {
                        'name': label_node.text if label_node is not None else 'Humidity',
                        'value': float(humidity_string)
                    }
        return data if data else None

    except Exception as e:
        print(f"Exception trace: {e}")
        return None
