from MySQL_DB_connect_functions import *
from MySQL_DB_update_functions import *
from youtube_api_functions import *

def run(channel_id_list):
    youtube_obj = build_yt_API_object()
    video_df = create_video_df(youtube_obj, channel_id_list)
    processed_video_df = clean_video_df(video_df)
    processed_video_df.to_csv(r'/Users/junwonchoi/Desktop/Projects/Youtube Data Analysis/test.csv', index = False, header=True)
    host_name, dbname, schema_name, port, username, password = get_db_info()

    cnx = connect_to_db(username, password, host_name, schema_name, port)
    cursor = cnx.cursor()
    cursor.execute("DROP TABLE IF EXISTS videos")
    create_mysql_table(cursor)

    # new_vid_df = update_df(cursor, processed_video_df)
    # new_vid_df.to_csv(r'/Users/junwonchoi/Desktop/Projects/Youtube Data Analysis/test.csv', index = False, header=True)
   
    # append_from_df_to_db(cursor, new_vid_df)
    # cnx.commit()
    # cursor.close()
    # cnx.close()