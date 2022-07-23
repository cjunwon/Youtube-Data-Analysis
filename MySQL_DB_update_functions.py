import pandas as pd

def create_mysql_table(cursor):
    create_video_table_query = (
    """
    CREATE TABLE IF NOT EXISTS videos (
        video_id VARCHAR(255) PRIMARY KEY,
        channelTitle TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        publishedAt DATE NOT NULL,
        viewCount INT(255) NOT NULL,
        likeCount INT(255) NOT NULL,
        favoriteCount INT(255) NOT NULL,
        commentCount INT(255) NOT NULL,
        caption BOOL NOT NULL,
        publishDayName TEXT NOT NULL,
        durationSecs INT(255) NOT NULL,
        tagCount INT(255) NOT NULL
    );
    """
    )
    
    cursor.execute(create_video_table_query)
    print('MySQL table created')

def check_if_video_exists(cursor, video_id):

    check_vid_query = (
    """
    SELECT video_id
    FROM videos
    WHERE video_id = %s;
    """
    )
    
    cursor.execute(check_vid_query, (video_id,))

    return cursor.fetchone() is not None

# update row if new video exists
def update_row(cursor, video_id, channelTitle, title, description, publishedAt, viewCount, likeCount, favoriteCount, commentCount, caption, publishDayName, durationSecs, tagCount):
    
    update_row_query = (
    """
    UPDATE videos
    SET channelTitle = %s,
        title = %s,
        description = %s,
        publishedAt = %s,
        viewCount = %s,
        likeCount = %s,
        favoriteCount = %s,
        commentCount = %s,
        caption BOOL = %s,
        publishDayName = %s,
        durationSecs = %s,
        tagCount = %s
    WHERE video_id = %s;
    """
    )
    
    vars_to_update = (channelTitle, title, description, publishedAt, viewCount, likeCount, favoriteCount, commentCount, caption, publishDayName, durationSecs, tagCount, video_id)
    
    cursor.execute(update_row_query, vars_to_update)

def update_df(cursor, df):
    tmp_df = pd.DataFrame(columns=['video_id', 'channelTitle', 'title', 'description', 'publishedAt', 'viewCount', 'likeCount', 'favoriteCount', 'commentCount', 'caption', 'publishDayName', 'durationSecs', 'tagCount'])

    for i, row in df.iterrows():
        if check_if_video_exists(cursor, row['video_id']):
            update_row(cursor, row['video_id'], row['channelTitle'], row['title'], row['description'], row['publishedAt'], row['viewCount'], row['likeCount'], row['favoriteCount'], row['commentCount'], row['caption'], row['publishDayName'], row['durationSecs'], row['tagCount'])
        else:
            pd.concat([tmp_df, row])
            # tmp_df = tmp_df.append(row)
            
    return tmp_df

def insert_into_table(cursor, video_id, channelTitle, title, description, publishedAt, viewCount, likeCount, favoriteCount, commentCount, caption, publishDayName, durationSecs, tagCount):

    insert_into_videos_query = (
        """
        INSERT INTO videos
        (video_id, channelTitle, title, description, publishedAt, viewCount, likeCount, favoriteCount, commentCount, caption, publishDayName, durationSecs, tagCount)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
    )

    row_to_insert = (video_id, channelTitle, title, description, publishedAt, viewCount, likeCount, favoriteCount, commentCount, caption, publishDayName, durationSecs, tagCount)

    cursor.execute(insert_into_videos_query, row_to_insert)

def append_from_df_to_db(cursor, df):
    for i, row in df.iterrows():
        insert_into_table(cursor, row['video_id'], row['channelTitle'], row['title'], row['description'], row['publishedAt'], row['viewCount'], row['likeCount'], row['favoriteCount'], row['commentCount'], row['caption'], row['publishDayName'], row['durationSecs'], row['tagCount'])
    print('Dataframe appended to database')