from turtle import update
from flask import Flask
from update import run as update_runner

app = Flask(__name__)

# http://localhost:8000/
@app.route("/", methods=['GET'])
def hello_world():
    # run other code here
    return 'This is Youtube Data Analysis test'


# channel_id_list = ['UCYO_jab_esuFRV4b17AJtAw'] #3blue1brown
channel_id_list = ['UCIRYBXDze5krPDzAEOxFGVA'] #TheGuardian,NYTimes(UCqnbDFdCpuN8CMEg0VuEBqA)

@app.route("/db-update", methods=['GET'])
def yt_API_db_update():
    update_runner(channel_id_list)
    return 'Youtube Data Update Complete'