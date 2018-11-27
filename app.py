from flask import Flask, jsonify, render_template, request, url_for
from threading import Thread
import random, time, urllib.parse, requests, base64, configparser

config = configparser.ConfigParser()
config.read("config.ini")
SPOTIFY_CLIENT_ID = config["DEFAULT"]["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = config["DEFAULT"]["SPOTIFY_CLIENT_SECRET"]
IS_RPI_SERVER = int(config["DEFAULT"]["IS_RPI_SERVER"])

print("Configuring for a {} server".format("RPI" if IS_RPI_SERVER else "non-RPI"))

if IS_RPI_SERVER:
    import sensor

app = Flask(__name__)
sensor_read = (0,0) # TODO: Temp dummy datatype
access_token = None
refresh_token = None

# =========== Sensing Loop =============
def mockSensorRead():
    """ For use when developing on non-raspberry pi """
    return (random.randint(0, 10), random.randint(0, 10))

def readSensorLoop():
    global sensor_read
    while True:
        sensor_read = sensor.readSensors() if IS_RPI_SERVER else mockSensorRead()
        time.sleep(1.0)

# ========= Rendered Templates ==========
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/js/spotify-maker.js")
def spotifyMakerjs():
    """ Serves the dynamic js script. """
    return render_template("js/spotify-maker.js")

@app.route("/js/sensor-read.js")
def sensorReaderjs():
    """ Serves the dynamic js script. """
    return render_template("/js/sensor-read.js")

# ============ Service Endpoints ============
@app.route("/sensor/read", methods = ["GET"])
def getSensorData():
    """ Serves the current readings from the sensors. """
    return jsonify(read=sensor_read)

@app.route("/spotify/auth/grant", methods = ["GET"])
def authSpotify():
    """ Serves the formatted url for Spotify OAuth. """
    scopes = ["streaming", "user-read-birthdate", "user-read-email", "user-read-private"]
    scope_string = (" ").join(scopes)
    params = {
        "response_type": "code",
        "client_id": SPOTIFY_CLIENT_ID,
        "scope": scope_string,
        "redirect_uri": url_for("spotifyCallback", _external=True)
    }
    encoded_query_string = urllib.parse.urlencode(params)
    base_url = 'https://accounts.spotify.com/authorize'
    auth_request_url = base_url + "?" + encoded_query_string
    return jsonify(auth_url = auth_request_url)

@app.route("/spotify/auth/callback")
def spotifyCallback():
    """Callback endpoint for approved auth flow. Generates Auth Token."""
    auth_code = request.args["code"]
    unencoded_client_bytestring = (SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET).encode()
    auth_header_string = "Basic {}".format(base64.b64encode(unencoded_client_bytestring).decode())
    resp = requests.post("https://accounts.spotify.com/api/token",
    data = {
        "grant_type" : "authorization_code",
        "code" : auth_code,
        "redirect_uri": url_for("spotifyCallback", _external=True)
        },
    headers = {
        "Authorization" : auth_header_string
    })

    if resp.status_code == 200:
        data = resp.json()
        global access_token
        access_token = data["access_token"]
        return "AUTHORIZATION SUCCESS - You may now close this window."

    return "AUTHORIZATION ERROR: {}".format(resp.reason), 400

@app.route("/spotify/auth/access_token", methods = ["GET"])
def spotifyGetAccessToken():
    """ Returns the access token (if available) """
    if access_token:
        return jsonify(access_token = access_token), 200
    return jsonify(message = "Need to do auth!"), 400

if __name__ == "__main__":
    Thread(target = readSensorLoop).start()
    app.run(host="0.0.0.0", debug=True, ssl_context='adhoc')
