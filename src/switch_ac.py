import json
import requests


class OrionClient:
    def __init__(self, orion_endpoint):
        self.orion_endpoint = orion_endpoint

    def patch_attr(self, entity_id, data):
        headers = {
            'Content-Type': 'application/json'
        }
        url = '{}/v2/entities/{}/attrs'.format(self.orion_endpoint, entity_id)
        response = requests.patch(url, headers=headers, data=data)
        if response.status_code > 399:
            raise Exception(response.text)
        return response


def main(args):
    temperature = args['data'][0]['temperature']['value']
    threshold = int(args['threshold'])
    orion_endpoint = args['orion_endpoint']
    status = 'OFF'
    if temperature > threshold:
        status = 'ON'

    data = {
        "status": {
            "value": status,
            "type": "string"
        }
    }
    orion_client = OrionClient(orion_endpoint)
    orion_client.patch_attr('AirConditioner1', json.dumps(data))

    return {'result': 'success'}

