import json
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging


logger = logging.getLogger(__name__)

options = {
    'headers': {
        'accept': 'application/json',
        'authorization': 'Bearer Q2JW7JjrikwnThChjwkCgfm1mtQfnN5p'
    }
}

global last_message_id 
last_message_id = None

def fetch_messages():
    logging.info('Fetching messages...')
    print('Fetching messages...')
    try:
        response = requests.get('https://gate.whapi.cloud/messages/list/120363317761180470%40g.us?count=100', headers=options['headers'])
        response.raise_for_status()
        data = response.json()
        logging.info('Parsed response: %s', data)
        return data

    except requests.exceptions.HTTPError as http_err:
        logging.error('HTTP error occurred: %s', http_err)
    except requests.exceptions.ConnectionError as conn_err:
        logging.error('Connection error occurred: %s', conn_err)
    except requests.exceptions.Timeout as timeout_err:
        logging.error('Timeout error occurred: %s', timeout_err)
    except requests.exceptions.RequestException as req_err:
        logging.error('Request error occurred: %s', req_err)


def fetch_group_messages(request):
    if request.method == 'GET':
        try:
            print(f"###Lable: 1 {last_message_id}")
            response = fetch_messages()
            print(response)
            return HttpResponse(response)
        
        except requests.exceptions.RequestException as req_err:
            logger.error('Request error occurred: %s', req_err)
            return HttpResponse(f"status error. status=500")
        
    return HttpResponse(f"status error. status=400")

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            # Process incoming message
            message = data['messages']['text']['body']
            logger.debug(f"Received message: {message}")
            # Update your website with the new message
            # For example, save the message to the database or send it to connected clients
            return JsonResponse({'status': 'success'})
        except KeyError as e:
            logger.error(f"KeyError: {e}")
            return JsonResponse({'status': 'error', 'message': 'Invalid data format'}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        group_id = "120363317761180470@g.us"
        token = "Q2JW7JjrikwnThChjwkCgfm1mtQfnN5p"
        url = f"https://gate.whapi.cloud/groups/{group_id}/messages"
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {token}",
            "content-type": "application/json"
        }
        payload = {
            "text": message
        }
        response = requests.post(url, headers=headers, json=payload)
        return JsonResponse(response.json())
    return JsonResponse({'status': 'error'}, status=400)
