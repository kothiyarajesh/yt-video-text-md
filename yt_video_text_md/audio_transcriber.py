import os
import yt_dlp
import whisper
import logging
import asyncio
import aiofiles  # Async file operations
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
_logger = logging.getLogger(__name__)

class AudioTranscriber:
    def __init__(self, video_id: str, output_dir: str = '/tmp', audio_format: str = 'mp3') -> None:
        """
        Initializes the AudioTranscriber with video ID, output directory, and audio format.

        :param video_id: YouTube video ID to download audio from.
        :param output_dir: Directory to save the audio file. Default is the current directory.
        :param audio_format: Format for the audio file. Default is 'mp3'.
        """
        self.video_id = video_id
        self.output_dir = output_dir
        self.audio_format = audio_format
        self.audio_file = os.path.join(self.output_dir, f'{video_id}_audio.{self.audio_format}')
        self.model = whisper.load_model("base")

    async def download_audio(self) -> None:
        """
        Downloads the audio from the YouTube video specified by video_id asynchronously.

        Uses yt-dlp to fetch the best audio format available and converts it to the specified audio format.
        """
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.output_dir, f'{self.video_id}_audio.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.audio_format,
                    'preferredquality': '192',
                }],
            }

            # Run yt-dlp in a thread to avoid blocking the async loop
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as pool:
                await loop.run_in_executor(pool, lambda: yt_dlp.YoutubeDL(ydl_opts).download([f'https://www.youtube.com/watch?v={self.video_id}']))
            
            _logger.info("Audio downloaded successfully.")
        
        except Exception as e:
            _logger.error(f"Failed to download audio: {e}")
            raise

    async def transcribe_audio(self) -> str:
        """
        Transcribes the downloaded audio file to text asynchronously.

        :return: The transcribed text from the audio file.
        :raises FileNotFoundError: If the audio file does not exist.
        """
        try:
            if not os.path.exists(self.audio_file):
                raise FileNotFoundError(f"The audio file {self.audio_file} does not exist.")
            
            # Run the Whisper model transcription in a thread to avoid blocking the async loop
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, lambda: self.model.transcribe(self.audio_file))
            _logger.info("Audio transcription completed successfully.")
            return result["text"]
        
        except FileNotFoundError as fnf_error:
            _logger.error(fnf_error)
            return None
        
        except Exception as e:
            _logger.error(f"Failed to transcribe audio: {e}")
            return None

    async def fetch_text(self) -> str:
        """
        Downloads the audio and transcribes it asynchronously.

        :return: The transcribed text from the audio file.
        """
        try:
            await self.download_audio()
            transcription = await self.transcribe_audio()
            return transcription
        
        except Exception as e:
            _logger.error(f"An error occurred while fetching text: {e}")
            return None
