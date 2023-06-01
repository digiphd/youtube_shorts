# YouTube Shorts Multi-Agent Processing System

This project contains a multi-agent system to process landscape talking head videos, transcribe speech into captions, crop and adjust videos for YouTube Shorts / Reels format. The system is developed as a solution for the "Coding at the Beach Meetup Challenge."

This is in no way complete code. It was built just for fun at a social event over a couple of hours.

## Assumptions
1. The input video is mostly spoken dialog
2. The input video is in landscape mode contains a talking head in the center

## List of Agents

1. FileMonitoringAgent: Monitors a folder for new video files and processes them concurrently.
2. TranscriptionAgent: Transcribes the audio from the video files using OpenAI Whisper tiny model (running locally) and finds interesting video segments and their timestamps using NLP.
3. VideoEditingAgent: Crops the video for YouTube Shorts format, adds captions to videos, and generates the final output files.

## Requirements

The project requires Python 3.6+ and uses the following libraries and APIs:

- openai
- watchdog
- loguru
- Levenshtein
- backoff
- MoviePy
- FFmpeg

## Setup
1. Clone the repository and install the required libraries using `pip install -r requirements.txt`.
2. Set up environment variable for OpenAI: `export OPENAI_API_KEY '<your-key>'` 

## Running the System

- Run the `main.py` with a folder path as an argument to monitor for new video files. e.g. `python main.py "<existing-folder-to-watch>"`
- Drop the video files in the folder, and the system automatically processes them and create the shorts with captions.

## TODO Wishlist
- Make the input folder if it doesn't exist
- Better exception handling and logging
- Better handling of tempory files
- Create youtube meta data (title, description, tags and hashtags) with GPT
- More advanced editing of the original input video based on the script and VAD
- Maybe write a blog, tweet and linkedin post with GPT from the transcript