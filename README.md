
# YouTube Video to Text Markdown Converter

`yt-video-text-md` is a Python package designed to retrieve and convert YouTube video transcripts/subtitles into Markdown files. This tool is particularly useful for extracting text from entire playlists or individual videos. It leverages the `youtube-transcript-api` for direct subtitle extraction and `whisper` for audio-to-text conversion when transcripts are unavailable.

## Features

- **Playlist and Video Support:** Extracts subtitles from both individual videos and entire playlists.
- **Fallback Mechanism:** Utilizes `whisper` to transcribe audio if subtitles are not available.
- **Markdown Formatting:** Outputs transcripts in Markdown format with video titles as headers.

## Installation

### Via pip

To install the latest version directly from the GitHub repository, use:

```bash
pip install git+https://github.com/kothiyarajesh/yt-video-text-md.git
```

### Building from Source

1. Clone the repository:

    ```bash
    git clone https://github.com/kothiyarajesh/yt-video-text-md.git
    ```

2. Navigate to the project directory:

    ```bash
    cd yt-video-text-md
    ```

3. Install the package:

    ```bash
    python setup.py install
    ```

4. If installing from source, make sure to install the dependencies manually:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Python Script

Here's a simple example of how to use the `yt-video-text-md` library in a Python script:

```python
from yt_video_text_md import YTVideoTextMD

# Define the URL of the YouTube video or playlist you want to process
video_url = "https://www.youtube.com/watch?v=pzo13OPXZS4"

# Specify the directory where the output Markdown file will be saved
output_directory = "."

# Set the default name for the generated Markdown file
markdown_file_name = "yt_video_2_text_md_"

# Define the directory where temporary audio files will be stored (Used only if a transcript is not available)
temporary_audio_directory = "/tmp"

# Create an instance of YTVideoTextMD with the specified parameters
YTVideoTextMD(
    url=video_url,
    output_dir=output_directory,
    default_md_file_name=markdown_file_name,
    audio_output_dir=temporary_audio_directory
)
```

### Command-Line Interface

You can also use the package from the command line:

```bash
yt-video-text-md -u "https://www.youtube.com/playlist?list=PLMrJAkhIeNNQV7wi9r7Kut8liLFMWQOXn" -d "." -f "playlist_video_" -ad "/tmp"
```

**Options:**
- `-u` or `--url`: URL of the YouTube video or playlist.
- `-d` or `--output-dir`: Directory where the output Markdown file will be saved.
- `-f` or `--file-name`: Name for the generated Markdown file.
- `-ad` or `--audio-dir`: Directory where temporary audio files will be stored (used only if a transcript is not available).

## Notes

- **Dependencies:** This package relies on several external libraries. Ensure all dependencies are installed for optimal functionality.
- **Audio Extraction:** If a video does not have an available transcript, the script will download the video, extract the audio, and convert it to text. This process requires a stable internet connection and may be resource-intensive, especially for long videos.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
