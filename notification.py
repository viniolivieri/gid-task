from twilio.rest import Client
from telegram.ext import Updater
class notification():

    def __init__(self,params):
        if params['channel'] == 'sms':
            self.send_sms(params)
        elif params['channel'] == 'telegram':
            self.send_telegram(params)
        else:
            raise Exception('Channel Invalid','Check avaiable channels at http://localhost:5000/')
        
    
    def send_sms(self,params):
        account_sid = 'ACede9a763902618129d8cafe2a902578e'
        auth_token = 'fb98fbedc7c61fddfe973b3f399a1b7a'

        client = Client(account_sid, auth_token)

        message = client.messages \
                .create(
                     body=params['body'],
                     from_='+12568889648',
                     to='+'+str(params['whoto'])
                 )
    
    def send_telegram(self,params):
        updater = Updater(token='627567908:AAFANQBQUeKNtq09K6JaI1xrc9eYWawrQTA', use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.bot.send_message(chat_id=-337374241, text=params['body'])
        return
