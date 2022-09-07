from MySQL_DB_connect_functions import *
from MySQL_DB_update_functions import *
from youtube_api_functions import *

def run(channel_id_list):
    # using youtube_api_functions.py:
    youtube_obj = build_yt_API_object() # builds Youtube API object
    video_df = create_video_df(youtube_obj, channel_id_list) # store API data into pandas df
    processed_video_df = clean_video_df(video_df) # run df through cleaning function

    # processed_video_df.to_csv(r'/Users/junwonchoi/Desktop/Projects/Youtube Data Analysis/test1.csv', index = False, header=True)
    
    # using MySQL_DB_connect_functions.py:
    host_name, dbname, schema_name, port, username, password = get_db_info() # imports sensitive auth. information from .env file
    cnx = connect_to_db(username, password, host_name, schema_name, port) # creates connection object
    cursor = cnx.cursor() # activates connection cursor

    cursor.execute("DROP TABLE IF EXISTS videos")

    # using MySQL_DB_update_functions.py:
    create_mysql_table(cursor) # create empty SQL table
    append_from_df_to_db(cursor, processed_video_df) # append cleaned dataframe to database table

    # new_vid_df = update_db(cursor, processed_video_df)
    # new_vid_df.to_csv(r'/Users/junwonchoi/Desktop/Projects/Youtube Data Analysis/test2.csv', index = False, header=True)
    # append_from_df_to_db(cursor, new_vid_df)
    cnx.commit()
    cursor.close()
    cnx.close()
    print('Test Complete')

channel_id_list = ['UCIRYBXDze5krPDzAEOxFGVA'] #TheGuardian,NYTimes(UCqnbDFdCpuN8CMEg0VuEBqA)
run(channel_id_list)