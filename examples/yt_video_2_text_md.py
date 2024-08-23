from yt_video_text_md import YTVideoTextMD

# Define the URL of the YouTube video you want to process (Here you can add playlist url or video url)
video_url = "https://www.youtube.com/watch?v=pzo13OPXZS4"

# Specify the directory where the output Markdown file will be saved
output_directory = "."

# Set the default name for the generated Markdown file
markdown_file_name = "yt_video_2_text_md_"

# Define the directory where temporary audio files will be stored (Audio is generated only in specific situations where a video transcript is not available.)
temporary_audio_directory = "/tmp"

# Create an instance of YTVideoTextMD with the specified parameters
YTVideoTextMD(
    url=video_url,
    output_dir=output_directory,
    default_md_file_name=markdown_file_name,
    audio_output_dir=temporary_audio_directory
)
