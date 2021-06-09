import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from YTPlaylist import YTPlaylistInfo
# import datetime

# src = input('Enter Playlist ID or link: ')
# print()

pl = YTPlaylistInfo.from_url('https://www.youtube.com/watch?v=yD0_1DPmfKM&list=PLQVvvaa0QuDe9nqlirjacLkBYdgc2inh3&index=1')
videos_list = pl.videos
videos = {
    'Title': [], 'Duration': [], 'Views': [],
    'Likes': [], 'Dislikes': [], 'Length': [],
    'Id': [], 'Link': [], 'Like/Dislike': []
}

for video in videos_list:
    Title = pl.getVideoTitle(video)
    Duration = pl.getVideoDuration(video)
    Id = pl.getVideoID(video)
    Link = pl.getVideoLink(video)
    Views = pl.getNumberOfViews(video)
    Likes = pl.getNumberOfLikes(video)
    Dislikes = pl.getNumberOfDislikes(video)
    Length = pl.getVideoLength(video)
    L_D = int(Likes) / int(Dislikes) if Likes != 'unknown' and Dislikes != 'unknown' else np.nan
    videos['Title'].append(Title if Title != 'unknown' else np.nan)
    videos['Duration'].append(Duration if Duration != 'unknown' else np.nan)
    videos['Id'].append(Id if Id != 'unknown' else np.nan)
    videos['Views'].append(int(Views) if Views != 'unknown' else np.nan)
    videos['Likes'].append(int(Likes) if Likes != 'unknown' else np.nan)
    videos['Dislikes'].append(int(Dislikes) if Dislikes != 'unknown' else np.nan)
    videos['Length'].append(Length if Length != 'unknown' else np.nan)
    videos['Link'].append(Link if Link != 'unknown' else np.nan)
    videos['Like/Dislike'].append(L_D)

print(pl.getTotalDuration())

df = pd.DataFrame(videos)
print(df[['Title', 'Duration']])

# plotting
fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

plt.style.use('dark_background')

# Graph for Views - Likes
filt = (df['Views'] != np.nan) & (df['Likes'] != np.nan)

ax1.scatter(
    df[filt]['Views'],
    df[filt]['Likes'],
    linewidth=1, alpha=0.69)
ax1.set_title('Likes to Views Comparison')
ax1.set_xlabel('Views')
ax1.set_ylabel('Likes')

# Graph for Views - Duration
filt = (df['Views'] != np.nan) & (df['Length'] != np.nan)
k = df[filt][['Length', 'Views']].sort_values('Length')
ax2.scatter(k['Length'], k['Views'], linewidth=1, alpha=0.69)

# ax2.set_yticks(np.arange(0, np.amax(k['Views'].values), 10))
ax2.set_title('Length to Views Comparison')
ax2.set_xlabel('Length')
ax2.set_ylabel('Views')

plt.show()
