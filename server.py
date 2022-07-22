from flask import Flask
from MySQL_DB_connect_functions import *
from MySQL_DB_update_functions import *
from youtube_api_functions import *

app = Flask(__name__)

# http://localhost:8000/
@app.route("/", methods=['GET'])
def hello_world():
    # run other code here
    return 'This is Youtube Data Analysis test'


channel_id_list = ['UCYO_jab_esuFRV4b17AJtAw'] #3blue1brown

@app.route("/db-update", methods=['GET'])
def yt_API_db_update():
    youtube_obj = build_yt_API_object()
    video_df = create_video_df(youtube_obj, channel_id_list)
    processed_video_df = clean_video_df(video_df)

    host_name, dbname, schema_name, port, username, password = get_db_info()

    cnx = connect_to_db(username, password, host_name, schema_name, port)
    cursor = cnx.cursor()
    cursor.execute("DROP TABLE IF EXISTS videos")
    create_mysql_table(cursor)
    new_vid_df = update_db(cursor, processed_video_df)
    return str(new_vid_df.head())
    # append_from_df_to_db(cursor, new_vid_df)
    cnx.commit()
    cursor.close()
    cnx.close()

    return 'Youtube Data Update Complete'