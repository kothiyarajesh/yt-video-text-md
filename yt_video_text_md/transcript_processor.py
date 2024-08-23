import os
import logging
from youtube_transcript_api import YouTubeTranscriptApi

logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Log message format
)
_logger = logging.getLogger(__name__)

class YouTubeTranscriptProcessor:
    def __init__(self, video_id: str, languages: list[str] = None):
        """
        Initialize the processor with a YouTube video ID and preferred languages.

        Args:
            video_id (str): The YouTube video ID.
            languages (list[str], optional): List of language codes to fetch the transcript in. 
                                              Defaults to a list of English variants if not provided.
        """
        self.video_id = video_id
        self.languages = languages or [
            "en", "en-US", "en-GB", "en-CA", "en-AU", "en-NZ", "en-IE", "en-IN", 
            "en-PH", "en-ZA", "en-SG", "en-MY", "en-TT", "en-BZ"
        ]

    @property
    def fetch_transcript(self) -> list[dict] | None:
        """
        Fetch the transcript for the initialized video ID in the preferred languages.

        Returns:
            list[dict] | None: The transcript data as a list of dictionaries, or None if an error occurs.
        """
        try:
            transcript = YouTubeTranscriptApi.get_transcript(self.video_id, languages=self.languages)
            return transcript
        except Exception as e:
            _logger.error(f"An error occurred while fetching the transcript for video {self.video_id}: {e}")
            return None
