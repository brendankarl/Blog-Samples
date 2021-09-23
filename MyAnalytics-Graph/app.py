import uuid
import json
import flask
from flask_oauthlib.client import OAuth

CLIENT_ID = ''
CLIENT_SECRET = ''

REDIRECT_URI = 'http://localhost:5000/login/authorized'
AUTHORITY_URL = 'https://login.microsoftonline.com/organizations'
AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
TOKEN_ENDPOINT = '/oauth2/v2.0/token'
RESOURCE = 'https://graph.microsoft.com/'
API_VERSION = 'beta'
SCOPES = ['Analytics.Read']

APP = flask.Flask(__name__)
APP.secret_key = 'development'
OAUTH = OAuth(APP)
MSGRAPH = OAUTH.remote_app(
    'microsoft', consumer_key=CLIENT_ID, consumer_secret=CLIENT_SECRET,
    request_token_params={'scope': SCOPES},
    base_url=RESOURCE + API_VERSION + '/',
    request_token_url=None, access_token_method='POST',
    access_token_url=AUTHORITY_URL + TOKEN_ENDPOINT,
    authorize_url=AUTHORITY_URL + AUTH_ENDPOINT)

@APP.route('/')
def login():
    """Prompt user to authenticate."""
    flask.session['state'] = str(uuid.uuid4())
    return MSGRAPH.authorize(callback=REDIRECT_URI, state=flask.session['state'])

@APP.route('/login/authorized')
def authorized():
    """Handler for the application's Redirect Uri."""
    if str(flask.session['state']) != str(flask.request.args['state']):
        raise Exception('state returned to redirect URL does not match!')
    response = MSGRAPH.authorized_response()
    flask.session['access_token'] = response['access_token']
    return flask.redirect('/graphcall')

@APP.route('/graphcall')
def graphcall():
    """Confirm user authentication by calling Graph and displaying some data."""
    endpoint = 'me/analytics/activityStatistics'
    headers = {'SdkVersion': 'sample-python-flask',
               'x-client-SKU': 'sample-python-flask',
               'client-request-id': str(uuid.uuid4()),
               'return-client-request-id': 'true'}
    graphdata = MSGRAPH.get(endpoint, headers=headers).data
    data = str(graphdata).replace("'",'"')
    datadict = json.loads(data)
    summary = []
    i = 0
    while i < 5:
        if datadict["value"][i]["activity"] == "Focus":
            i += 1
        else:
            summary.append("Activity Type: " + datadict["value"][i]["activity"] + " / Date: " + datadict["value"][i]["startDate"] + " / After Hours " + datadict["value"][i]["afterHours"])
            i += 1
    return str(summary)  

@MSGRAPH.tokengetter
def get_token():
    """Called by flask_oauthlib.client to retrieve current access token."""
    return (flask.session.get('access_token'), '')

if __name__ == '__main__':
    APP.run()
