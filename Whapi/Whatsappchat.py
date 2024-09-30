import requests
import time
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

options = {
    'headers': {
        'accept': 'application/json',
        'authorization': 'Bearer Q2JW7JjrikwnThChjwkCgfm1mtQfnN5p'
    }
}

last_message_id = None

def clear_terminal():
    # ANSI escape sequence to clear the terminal
    print("\033[H\033[J", end='')

def fetch_messages():
    logging.info('Fetching messages...')
    try:
        response = requests.get('https://gate.whapi.cloud/messages/list/120363317761180470%40g.us?count=100', headers=options['headers'])
        response.raise_for_status()
        data = response.json()
        logging.info('Parsed response: %s', data)

        if 'groups' in data and len(data['groups']) > 0:
            group = next((g for g in data['groups'] if g['id'] == '120363317761180470@g.us'), None)
            if group and 'last_message' in group:
                new_message = group['last_message']
                global last_message_id
                if last_message_id != new_message['id']:
                    last_message_id = new_message['id']
                    clear_terminal()  # Clear the terminal
                    logging.info('New message: %s', new_message)
                else:
                    logging.info('No new messages.')
            else:
                logging.info('No messages found.')
        else:
            logging.info('No groups found.')
    except requests.exceptions.HTTPError as http_err:
        logging.error('HTTP error occurred: %s', http_err)
    except requests.exceptions.ConnectionError as conn_err:
        logging.error('Connection error occurred: %s', conn_err)
    except requests.exceptions.Timeout as timeout_err:
        logging.error('Timeout error occurred: %s', timeout_err)
    except requests.exceptions.RequestException as req_err:
        logging.error('Request error occurred: %s', req_err)

# Poll the API every 5 seconds

    #fetch_messages()

