import os
import logging
import argparse
from pytube import Playlist, YouTube
from tqdm import tqdm
from yt_video_text_md import YouTubeTranscriptProcessor
from yt_video_text_md import AudioTranscriber
import asyncio

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
_logger = logging.getLogger(__name__)


class YTVideoTextMD:
    def __init__(self, url: str, output_dir: str = '.', default_md_file_name: str = "yt_video_text_", audio_output_dir: str = "/tmp") -> None:
        self.url = url
        self.output_dir = output_dir
        self.audio_output_dir = audio_output_dir
        self.current_dir = os.path.abspath(self.output_dir)
        self.default_md_file_name = default_md_file_name
        self.video_list = []
        try:
            self.video_list = self.get_video_ids_from_url(url)
            asyncio.run(self.save_video_to_md())
        except Exception as e:
            _logger.error(f"An error occurred: {e}")

    def get_video_ids_from_url(self, url: str) -> list:
        video_list = []

        try:
            if 'playlist' in url:
                playlist = Playlist(url)
                video_list = [(video.video_id, video.title, index + 1) 
                              for index, video in enumerate(playlist.videos)]
            elif 'watch?v=' in url:
                yt = YouTube(url)
                video_id = url.split('watch?v=')[-1]
                video_list = [(video_id, yt.title, 1)]

            if not video_list:
                raise ValueError("No valid video or playlist found in the URL.")

        except Exception as e:
            _logger.error(f"Failed to get video IDs from URL: {e}")
            raise

        return video_list

    async def save_video_to_md(self) -> None:
        tasks = []
        for video_id, video_title, video_number in self.video_list:
            file_name = f"{self.default_md_file_name}{video_number}.md"
            file_path = os.path.join(self.current_dir, file_name)
            tasks.append(self.process_video(video_id, video_title, file_path))
        
        await asyncio.gather(*tasks)

    async def process_video(self, video_id, video_title, file_path):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f"# {video_title}\n\n")

                transcript = YouTubeTranscriptProcessor(video_id).fetch_transcript
                
                if transcript:
                    text = " ".join(entry['text'] for entry in transcript)
                    file.write(text + "\n")
                else:
                    transcriber = AudioTranscriber(video_id, self.audio_output_dir)
                    text = await transcriber.fetch_text()
                    if text:
                        file.write(text + "\n")
                    else:
                        file.write("No content available.\n")
                
                _logger.info(f'File created: {file_path}')
        
        except Exception as e:
            _logger.error(f"Error processing video ID {video_id}: {e}")


def parse_args():
    parser = argparse.ArgumentParser(description='Fetch YouTube video transcripts and save them to markdown files.')
    parser.add_argument('-u', '--url', required=True, help='URL of the YouTube playlist or video.')
    parser.add_argument('-d', '--directory', default='.', help='Directory to save the markdown files.')
    parser.add_argument('-f', '--filename', default='yt_video_text_', help='Default prefix for markdown file names.')
    parser.add_argument('-ad', '--audio_directory', default='.', help='Directory to save the audio files.')

    return parser.parse_args()

def main():
    args = parse_args()
    YTVideoTextMD(url=args.url, output_dir=args.directory, default_md_file_name=args.filename, )

if __name__ == "__main__":
    main()
