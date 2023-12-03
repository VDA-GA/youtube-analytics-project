import datetime

import isodate

from src.channel import APIMixin


class PlayList(APIMixin):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = "https://www.youtube.com/playlist?list=" + playlist_id
        self.info = (
            APIMixin.get_service()
            .playlists()
            .list(id=playlist_id, part="snippet")
            .execute()
        )
        self.title = self.info["items"][0]["snippet"]["title"]
        self.playlist_videos = (
            APIMixin.get_service()
            .playlistItems()
            .list(
                playlistId=playlist_id,
                part="contentDetails",
                maxResults=50,
            )
            .execute()
        )

    @property
    def total_duration(self):
        total_duration = datetime.timedelta(0)

        video_ids = [
            video["contentDetails"]["videoId"]
            for video in self.playlist_videos["items"]
        ]
        video_response = (
            APIMixin.get_service()
            .videos()
            .list(part="contentDetails,statistics", id=",".join(video_ids))
            .execute()
        )
        for video in video_response["items"]:
            iso_8601_duration = video["contentDetails"]["duration"]
            total_duration += isodate.parse_duration(iso_8601_duration)
        return total_duration

    def show_best_video(self):
        video_ids = [
            video["contentDetails"]["videoId"]
            for video in self.playlist_videos["items"]
        ]
        video_response = (
            APIMixin.get_service()
            .videos()
            .list(part="contentDetails,statistics", id=",".join(video_ids))
            .execute()
        )
        video_like = 0
        best_video = None
        for video in video_response["items"]:
            if int(video["statistics"]["likeCount"]) > video_like:
                video_like = int(video["statistics"]["likeCount"])
                best_video = "https://youtu.be/" + video["id"]
        return best_video
