import requests

# Set the key used to query the YouTube API
key = "KEY"

# Specify the name of the channel to query - remember to drop the leading @ sign
channel = "NTFAQGuy" # the very reason that I wrote this script!

# Set the location of the CSV file to write to
csv = "C:\\videos.csv" # Windows path

try:
    # Retrieve the channel id from the username (channel variable) - which is required to query the videos contained within a channel
    url = "https://youtube.googleapis.com/youtube/v3/channels?forUsername=" + channel + "&key=" + key
    request = requests.get(url)
    channelid = request.json()["items"][0]["id"]

except:
    # if this fails, perform a channel search instead. Further documentation on this: https://developers.google.com/youtube/v3/guides/working_with_channel_ids
    url = "https://youtube.googleapis.com/youtube/v3/search?q=" + channel + "&type=channel" + "&key=" + key
    request = requests.get(url)
    channelid = request.json()["items"][0]["id"]["channelId"]

# Create the playlist id (which is based on the channel id) of the uploads playlist (which contains all videos within the channel) - uses the approach documented at https://stackoverflow.com/questions/55014224/how-can-i-list-the-uploads-from-a-youtube-channel
playlistid = list(channelid)
playlistid[1] = "U"
playlistid = "".join(playlistid)

# Query the uploads playlist (playlistid) for all videos and writes the video title and URL to a CSV file (file path held in CSV variable)
lastpage = "false"
nextPageToken = ""

while lastpage:
    videosUrl = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&playlistId=" + playlistid + "&pageToken=" + nextPageToken + "&maxResults=50" + "&fields=items(contentDetails(videoId%2CvideoPublishedAt)%2Csnippet(publishedAt%2Ctitle))%2CnextPageToken%2CpageInfo%2CprevPageToken%2CtokenPagination&key=" + key
    request = requests.get(videosUrl)
    videos = request.json()
    for video in videos["items"]:
        f = open(csv,"a")
        f.write(video["snippet"]["title"].replace(",","") + "," + "https://www.youtube.com/watch?v=" + video["contentDetails"]["videoId"] + "\n")
        f.close()
    try: # I'm sure there are far more elegant ways of identifying the last page of results!
        nextPageToken = videos["nextPageToken"]
    except:
        break
