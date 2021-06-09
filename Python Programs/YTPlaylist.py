'''
@author: mkpro118
@last updated : 19-05-2021
'''


import os
import re
import requests
from bs4 import BeautifulSoup as bs
from datetime import timedelta
from googleapiclient.discovery import build


class YTPlaylistInfo:
    '''This Class can access any public playlist on Youtube and return the total duration of the playlist,
    sort the playlist on numerous factors such as duration, likes, dislikes, views and title
    Warning : The sort methods return generator objects
    '''

    def __init__(self, playlistID, api_key=os.environ.get('YT_API_Password')):
        '''Returns a YTPlaylistInfo object
        Required Parameter <plalistID> (string) : The ID of the Youtube Playlist
        Warning: Only one playlist can be analysed at a time
        Required Parameter <api_key> (string) : The Developer's API key for the Youtube API
        NOTE : Recommend using the classmethods ==>  <from_url(cls, url)> or
        <from_id(cls, playlist_ID)> to create YTPlaylistInfo objects
        '''
        self.api_key = api_key
        self.playlistID = playlistID
        self.totalDuration = 0
        self.hours_pattern = re.compile(r'(\d+)[Hh]')
        self.minutes_pattern = re.compile(r'(\d+)[Mm]')
        self.seconds_pattern = re.compile(r'(\d+)[Ss]')
        self.nextPageToken = None
        self.videos = []
        source = requests.get(f'https://youtube.com/playlist?list={self.playlistID}').text
        soup = bs(source, 'lxml')
        title = soup.find('title').text
        self.playlistTitle = title.replace(' - YouTube', '')
        self.__findVideos()

    def __findVideos(self):
        '''Warning: This method is run automatically
        and should not be accessed.
        '''
        with build('youtube', 'v3', developerKey=self.api_key) as youtube:
            while True:
                playlist_request = youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=self.playlistID,
                    maxResults=50,
                    pageToken=self.nextPageToken
                )
                playlist_response = playlist_request.execute()
                video_IDs = []
                for item in playlist_response['items']:
                    video_IDs.append(item['contentDetails']['videoId'])
                video_request = youtube.videos().list(
                    part='contentDetails, statistics, snippet',
                    id=','.join(video_IDs)
                )
                video_response = video_request.execute()
                for item in video_response['items']:
                    try:
                        Duration = self._findDuration(item['contentDetails']['duration'], work_type='convert')
                    except KeyError:
                        Duration = 'unknown'
                    try:
                        Id = item['id']
                    except KeyError:
                        Id = 'unknown'
                    try:
                        Title = item['snippet']['title']
                    except KeyError:
                        Title = 'unknown'
                    try:
                        ViewCount = item['statistics']['viewCount']
                    except KeyError:
                        ViewCount = 'unknown'
                    try:
                        LikeCount = item['statistics']['likeCount']
                    except KeyError:
                        LikeCount = 'unknown'
                    try:
                        DislikeCount = item['statistics']['dislikeCount']
                    except KeyError:
                        DislikeCount = 'unknown'
                    try:
                        Length = self._findDuration(item['contentDetails']['duration'], work_type='length')
                    except KeyError:
                        Length = 'unknown'
                    vid_info = {'Id': Id, 'ViewCount': ViewCount, 'Title': Title, 'Link': f'https://youtu.be/{self.playlistID}',
                                'Duration': Duration, 'LikeCount': LikeCount, 'DislikeCount': DislikeCount, 'Length': Length}
                    self.videos.append(vid_info)

                self.nextPageToken = playlist_response.get('nextPageToken')
                if not self.nextPageToken:
                    break

    def _findDuration(self, duration, work_type):
        ''' This method parses the duration paramter
        into hours, minutes and seconds, and returns the
        total number of seconds if <work_type == 'length'
        and returns a formatted string of the duration of
        a Youtube video if <work_type == 'convert'
        Required Parameter <duration> (string) : String of the form PT00H00M00S
        Required Parameter <work_type> (string) :
        'convert' indicates a formatted duration string is desired
        'length' indicates that the total number of seconds in the duration is desired
        '''
        hours = self.hours_pattern.search(duration)
        minutes = self.minutes_pattern.search(duration)
        seconds = self.seconds_pattern.search(duration)
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0
        total_seconds = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds
        ).total_seconds()
        if work_type == 'convert':
            self.totalDuration += int(total_seconds)
            val = None
            if hours == 0:
                if minutes == 0:
                    val = f'{seconds}s'
                else:
                    val = f'{minutes}m {seconds}s'
            else:
                val = f'{hours}h {minutes}m {seconds}s'

            return val
        if work_type == 'length':
            return int(total_seconds)

    def sortbyDuration(self, rev=False):
        '''Sorts the videos list by Duration, shortedt first
        Returns a generator of the sorted videos
        Optional Parameter <rev> (bool) : Default value is : False
        False sorts the videos shortest first,
        True sorts the videos longest first
        '''
        unknown_videos = []
        videos_copy = []
        for video in self.videos:
            if video['Length'] == 'unknown':
                unknown_videos.append(video)
            else:
                videos_copy.append(video)
        videos_copy.sort(key=lambda vid: vid['Length'], reverse=rev)
        all_videos = videos_copy + unknown_videos
        yield from all_videos

    def sortbyLikes(self, rev=True):
        '''Sorts the videos list by the number of Likes it has on youtube, most liked first
        Returns a generator of the sorted videos
        Optional Parameter <rev> (bool) : Default value is : True
        False sorts the videos least liked first,
        True sorts the videos most liked first
        '''
        unknown_videos = []
        videos_copy = []
        for video in self.videos:
            if video['LikeCount'] == 'unknown':
                unknown_videos.append(video)
            else:
                videos_copy.append(video)
        videos_copy.sort(key=lambda vid: int(vid['LikeCount']), reverse=rev)
        all_videos = videos_copy + unknown_videos
        yield from all_videos

    def sortbyDislikes(self, rev=True):
        '''Sorts the videos list by the number of Disikes it has on youtube, most disliked first
        Returns a generator of the sorted videos
        Optional Parameter <rev> (bool) : Default value is : True
        False sorts the videos least disliked first,
        True sorts the videos most disliked first
        '''
        unknown_videos = []
        videos_copy = []
        for video in self.videos:
            if video['DislikeCount'] == 'unknown':
                unknown_videos.append(video)
            else:
                videos_copy.append(video)
        videos_copy.sort(key=lambda vid: int(vid['DislikeCount']), reverse=rev)
        all_videos = videos_copy + unknown_videos
        yield from all_videos

    def sortbyViews(self, rev=True):
        '''Sorts the videos list by the number of Views it has on youtube, most viewed first
        Returns a generator of the sorted videos
        Optional Parameter <rev> (bool) : Default value is : True
        False sorts the videos least viewed first
        True sorts the videos most viewed first
        '''
        unknown_videos = []
        videos_copy = []
        for video in self.videos:
            if video['ViewCount'] == 'unknown':
                unknown_videos.append(video)
            else:
                videos_copy.append(video)
        videos_copy.sort(key=lambda vid: int(vid['ViewCount']), reverse=rev)
        all_videos = videos_copy + unknown_videos
        yield from all_videos

    def sortbyTitle(self, rev=False):
        '''Sorts the videos list alphabetically
        Returns a generator of the sorted videos
        Optional Parameter <rev> (bool) : Default value is : False
        False sorts the videos in alphabetically ascending order [A-Z],
        True sorts the videos in alphabetically descending order [Z-A]
        '''
        unknown_videos = []
        videos_copy = []
        for video in self.videos:
            if video['Title'] == 'unknown':
                unknown_videos.append(video)
            else:
                videos_copy.append(video)
        videos_copy.sort(key=lambda vid: vid['Title'] if 'The' != vid['Title'][:3] else vid['Title'].replace('The ', ''), reverse=rev)
        all_videos = videos_copy + unknown_videos
        yield from all_videos

    def getVideoLength(self, video):
        '''Returns the Length of the video in seconds
        Required Parameter <video> (dict) : any one element of the YTPlaylistInfo<object>.videos list
        '''
        return video['Length']

    def getVideoDuration(self, video):
        '''Returns the Duration of the video
        Required Parameter <video> (dict) : any one element of the YTPlaylistInfo<object>.videos list
        '''
        return video['Duration']

    def getVideoTitle(self, video):
        '''Returns the Title of the video
        Required Parameter <video> (dict) : any one element of the YTPlaylistInfo<object>.videos list
        '''
        return video['Title']

    def getVideoLink(self, video):
        '''Returns the Youtube link to the video
        Required Parameter <video> (dict): any one element of the YTPlaylistInfo<object>.videos list
        '''
        return video['Link']

    def getNumberOfLikes(self, video):
        '''Returns the Number of Likes on the video
        Required Parameter <video> (dict): any one element of the YTPlaylistInfo<object>.videos list
        '''
        return video['LikeCount']

    def getNumberOfDislikes(self, video):
        '''Returns the Number of Dislikes on the video
        Required Parameter <video> (dict) : any one element of the YTPlaylistInfo<object>.videos list
        '''
        return video['DislikeCount']

    def getNumberOfViews(self, video):
        '''Returns the Number of views on the video
        Required Parameter <video> (dict) : any one element of the YTPlaylistInfo<object>.videos list
        '''
        return video['ViewCount']

    def getVideoID(self, video):
        '''Returns the Youtube Video ID for the video
        Required Parameter <video> (dict) : any one element of the YTPlaylistInfo<object>.videos list
        '''
        return video['Id']

    def getVideoNames(self):
        '''Returns a generator of the Title of all the videos in the playlist, in the order of appearance
        '''
        yield from self.videos

    def listVideoNames(self):
        '''Prints all the video Titles in the playlist, in order of appearance
        '''
        for video in self.videos:
            print(video['Title'])

    def getTotalDuration(self):
        '''Returns a formatted string of the total duration of the playlist
        in the form : 00h 00m 00s
        '''
        minutes, seconds = divmod(self.totalDuration, 60)
        hours, minutes = divmod(minutes, 60)
        return f'{self.playlistTitle} is {hours}h {minutes}m {seconds}s long'

    @classmethod
    def from_url(cls, url):
        '''Recommended to use this classmethod as an instatiator for the class
        if the url to the playlist is known
        Required Parameter <url> (string) : The url to the playlist
        '''
        pattern = re.compile(r'list=([\w-]+)&?')
        playlist_ID = pattern.search(url).group(1)
        return cls(playlist_ID)

    @classmethod
    def from_id(cls, playlist_ID):
        '''Recommended to use this classmethod as an instatiator for the class
        if the playlist ID is known
        Required Parameter <playlist_ID> (string) : The playlist ID
        '''
        return cls(playlist_ID)


if __name__ == '__main__':
    # given_input = input('Enter Playlist ID or URL')
    # for testing
    given_input = 'https://www.youtube.com/watch?v=yD0_1DPmfKM&list=PLQVvvaa0QuDe9nqlirjacLkBYdgc2inh3&index=1'
    pattern = re.compile(r'youtube')
    Playlist = None
    if pattern.search(given_input):
        Playlist = YTPlaylistInfo.from_url(given_input)
    else:
        Playlist = YTPlaylistInfo.from_id(given_input)

    total_duration = Playlist.getTotalDuration()
    most_long = Playlist.sortbyDuration(rev=False)
    most_liked = Playlist.sortbyLikes()
    most_disliked = Playlist.sortbyDislikes()
    most_viewed = Playlist.sortbyViews()
    alphabetically = Playlist.sortbyTitle()
    print(total_duration)
    for video in most_long:
        print(Playlist.getVideoTitle(video), Playlist.getVideoDuration(video))
    # print('Longest video is :', Playlist.getVideoTitle(k := next(most_long)), 'with a play time of', Playlist.getVideoDuration(k))
    print('Most Viewed Video', Playlist.getVideoTitle(k := next(most_viewed)), '\t Views : ', Playlist.getNumberOfViews(k))
    print('Most Liked Video', Playlist.getVideoTitle(k := next(most_liked)), '\t Likes : ', Playlist.getNumberOfLikes(k))
    print('Most Disliked Video', Playlist.getVideoTitle(k := next(most_disliked)), '\t Dislikes : ', Playlist.getNumberOfDislikes(k))
