import os
from dotenv import load_dotenv
import telebot
import requests
import json

# Load Telegram API KEY
load_dotenv()
API_KEY = os.getenv('API_KEY')
bot = telebot.TeleBot(API_KEY)

# Login
project_id = ''

# API_table
API_TABLE = {
    'ID' : 'eth_blockNumber',
    'Author' : 'bor_getAuthor',
    'Signer' : 'bor_getSignersAtHash',
    'Validator' : 'bor_getCurrentValidators',
    'Proposer' : 'bor_getCurrentProposer'
}

def send_API(method, params=[]):
    url = f'https://polygon-mainnet.infura.io/v3/{project_id}'
    request_headers = {'Content-Type' : 'application/json'}
    form_data = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': method,
        'params': params
    }
    r = requests.post(url, data=json.dumps(form_data), headers=request_headers)
    return (json.loads(r.text))

def setname_request(message):
    request = message.text.split(' ')
    if request[0] == 'ID' and len(request) == 2:
        global project_id
        project_id = request[1]
        return True
    elif request[0] == 'Signer' and request[1][0:2] == '0x':
        return True
    elif request[0] == 'Author' or request[0] == 'Validator' or request[0] == 'Proposer':
        return True
    else:
        False

@bot.message_handler(func=setname_request)
def send_request(message):
    request = message.text.split(' ')
    if request[0] == 'ID':
        send_API("bor_getAuthor")
        bot.send_message(message.chat.id, "Change your id")
    elif request[0] == 'Author':
        res = send_API(API_TABLE['Author'])
        bot.send_message(message.chat.id, "Address of author's block: " + res['result'])
    elif request[0] == 'Signer':
        res = send_API(API_TABLE['Signer'], [request[1]])
        length = len(res['result'])
        result = f'There are {length} signers of this block.\n'
        for re in res['result']:
            result += f'{re}\n'
        bot.send_message(message.chat.id, result)
    elif request[0] == 'Validator':
        res = send_API(API_TABLE['Validator'])
        length = len(res['result'])
        result = f'There are {length} validators.\n'
        for re in res['result']:
            result += f'{re}\n'
        bot.send_message(message.chat.id, result)
    elif request[0] == 'Proposer':
        res = send_API(API_TABLE['Proposer'])
        bot.send_message(message.chat.id, "Address of the current proposer: " + res['result'])
    else:
        bot.send_message('Invalid commands')


@bot.message_handler(commands=['help'])
def help(message):
    result = "You can use these commands!!\n"
    result += '- ID{:>10}\n'.format('[Your ID]')
    result += '- Author{:>10}\n'.format('[Block ID]')
    result += '- Signer{:>10}\n'.format('[Block ID]')
    result += '- Validator\n'
    result += '- Proposer\n'
    bot.send_message(message.chat.id, result)

bot.polling()

