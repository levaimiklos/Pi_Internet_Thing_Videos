import random
import time

import thing

from flask import *


# Create flask app and global pi 'thing' object.
app = Flask(__name__)
pi_thing = thing.PiThing()


# Define app routes.
# Index route renders the main HTML page.
@app.route("/")
def index():
    # Read the current switch state to pass to the template.
    switch = pi_thing.read_switch()
    # Render index.html template.
    return render_template('index.html', switch=switch)

# LED route allows changing the LED state with a POST request.
@app.route("/led/<int:state>", methods=['POST'])
def led(state):
    # Check if the led state is 0 (off) or 1 (on) and set the LED accordingly.
    if state == 0:
        pi_thing.set_led(False)
    elif state == 1:
        pi_thing.set_led(True)
    else:
        return ('Unknown LED state', 400)
    return ('', 204)

# Server-sent event endpoint that streams the switch state every second.
@app.route("/switch")
def switch():
    def read_switch():
        while True:
            switch = pi_thing.read_switch()
            yield 'data: {0}\n\n'.format(switch)
            time.sleep(1.0)
    return Response(read_switch(), mimetype='text/event-stream')


# Start the flask debug server listening on the pi port 5000 by default.
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
