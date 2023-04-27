import os
from pytube import YouTube
import openai


class AudioTranscriber:
    def __init__(self, url, audio_path):
        self.url = url
        self.audio_path = audio_path
        openai.api_key = 'your api key'

    def download_audio(self):
        yt = YouTube(self.url)
        video = yt.streams.filter(only_audio=True).first()

        download_path = 'audios/'
        if not os.path.isdir(download_path):
            os.makedirs(download_path)
        out_file = video.download(output_path=download_path)
        base, ext = os.path.splitext(out_file)
        new_file = f"{base}.mp3"
        os.rename(out_file, new_file)
        file_name = os.path.basename(new_file)
        file_path = os.path.join(download_path, file_name)
        # raw = repr(file_path)[1:-1]
        return file_path
        # return raw

    def transcribe_audio(self, file):
        transcription = openai.Audio.transcribe("whisper-1", file)
        return transcription
        # model = whisper.load_model("base", device='cpu')
        # transcription = model.transcribe(self)
        # return transcription["text"]

    def transcribe(self):
        try:
            audio_path = self.download_audio()
            audio_data = open(audio_path, "rb")
            transcription = self.transcribe_audio(audio_data)
            audio_data.close()
            os.remove(audio_path)
            return transcription
        except Exception as e:
            print("Error occurred: ", e)
            return "cannot transcribe"


if __name__ == "__main__":
    # Test YouTube crawler
    url = input("Enter YouTube URL: ")
    transcriber = AudioTranscriber(url, "audios/")
    print("\n\n", transcriber.transcribe());
