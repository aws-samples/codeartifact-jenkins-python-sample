# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from flask import Flask
from fantastic_ascii import ascii
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return "<pre>%s</pre>" % ascii.joe_say("Current time is %s" % current_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)