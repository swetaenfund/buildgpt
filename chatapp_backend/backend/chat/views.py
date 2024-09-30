import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

options = {
    'headers': {
        'accept': 'application/json',
        'authorization': 'Bearer Q2JW7JjrikwnThChjwkCgfm1mtQfnN5p'
    }
}

last_message_id = None

@csrf_exempt
def fetch_group_messages(request):
    if request.method == 'GET':
        group_id = "120363317761180470@g.us"
        url = f"https://gate.whapi.cloud/messages/list/{group_id}?count=100"
        headers = options['headers']
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            logger.info('Parsed response: %s', data)

            if 'groups' in data and len(data['groups']) > 0:
                group = next((g for g in data['groups'] if g['id'] == group_id), None)
                if group and 'last_message' in group:
                    new_message = group['last_message']
                    global last_message_id
                    if last_message_id != new_message['id']:
                        last_message_id = new_message['id']
                        logger.info('New message: %s', new_message)
                        return JsonResponse(new_message)
                    else:
                        logger.info('No new messages.')
                        return JsonResponse({'message': 'No new messages.'})
                else:
                    logger.info('No messages found.')
                    return JsonResponse({'message': 'No messages found.'})
            else:
                logger.info('No groups found.')
                return JsonResponse({'message': 'No groups found.'})
        except requests.exceptions.HTTPError as http_err:
            logger.error('HTTP error occurred: %s', http_err)
            return JsonResponse({'error': 'HTTP error occurred'}, status=500)
        except requests.exceptions.ConnectionError as conn_err:
            logger.error('Connection error occurred: %s', conn_err)
            return JsonResponse({'error': 'Connection error occurred'}, status=500)
        except requests.exceptions.Timeout as timeout_err:
            logger.error('Timeout error occurred: %s', timeout_err)
            return JsonResponse({'error': 'Timeout error occurred'}, status=500)
        except requests.exceptions.RequestException as req_err:
            logger.error('Request error occurred: %s', req_err)
            return JsonResponse({'error': 'Request error occurred'}, status=500)
    return JsonResponse({'status': 'error'}, status=400)

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
