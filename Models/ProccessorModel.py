from PyQt5 import QtCore, QtWidgets
from pytube import Stream
import youtube_dl

class ProccessorModel(QtCore.QObject):
    length = QtCore.pyqtSignal(str, str, str)
    rec = QtCore.pyqtSignal(int)

    def __init__(self, title=None, url=None, path=None):
        super().__init__()
        self.title = title
        self.url = url
        self.path = path

    def run(self):
        dl = youtube_dl.YoutubeDL()
        result = dl.extract_info(self.url, download=False)
        if 'entries' in result:
            video = result['entries'][0]
        else:
            video = result
        video_title = video['title']
        video_description = video['description']
        video_thumbnail = video['thumbnail']
        self.length.emit(video_title, video_description, video_thumbnail)

    def download(self):
        dl_options = {'format': 'best', 'outtmpl': self.path + '/' + self.title + '.mp4', 'progress_hooks': [self.progress]}
        with youtube_dl.YoutubeDL(dl_options) as dl:
            dl.download([self.url])

    def progress(self, percent):
        if percent['status'] == 'downloading':
            result = round(percent['downloaded_bytes'] / percent['total_bytes'] * 100, 1)
            self.rec.emit(result)

    def on_progress(self, stream: Stream, bytes_remaining: int) -> None:
        filesize = stream.filesize
        bytes_remaining = filesize - bytes_remaining
        percent = round(100 * bytes_remaining / float(filesize), 1)
        self.rec.emit(percent)