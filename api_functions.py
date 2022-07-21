# Import Libraries for API request
from googleapiclient.discovery import build
from IPython.display import JSON
import pandas as pd

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