import openai
import VideoEditingAgent
import os
from tools.transcibe import transcribe_audio
from loguru import logger
import backoff
import json
import datetime as datetime
from Levenshtein import distance
import re
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

SYSTEM_PROMPT = "You are exceptional at scaning through text and finding the most suitable text which is could be interesting to people, your skill is unparalleled. Your comprehensive knowledge of the english language and mastery of story telling enable you to find captivating text that intrigue and draw people in. That said the last thing you want to do is mislead viewers by stating unfactual things, or misrepresenting the any reference material you may be provided."


@backoff.on_exception(backoff.expo, (openai.error.RateLimitError, openai.error.APIError, openai.error.ServiceUnavailableError, openai.error.APIConnectionError))
def chat_completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def find_interesting_points(script, N=5):
    """
    Used to generate a list of N interesting points from a given script using GPT-4
    :param script_file: txt file
    :param N: number of points
    :return: list of string points
    """
    logger.info('Finding Interesting Points:'+str(N))

    # Split text into sentences
    sentences = script.split('.')
    sentences = [sentence.strip() + "." for sentence in sentences if len(sentence.split()) >= 15]

    # If the script is over 2000 words, break the script up into chunks of complete sentences no longer than 2000 words.
    chunks = []
    current_chunk = ""
    current_chunk_words = 0
    for sentence in sentences:
        sentence_words = len(sentence.split())
        if current_chunk_words + sentence_words <= 2000:
            current_chunk += sentence
            current_chunk_words += sentence_words
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_chunk_words = sentence_words
    if current_chunk:
        chunks.append(current_chunk.strip())

    interesting_points = []
    openai.api_key = OPENAI_API_KEY
    
    for chunk in chunks:
        # Find interesting points for each chunk
        prompt = f"Slice the below text into {N} most interesting bits of information. The output should be exact slices of the text containing two or more sentences that appear one after the other, and each should be longer then 30 words but less than 120 words. If the text is to short just return the first sentence and nothing else: \n\n"
        choices = "### Sentences: \n" + "\n".join(chunk.split('.'))

        messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt+ choices}
                ]

        completions = chat_completions_with_backoff(model="gpt-4", messages=messages, max_tokens=50,
                                           temperature=0.7)
        response_str = completions.choices[0].message.content.strip()

        response_str = response_str.strip().split("\n")
       
        interesting_points += response_str
 
    # If the script is over 2000 words, break the script up into chunks to find interesting points.
    interesting_points = interesting_points[:N]
    return interesting_points

def get_phrase_timing(interesting_points, word_timings):
    
    segments = []
    for input_string in interesting_points:
  
        input_sentences = input_string.split('.')  # split the input string into sentences
        sentence_segments = []
        sentences_pieces = []
        for input_sentence in input_sentences:
            start_time = None
            end_time = None
            last_end_time = None
            sentence = ""
            word_count = 0
            for word in word_timings:
                content = word['word']
                start = float(word['start_time'])
                end = float(word['end_time'])
                if sentence == "":
                    start_time = start
                sentence += content + " "
                last_end_time = end
                word_count += 1
                if content.endswith('.') or content.endswith('!') or content.endswith('?'):
                    end_time = last_end_time
                    if distance(input_sentence.lower(), sentence.lower().strip()) < 15 and word_count > 5:
                

                        sentence_segments.append([start_time, end_time])
                        sentences_pieces.append(sentence)
                  
                    sentence = ""
                    start_time = None
                    word_count = 0

        if sentence_segments:
            segment_start = min([min(segment) for segment in sentence_segments])
            segment_end = max([max(segment) for segment in sentence_segments])
            joined_sentences = ''.join(sentences_pieces)
            segments.append({'segment': joined_sentences, 'start':segment_start, 'end':segment_end})


    return segments

def process_video(video_file_path):
   
    # Transcribe audio
    script, word_dict = transcribe_audio(video_file_path)
    # Find interesting points and timings
    interesting_points = find_interesting_points(script)
    segments = get_phrase_timing(interesting_points, word_dict)
    # Pass video and captions to the next agents
    VideoEditingAgent.process_video(video_file_path, segments)


if __name__ == "__main__":
    folder_path = "/Users/roger/Desktop/youtube_shorts/test_video.mov"
    process_video(folder_path)
   

