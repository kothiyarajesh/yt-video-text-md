import pytest
import asyncio
from unittest.mock import patch, MagicMock
from yt_video_text_md import YTVideoTextMD

# Test the initialization and video processing
@patch('yt_video_text_md.YouTubeTranscriptProcessor')
@patch('yt_video_text_md.AudioTranscriber')
def test_yt_video_text_md(MockAudioTranscriber, MockYouTubeTranscriptProcessor):
    # Mock Playlist and YouTube
    mock_playlist = MagicMock()
    mock_video = MagicMock()
    mock_video.video_id = 'pzo13OPXZS4'
    mock_video.title = 'Test Title'
    mock_playlist.videos = [mock_video]

    mock_transcript_processor = MagicMock()
    mock_transcript_processor.fetch_transcript = [{'text': 'This is a transcript'}]
    MockYouTubeTranscriptProcessor.return_value = mock_transcript_processor

    mock_audio_transcriber = MagicMock()
    mock_audio_transcriber.fetch_text = MagicMock(return_value='This is audio text')
    MockAudioTranscriber.return_value = mock_audio_transcriber

    # Create an instance of YTVideoTextMD
    url = "https://www.youtube.com/watch?v=pzo13OPXZS4"
    output_dir = "/tmp"
    default_md_file_name = "yt_file_txt_"
    audio_output_dir = "/tmp"
    
    yt_instance = YTVideoTextMD(
        url=url,
        output_dir=output_dir,
        default_md_file_name=default_md_file_name,
        audio_output_dir=audio_output_dir
    )
    
    # Test video_list populated correctly
    assert len(yt_instance.video_list) > 0
    assert yt_instance.video_list[0][0] == 'pzo13OPXZS4'
    
    # Test that process_video is called
    with patch('yt_video_text_md.YTVideoTextMD.process_video') as mock_process_video:
        asyncio.run(yt_instance.save_video_to_md())
        assert mock_process_video.called
