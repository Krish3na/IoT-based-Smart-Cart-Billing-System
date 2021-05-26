import razorpay
import json

import threading
import logging as log
from werkzeug.serving import make_server
import time
from flask import Flask, render_template, request
global status1
status1=False
app = Flask(__name__,static_folder = "static", static_url_path='')
razorpay_client = razorpay.Client(auth=("rzp_test_apypqYs1I2IFY2", "ESwFHI6GBmaj2CbzsJlbGssC"))

class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        log.info('starting server')
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

def start_server():
    global server
    
    ...
    server = ServerThread(app)
    server.start()
    log.info('server started')
def stop_server():
    global server
    server.shutdown()



@app.route('/')
def app_create():
    return render_template('app.html')


@app.route('/charge', methods=['POST'])
def app_charge():
    global stat,amount,status,status1
    

    amount = amount1
    payment_id = request.form['razorpay_payment_id']
    j=razorpay_client.payment.capture(payment_id, amount)
    stat= razorpay_client.payment.fetch(payment_id)
    if stat:
        status=stat['status']
        print(status)
        status1=True
        print(status,status1)
    else:
        status1=False
        print(status1)
    
    #print(j)
    #if stat=='captured':
    return json.dumps({'Thankyou': 'Dear Customer !'})
    

def get_amount(amt):
    global amount1,server,status1
    amount1=amt[:-2]
    #print("amount  :",amount1)
    start_server()
    time.sleep(120)
    stop_server()

    if status1:
        return 'passed'
    else:
        return 'failed'
    #app.run(debug=False)


