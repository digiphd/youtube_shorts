import whisper_timestamped as whisper
from loguru import logger
import os
import json
import datetime

def transcribe_audio(path, srt = True, srt_path= './script.srt', word_json = True):
    # Code to transcribe audio using OpenAI Whisper API
    logger.info("SPEECH TOOLS: Whisper Transcribing, creating SRT, and Word Timings")
    word_path = './words.json'
  
    audio = whisper.load_audio(path)

    model = whisper.load_model("tiny", device="cpu")
    result = whisper.transcribe(model, audio, language="en", condition_on_previous_text=False) 
    # result = whisper2.transcribe(model, audio, language="en")
    text = result["text"]
    
    segments = result["segments"]
    word_timings = []
    for segment in segments:
        for word in segment['words']:
            word_timings.append({
                'word': word['text'],
                'start_time': word['start'],
                'end_time': word['end']
            })

    # Save word timings to file
    if word_json:
        with open(word_path, 'w') as f:
            json.dump(word_timings, f)

   
    # Write SRT file
    if srt:
        if os.path.exists(srt_path):
            # Remove the file
            os.remove(srt_path)

        else:
            logger.error("SPEECH TOOLS: The file does not exist")
        
        # Save captions file
        index = 1
        for item in segments:
            start_time = item["start"]
            end_time = item["end"]
            text_chunks = break_into_chunks(item["text"], max_words=4)

            time_chunks = chunks_duration(start_time, end_time, len(text_chunks))
            
            with open(srt_path, 'a', encoding='utf-8') as f:
                for (chunk_start, chunk_end), chunk in zip(time_chunks, text_chunks):
                    f.write(str(index) + "\n")
                    f.write(f'{format_time(chunk_start)} --> {format_time(chunk_end)}\n')
                    f.write(chunk + "\n")
                    f.write("\n")
                    index += 1
  
    return text, word_timings


def chunks_duration(start, end, num_chunks):
    duration = end - start
    chunk_duration = duration / num_chunks
    return [(start + i * chunk_duration, start + (i + 1) * chunk_duration) for i in range(num_chunks)]

def format_time(seconds: float) -> str:
    time = datetime.timedelta(seconds=seconds)
    if '.' in str(time):
        time_base, millis = str(time).split('.')
        formatted_time = time_base + ',' + millis[:3]
    else:
        formatted_time = str(time) + ',000'
    return formatted_time

def break_into_chunks(text: str, max_words: int = 6) -> list:
    """
    Break the input text into chunks with a maximum number of words specified by max_words.

    :param text: The input text to be broken into chunks.
    :param max_words: Maximum number of words allowed in each chunk (default is 10).
    :return: A list containing the chunks of text.
    """
    words = text.split()  # Split the text into a list of words
    wrapped_text = [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    return wrapped_text