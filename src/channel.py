import json
import os
from typing import Any

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_info = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel_info['items'][0]['snippet']['title']
        self.description = self.channel_info['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__channel_id
        self.subscriber_count = int(self.channel_info['items'][0]['statistics']['subscriberCount'])
        self.video_count = self.channel_info['items'][0]['statistics']['videoCount']
        self.view_count = self.channel_info['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    @property
    def channel_id(self) -> str:
        """Геттер для channel_id. Возвращает channel_id"""
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_info, indent=2, ensure_ascii=False))

    def to_json(self, name_file: str) -> None:
        """Сохраняет в файл значения атрибутов экземпляра класса Channel"""
        with open(name_file, 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.__dict__, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls) -> Any:
        """Метод класса возвращающий объект для работы с YouTube API"""
        __api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=__api_key)
