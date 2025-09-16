# -*- coding: utf-8 -*-
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from google.cloud import translate_v2 as translate
import os
from dotenv import load_dotenv
load_dotenv()
YOUTUBE_API_KEY = os.getenv("API_KEY")
max_bytes = 600

def get_transcript(videoCode:int): 
    print('Pulling the transcript')
    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(videoCode)
    full_text = " ".join([x.text for x in fetched_transcript])
    return full_text


def get_video_title(video_id:int):
    print("getting video title")
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()

    if "items" in response and response["items"]:
        title = response["items"][0]["snippet"]["title"]
        print('Youtube video: ',title)
        return title
    else:
        return "Video not found or API error."
    
def translate_text(text_to_translate):
    print('Translating to Japanese')
    translate_client = translate.Client()

    result = translate_client.translate(
        values=text_to_translate, 
        target_language='ja',
        source_language='en'
    )
    final_result = result['translatedText'].replace(' \n',' ').replace(".","。 ").replace("&#39;","")
    return final_result

def ssml_split_long_sentences(text: str) -> str:
    max_chars=4000
    chunks = []
    current_chunk = ""
    sentences = text.replace(" ",'').split('。')
    for line in sentences:
        if len(current_chunk) + len(line) + 10 < max_chars:
            chunks.append(f"<speak> <s>{current_chunk}。</s></speak>")
            current_chunk = line
        else:
            current_chunk += f"<s>{line}。</s><break time='500ms'/>"    
    return chunks

def txt_split_long_sentences(text: str) -> str:
    max_chars=4000
    chunks = []
    current_chunk = ""
    sentences = text.replace(" ",'').split('。')
    for line in sentences:
        if len(current_chunk) + len(line) + 10 < max_chars:
            chunks.append(f"{current_chunk}。")
            current_chunk = line
        else:
            current_chunk += f"{line}。"    
    return chunks

# not needed if im doing smaller SSML chunks
def split_long_sentences(text: str) -> str:
    text_to_process = text
    check_is_needed = True
    if len(text_to_process.encode('utf-8')) <= max_bytes:
        return text_to_process

    final_text = ""
    while check_is_needed:
        break_points_inserted = 0
        all_sentences = text_to_process.split('。')
        print('going through a loop to check all sentences')
        
        for sentence in all_sentences:
            if len((sentence+"。").encode('utf-8')) < max_bytes:
                final_text+=f'{sentence}。'
            else:
                broken_up_text = sentence.split('、')
                for i,chunk in enumerate(broken_up_text):
                    
                    if i<len(broken_up_text)-1 and len((chunk+"。").encode('utf-8'))+ len(broken_up_text[i+1].encode('utf-8')) < max_bytes:
                        final_text += chunk+"、"

                    elif i<len(broken_up_text)-1 and len((chunk+"。").encode('utf-8'))+ len(broken_up_text[i+1].encode('utf-8')) >= max_bytes:
                        
                        final_text += (chunk+"。 ")
                        break_points_inserted +=1

                    elif i==len(broken_up_text)-1:
                        final_text += (chunk+"。 ")

                    elif len(chunk.encode('utf-8')) > max_bytes:
                        print('one single chunk is too long and cant be logically split with this. this is the chunk', chunk)

                    else:
                        print('++++++++++something unforseen +++++++++++++')
        text_to_process = final_text
        if not break_points_inserted: 
            check_is_needed = False 
    # print(final_text)
    return final_text
        
def final_check_long_sentences(text: str) -> None:
    sentences = text.split('。')
    long_sentences_found = False
    # print(f"Checking {len(sentences)} sentences for byte length > 400...")
    
    for i, sentence in enumerate(sentences):
        full_sentence = sentence + '。'
        byte_length = len(full_sentence.encode('utf-8'))
        
        if byte_length > max_bytes:
            print("-" * 40)
            print(f"Sentence {i+1} is too long:")
            print(f"  Byte Length: {byte_length} bytes")
            print(f"  Sentence: {full_sentence.strip()}")
            long_sentences_found = True
    
    if not long_sentences_found:
        print("-" * 40)
        print("All sentences are within the byte limit.")
    else:
        print("-" * 40)
        print("Please split the long sentences using the provided functions before synthesis.")
