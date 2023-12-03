from src.channel import APIMixin


class Video(APIMixin):

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        youtube = APIMixin.get_service()
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()

        self.video_title: str = video_response['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch?v=' + self.video_id
        self.view_count: int = video_response['items'][0]['statistics']['viewCount']
        self.like_count: int = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.video_title}', {self.url}, {self.view_count}, {self.like_count})"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
