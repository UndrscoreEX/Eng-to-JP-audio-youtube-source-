
# -*- coding: utf-8 -*-
# from google.cloud import texttospeech  as tts
from google.cloud import texttospeech_v1 as tts # didnt work 
# from google.cloud import texttospeech_v1beta1  as tts # didnt work
from pydub import AudioSegment
import io
import random
from YTextractor import ssml_split_long_sentences,txt_split_long_sentences, final_check_long_sentences, get_transcript, get_video_title, translate_text, split_long_sentences
import os
import unicodedata
from google.cloud import storage


PROJECT_ID=os.getenv("PROJECT_ID")

def synthesize_from_file_japanese(video_code: str):
    print(f"launching synthesis of https://www.youtube.com/watch?v={video_code}")
    
    text_output_directory = "/home/ethan/GoogleVertexAudio/textfiles"
    audio_output_directory = "/home/ethan/GoogleVertexAudio/audiofiles"
    os.makedirs(text_output_directory, exist_ok=True)

    video_name = get_video_title(video_code).replace(' ', '_')
    english_transcript = get_transcript(video_code).replace("[ __ ]"," ").replace("&#39;","")

    original_japanese_text = translate_text(english_transcript)

    # for clean JP translation
    final_japanese_text = split_long_sentences(original_japanese_text)
    final_japanese_text =  unicodedata.normalize("NFC", final_japanese_text)
    text_output_file_path = os.path.join(text_output_directory, f"{video_name}.txt")
    # final_check_long_sentences(final_japanese_text)
    with open(text_output_file_path, "w", encoding="utf-8") as out_text_file:
        out_text_file.write(original_japanese_text)
        print(f'Translated text content written to file: {text_output_file_path}')
    

    # SSML gen
    ssml_final_japanese_text = ssml_split_long_sentences(original_japanese_text)
    # print(ssml_final_japanese_text)
    ssml_chunks = ssml_split_long_sentences(final_japanese_text)
    # for x in ssml_chunks :
    #     print( len(x.encode('utf-8')))


    # txt gen DONT DELTE
    # txt_chunks = txt_split_long_sentences(final_japanese_text)
    # for x in txt_chunks :
    #     print( len(x.encode('utf-8')))
    # ssml_output_file_path = os.path.join(text_output_directory, f"{video_name}.ssml")
    # with open(ssml_output_file_path, "w", encoding="utf-8") as out_text_file:
    #     out_text_file.write(ssml_final_japanese_text)
    #     print(f'Translated text content written to SSML and sent to file: {ssml_output_file_path}')
    
    
    # 2. Upload Txt to GCS
    txt_output_file_path = os.path.join(text_output_directory, f"{video_name}.txt")

    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket("eng_to_japanese_podcasts_ex")
    blob = bucket.blob(f"Podcast_text/{video_name}.txt")
    blob.upload_from_filename(txt_output_file_path, content_type="text/plain; charset=utf-8")

    client = tts.TextToSpeechClient()

    # txt file voices Doesnt work with SSML
    # voice_options = {
        # Chirp3-HD Voices
        # "ja-JP-Chirp3-HD-Achernar": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Achird": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Algenib": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Algieba": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Aoede": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Autonoe": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Callirrhoe": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Charon": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Despina": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Enceladus": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Erinome": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Fenrir": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Gacrux": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Iapetus": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Kore": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Laomedeia": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Leda": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Orus": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Puck": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Pulcherrima": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Rasalgethi": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Sadachbia": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Sadaltager": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Schedar": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Sulafat": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Umbriel": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Vindemiatrix": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Zephyr": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Chirp3-HD-Zubenelgenubi": tts.SsmlVoiceGender.MALE,
        # }
    
    # ssml file voices
    voice_options = {
    # chirpHD voices
    # "ja-JP-Chirp3-HD-Acrux": tts.SsmlVoiceGender.MALE,
    # "ja-JP-Chirp3-HD-Achird": tts.SsmlVoiceGender.MALE,
    # "ja-JP-Chirp3-HD-Vindemiatrix": tts.SsmlVoiceGender.FEMALE,
    # Neural2 Voices
    "ja-JP-Wavenet-A": tts.SsmlVoiceGender.MALE,
    # "ja-JP-Wavenet-B": tts.SsmlVoiceGender.FEMALE,
    "ja-JP-Wavenet-C": tts.SsmlVoiceGender.MALE,
    # "ja-JP-Wavenet-D": tts.SsmlVoiceGender.FEMALE,
    # "ja-JP-Standard-A": tts.SsmlVoiceGender.FEMALE,
    # "ja-JP-Standard-B": tts.SsmlVoiceGender.FEMALE,
    "ja-JP-Standard-C": tts.SsmlVoiceGender.MALE,
    "ja-JP-Standard-D": tts.SsmlVoiceGender.MALE,
}
    
    selected_voice_name = random.choice(list(voice_options.keys()))
    selected_gender = voice_options[selected_voice_name]
    voice = tts.VoiceSelectionParams(
        language_code="ja-JP" ,
        name=selected_voice_name,
        ssml_gender=selected_gender,
    )
    print(selected_voice_name, selected_gender)
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)
    
    audio_segments = []
    # ssml feed
    for chunk in ssml_chunks:  
        input_text = tts.SynthesisInput(ssml=chunk)
        response = client.synthesize_speech(
            input=input_text,
            voice=voice,
            audio_config=audio_config,
        )
        audio_segments.append(response.audio_content) 

    # audio_segments.append(response.audio_content) 
    # for chunk in txt_chunks:  
    #     input_text = tts.SynthesisInput(text=chunk)
    #     response = client.synthesize_speech(
    #         input=input_text,
    #         voice=voice,
    #         audio_config=audio_config,
    #     )
        # audio_segments.append(response.audio_content) 



        # dont need this because short form is sync
        # try:
        #     print("Waiting for long audio synthesis to complete...")
        #     response.result(timeout=300)
        #     print("Synthesis completed successfully! The audio file should now be in your GCS bucket.")
        
        # except Exception as e:
        #     print(f"An error occurred during long audio synthesis: {e}")

    
    combined_audio = AudioSegment.empty()
    for segment_bytes in audio_segments:
        segment = AudioSegment.from_file(io.BytesIO(segment_bytes), format="wav")
        combined_audio += segment

    # Export to local file first
    combined_audio.export(f"{audio_output_directory}/{video_name}.wav", format="wav")
    
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket("eng_to_japanese_podcasts_ex")
    blob = bucket.blob(f"Podcast_audio/{video_name}.wav")
    blob.upload_from_filename(f"/{audio_output_directory}/{video_name}.wav")
    

if __name__ == "__main__":
    videoID = input("Enter the video ID code: ")
    synthesize_from_file_japanese(videoID)
    # synthesize_from_file_japanese("ZOEaUD82GlI")
