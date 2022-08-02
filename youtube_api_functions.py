# Import libraries for API request
from googleapiclient.discovery import build
from IPython.display import JSON
import urllib.request
import urllib
import json
import pandas as pd
import numpy as np
import datetime
import isodate
import os
from dotenv import load_dotenv

def build_yt_API_object():
    # Import Credentials
    load_dotenv()
    API_KEY = os.getenv('API_KEY')

    # Create Youtube API build object
    api_service_name = "youtube"
    api_version = "v3"
    youtube_obj = build(api_service_name, api_version, developerKey=API_KEY)

    return youtube_obj

def get_channel_stats(youtube, channel_ids):

    """
    Gets general channel statistics

    Params:
    --------
    youtube: Youtube API build object
    channel_ids: list of channel IDs

    Return:
    --------
    Pandas Dataframe containing the channel name, subscriber count, view count, video count, playlist id (associated with all channel uploads)

    """
    
    all_data = []
    
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids)
    )
    response = request.execute()
    
    # Loop through 'items' to extract channel statistics
    for item in response['items']:
        data = {'channel_name': item['snippet']['title'],
                'subscribers': item['statistics']['subscriberCount'],
                'total_views': item['statistics']['viewCount'],
                'total_videos': item['statistics']['videoCount'],
                'playlist_id': item['contentDetails']['relatedPlaylists']['uploads']
                }
        
        all_data.append(data)
        
    return(pd.DataFrame(all_data))

def get_video_ids(youtube, playlist_id):
    
    """
    Gets video ids of selected playlist id

    Params:
    --------
    youtube: Youtube API build object
    playlist_id: distinct playlist id from a channel

    Return:
    --------
    List containing the video ids of all uploaded videos of a channel

    """

    video_ids = []

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults = 50 # The maximum number of results Youtube API will return on a single instance
    )
    response = request.execute()
    
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
        
    # Implement 'next_page_token' to loop through all pages containing video data
    next_page_token = response.get('nextPageToken')
    
    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults = 50,
            pageToken = next_page_token # Prevents infinite loop
        )
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')
    
    return video_ids

def get_video_details(youtube, video_ids):

    """
    Gets video ids of selected playlist id

    Params:
    --------
    youtube: Youtube API build object
    video_ids: list of video ids

    Return:
    --------
    Pandas Dataframe containing detailed information from uploaded videos

    """
    
    all_video_info = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'favoriteCount', 'commentCount'],
                             'contentDetails': ['duration', 'definition', 'caption']
                            }

            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)
        
    return pd.DataFrame(all_video_info)

def get_vid_title(video_id):
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return data['title']

def get_video_comments(youtube, video_id):

    request = youtube.commentThreads().list(
        part='snippet',
        maxResults=100,
        textFormat='plainText',
        order='time',
        videoId=video_id
        # allThreadsRelatedToChannelId=channel_id
    )
    response = request.execute()

    video_ids, vid_titles, comment_ids, comments, like_counts, reply_counts, authorurls, authornames, dates, totalReplyCounts = [], [], [], [], [], [], [], [], [], []

    while response:
        for item in response['items']:
            video_id = item['snippet']['topLevelComment']['snippet']['videoId']
            vid_title = get_vid_title(video_id)
            comment_id = item['snippet']['topLevelComment']['id']
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
            reply_count = item['snippet']['totalReplyCount']
            authorurl = item['snippet']['topLevelComment']['snippet']['authorChannelUrl']
            authorname = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            date = item['snippet']['topLevelComment']['snippet']['publishedAt']
            totalReplyCount = item['snippet']['totalReplyCount']

            video_ids.append(video_id)
            vid_titles.append(vid_title)
            comment_ids.append(comment_id)
            comments.append(comment)
            like_counts.append(like_count)
            reply_counts.append(reply_count)
            authorurls.append(authorurl)
            authornames.append(authorname)
            dates.append(date)
            totalReplyCounts.append(totalReplyCount)

        try:
            if 'nextPageToken' in response:
                request = youtube.commentThreads().list(
                    part='snippet',
                    maxResults=100,
                    textFormat='plainText',
                    order='time',
                    videoId=video_id
                    # allThreadsRelatedToChannelId=channelId
                )
                response = request.execute()
            else:
                break
        except: break

    comment_dict = {'video_id': video_ids,
                    'vid_title': vid_titles,
                    'comment_id': comment_ids,
                    'comment': comments,
                    'like_count': like_counts,
                    'reply_count': like_counts,
                    'authorurl': authorurls,
                    'authorname': authornames, 
                    'date': dates,
                    'totalReplyCount': totalReplyCounts
    }
    
    return pd.DataFrame(comment_dict)

def create_video_df(youtube_obj, channel_id_list):
    channel_stats = get_channel_stats(youtube_obj, channel_id_list)

    playlist_ids = channel_stats['playlist_id'].to_list()

    video_ids = []
    for id in playlist_ids:
        video_ids.extend(get_video_ids(youtube_obj, id))

    video_df = get_video_details(youtube_obj, video_ids)

    return video_df

def clean_video_df(video_df):
    # Change data types of columns with quantitative values from object to numeric
    numeric_cols = ['viewCount', 'likeCount', 'favoriteCount', 'commentCount'] # Listing columns to convert to numeric data type
    video_df[numeric_cols] = video_df[numeric_cols].apply(pd.to_numeric, errors = 'coerce', axis = 1)

    # Change the 'true' and 'false' objects in definition to '1' and '0' respectively (for convenience when importing data into MySQL database)
    video_df['caption'] = np.where(video_df['caption'] == 'true', 1, 0)

    # Add column showing published day of the week
    video_df['publishedAt'] = pd.to_datetime(video_df['publishedAt']).dt.tz_localize(None)
    video_df['publishDayName'] = video_df['publishedAt'].apply(lambda x: x.strftime('%A'))
    video_df['publishedAt'] = video_df['publishedAt'].apply(lambda x: x.strftime('%Y-%m-%d'))

    # Convert duration (originally in ISO format) to seconds using the 'isodate' library
    video_df['durationSecs'] = video_df['duration'].apply(lambda x: isodate.parse_duration(x))
    video_df['durationSecs'] = video_df['durationSecs'].astype('timedelta64[s]') # extracts only seconds from timedelta values

    # Add tag count
    video_df['tagCount'] = video_df['tags'].apply(lambda x: 0 if x is None else len(x))

    # Remove unused columns
    video_df = video_df.drop(['tags', 'duration', 'definition'], axis=1)

    return video_df