from flask import Flask,request,jsonify
from twilio.rest import Client
import requests, json
from notification import notification

app = Flask(__name__)


def get_ep_info(ep_id,token='dd0df21c8af5d929dff19f74506c4a8153d7acd34306b9761fd4a57cfa1d483c'):
        r = requests.get('http://api-staging.aiesec.org/v2/people/'+str(ep_id)+'?access_token='+token)
        return r.text
@app.route("/")
def hello():
    html = '''
    <html>
        <h1>This is an API for the GID Task!</h1>
        <h2> SERVICES AVAIABLE: SMS, TELEGRAM</h3>
        <h3> SMS Parameters</h3>
        <p>EP_ID as an integer</p>
        <p>channel as an string = 'sms'</p>
        <p>whoto as integer (format: COUNTRY_CODE + AREA_CODE + NUMBER)</p>
        <h3> Telegram Parameters</h3>
        <p>EP_ID as an integer</p>
        <p>channel as an string = 'telegram'</p>
        <a h_ref="https://t.me/joinchat/CRY3LRQb7CHE3h1ZrYo-Xw" target="blank_">Group Link for receiving notifications from telegram</a>
        <p>https://t.me/joinchat/CRY3LRQb7CHE3h1ZrYo-Xw</p>
    </html>

    
    '''
    return html

@app.route("/notification")
def send_sms():
    #Defining response
    response = {}
    
    #Getting variable from the request
    
    ep_id = request.args.get('ep_id', default=1, type=int)
    channel = request.args.get('channel', default='', type=str)
    whoto = request.args.get('whoto')

    #Requesting EP info and converting into a JSON
    p = json.loads(get_ep_info(ep_id))
    try:
        if p['status']['code'] != 200:
            response['status'] = 'failure'
            response['comment'] = 'review ep id'
            return response
    except:
        pass
    
    #Setting Body message, same for every channel
    body = '''
    Hello! Here is the result of your consult!
    EP Name: {ep_name}
    EP ID: {ep_id}
    LC: {ep_lc}
    MC: {ep_mc}
    Status: {ep_status}
    '''
    body = body.format(ep_name=p['full_name'],ep_id=p['id'],ep_lc=p['home_lc']['full_name'],ep_mc=p['home_lc']['country'],ep_status=p['status'])


    #send_by_the_channel_requested
    ##set params
    params = {
        'body':body,
        'whoto': whoto,
        'channel': channel
    }
    try:
        notification(params)
        response['ep_id'] = ep_id
        response['ep_name'] = p['first_name']
        response['channel'] = channel
        response['whoto'] = whoto
        response['body_message'] = params['body']
        response['status'] = 'success'
    except:
        response['status'] = 'failure'
        response['comment'] = 'review params on http://127.0.0.1:5000/ or contact support'

    return response

if __name__ == "__main__":
    app.run(debug=True)


