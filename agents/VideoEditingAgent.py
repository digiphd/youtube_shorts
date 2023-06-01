
from loguru import logger
import subprocess
from agents.tools.transcibe import transcribe_audio
from agents.tools.instance_dir import create_temp_folder, remove_temp_folder
import os

def add_captions(input_video: str, caption_file: str, output_video: str) -> None:
    """
    Add captions to a video using FFmpeg when not animated, and using Moviepy for animated text.

    :param input_video: The path to the input video file.
    :param output_video: The path to the output video file.
    :param animated: If True, use Moviepy to create animated text.
    """
    logger.info("Generating captions for short")
    transcribe_audio(input_video, srt_path=caption_file, srt=True)
    subprocess.call(['ffmpeg', '-y', '-i', input_video, '-vf',
                         f'subtitles={caption_file}:force_style=\'Fontfile=Arial.ttf,Fontsize=20,PrimaryColour=&H00FFFF,BorderStyle=1,OutlineColour=&H000000,Outline=2, Bold=1,MarginV=50\'',
                         '-c:v', 'libx264', '-c:a', 'copy', output_video])
    
def crop_video(input_video: str, segment, output_video: str) -> None:
    """
    Crop the landscape video to center portrait suited for YouTube Shorts.

    :param input_video: The path to the input video file.
    :param output_video: The path to the output video file.
    """

    logger.info("Cropping video for YouTube Shorts")

    subprocess.call(['ffmpeg', '-y', '-i', input_video,  "-ss", str(segment['start']), "-t", str(segment['end'] - segment['start']+1), '-vf',
                     'crop=ih/16*9:ih:(iw/2-ih/16*9/2):0', output_video])
    

def process_video(input_video, segments):
    logger.info('Editing Video')
    
    # Create temporary folder for storing intermediate files
    temp_folder = create_temp_folder("instance")

    input_video_folder = os.path.dirname(input_video)

    subclips = []
    for i, segment in enumerate(segments):     
        subclip_path = os.path.join(input_video_folder, f"output_short_{i}.mp4")
        subclip_tmp_path = os.path.join(temp_folder, f"subclip_{i}_temp.mp4")
        caption_file = os.path.join(temp_folder, f"subclip_captions_{i}.srt")

        # Crop and add captions to video
        crop_video(input_video, segment, subclip_tmp_path)
        add_captions(subclip_tmp_path, caption_file, subclip_path)

        subclips.append(subclip_path)
    
    # Remove temporary folder and intermediate files
    remove_temp_folder(temp_folder)