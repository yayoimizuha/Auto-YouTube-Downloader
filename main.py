import datetime
import os
import pprint

from googleapiclient.discovery import build

youtube = build(
    'youtube',
    'v3',
    developerKey=os.environ['API_KEY']
)


def get_playlist(playlist_id):
    next_page_token = ''
    while True:
        playlist = youtube.playlistItems().list(part='snippet,status',
                                                fields='items(snippet(publishedAt,resourceId/videoId,thumbnails,title),'
                                                       'status),nextPageToken',
                                                playlistId=playlist_id,
                                                pageToken=next_page_token,
                                                maxResults=50).execute()
        for playlistItem in playlist['items']:
            if playlistItem['status']['privacyStatus'] != 'public':
                continue
            date = datetime.datetime.fromisoformat(playlistItem['snippet']['publishedAt'].replace('Z', '+00:00'))
            thumbnail = sorted([playlistItem['snippet']['thumbnails'].get(i) for i in
                                playlistItem['snippet']['thumbnails']], key=lambda x: x['width'] * x['height'])[-1]
            youtube_data = {
                'title': playlistItem['snippet']['title'],
                'date': date.isoformat(),
                'videoId': playlistItem['snippet']['resourceId']['videoId'],
                'thumbUrl': thumbnail['url'],
                'thumbSize': {
                    'width': thumbnail['width'],
                    'height': thumbnail['height']
                }
            }
            pprint.pprint(youtube_data, indent=4)
            print('')
        if 'nextPageToken' not in playlist:
            break
        print("\n\n\n\n\n\n\n\n\n\n\n")
        next_page_token = playlist['nextPageToken']


get_playlist('PL0DCF7F78614F3AE6')
