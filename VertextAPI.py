
# -*- coding: utf-8 -*-
# from google.cloud import texttospeech  as tts
from google.cloud import texttospeech_v1 as tts # didnt work 
# from google.cloud import texttospeech_v1beta1  as tts # didnt work

from google.cloud.texttospeech_v1.services.text_to_speech_long_audio_synthesize import (
    TextToSpeechLongAudioSynthesizeClient,
)
from google.cloud.texttospeech_v1.types import (
    SynthesizeLongAudioRequest,
    SynthesisInputFromGcs,
    GcsSource,
    VoiceSelectionParams,
    AudioConfig,
    AudioEncoding,
)

import random
from YTextractor import ssml_split_long_sentences, final_check_long_sentences, get_transcript, get_video_title, translate_text, split_long_sentences
import os
import unicodedata
from google.cloud import storage


PROJECT_ID=os.getenv("PROJECT_ID")

def synthesize_from_file_japanese(video_code: str):
    print(f"launching synthesis of https://www.youtube.com/watch?v={video_code}")
    
    # audio_output_directory = "/home/ethan/GoogleVertexAudio"
    # os.makedirs(audio_output_directory, exist_ok=True)
    # gcs_output_uri_text ='gs://eng_to_japanese_podcasts_ex/Podcast_text/'

    text_output_directory = "/home/ethan/GoogleVertexAudio/textfiles"
    os.makedirs(text_output_directory, exist_ok=True)

    video_name = get_video_title(video_code).replace(' ', '_')
    english_transcript = get_transcript(video_code).replace("[ __ ]"," ").replace("&#39;","")
    # print(english_transcript)

    original_japanese_text = translate_text(english_transcript)
    final_japanese_text = split_long_sentences(original_japanese_text)
    final_japanese_text =  unicodedata.normalize("NFC", final_japanese_text)
    final_check_long_sentences(final_japanese_text)

    ssml_final_japanese_text = ssml_split_long_sentences(original_japanese_text)
    

    # # 1. Save SSML to local file
    # ssml_path = f"/tmp/{video_name}.ssml"
    # with open(ssml_path, "w", encoding="utf-8") as f:
    #     f.write(final_japanese_text)

    # # 2. Upload SSML to GCS
    # storage_client = storage.Client(project=PROJECT_ID)
    # bucket = storage_client.bucket("eng_to_japanese_podcasts_ex")
    # blob = bucket.blob(f"Podcast_text/{video_name}.ssml")
    # blob.upload_from_filename(ssml_path)

    # print(final_japanese_text)

    text_output_file_path = os.path.join(text_output_directory, f"{video_name}_JP.txt")
    with open(text_output_file_path, "w", encoding="utf-8") as out_text_file:
        out_text_file.write(original_japanese_text)
        print(f'Translated text content written to file: {text_output_file_path}')
    
    
    ssml_output_file_path = os.path.join(text_output_directory, f"{video_name}.ssml")
    with open(ssml_output_file_path, "w", encoding="utf-8") as out_text_file:
        out_text_file.write(ssml_final_japanese_text)
        print(f'Translated text content written to SSML and sent to file: {ssml_output_file_path}')
    
    
    # 2. Upload Txt to GCS
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket("eng_to_japanese_podcasts_ex")
    blob = bucket.blob(f"Podcast_text/{video_name}.ssml")
    blob.upload_from_filename(ssml_output_file_path, content_type="text/plain; charset=utf-8")

    gcs_output_uri_ssml = f"gs://eng_to_japanese_podcasts_ex/Podcast_text/{video_name}.ssml"
    gcs_output_uri_audio =f'gs://eng_to_japanese_podcasts_ex/Podcast_audio/{video_name}_JP.wav'
    # --- Step 5: Synthesize the Japanese text into audio ---
    client = tts.TextToSpeechLongAudioSynthesizeClient()

    # old synthesis_input when using short form tts
    # synthesis_input = tts.SynthesisInput(text=final_japanese_text)
    
    # new input option:
    gcs_source = tts.GcsSource(uris=[gcs_output_uri_ssml])
    input = tts.SynthesisInputFromGcs(gcs_source=gcs_source)


    # input  = tts.SynthesisInput(ssml=gcs_output_uri_ssml)
    # input.ssml = ssml_final_japanese_text
    # print(len(ssml_final_japanese_text.encode('utf-8')))



    # gcs_source = tts.GcsSource(uris=[f"gs://{bucket.name}/Podcast_text/{video_name}.txt"])
    # synthesis_input = tts.SynthesisInputFromGcs(gcs_source=gcs_source)

    # synthesis_input = tts.SynthesisInput(ssml_gcs_uri=gcs_input_uri)
    # print(synthesis_input)

    voice_options = {
        # Chirp3-HD Voices
        "ja-JP-Chirp3-HD-Achernar": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Achird": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Algenib": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Algieba": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Chirp3-HD-Alnilam": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Aoede": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Autonoe": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Callirrhoe": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Charon": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Despina": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Enceladus": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Erinome": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Fenrir": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Gacrux": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Iapetus": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Kore": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Laomedeia": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Leda": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Orus": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Puck": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Pulcherrima": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Rasalgethi": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Sadachbia": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Sadaltager": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Schedar": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Sulafat": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Umbriel": tts.SsmlVoiceGender.MALE,
        "ja-JP-Chirp3-HD-Vindemiatrix": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Zephyr": tts.SsmlVoiceGender.FEMALE,
        "ja-JP-Chirp3-HD-Zubenelgenubi": tts.SsmlVoiceGender.MALE,

        # # Neural2 Voices
        # "Neural2-A": tts.SsmlVoiceGender.FEMALE,
        # "Neural2-B": tts.SsmlVoiceGender.FEMALE,
        # "Neural2-C": tts.SsmlVoiceGender.MALE,
        # "Neural2-D": tts.SsmlVoiceGender.MALE,
        # "AoiNeural": tts.SsmlVoiceGender.FEMALE,
        # "DaichiNeural": tts.SsmlVoiceGender.MALE,
        # "MayuNeural": tts.SsmlVoiceGender.FEMALE,
        # "NaokiNeural": tts.SsmlVoiceGender.MALE,
        # "ShioriNeural": tts.SsmlVoiceGender.FEMALE,

        # # WaveNet Voices
        # "ja-JP-Wavenet-A": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Wavenet-B": tts.SsmlVoiceGender.FEMALE,
        # "ja-JP-Wavenet-C": tts.SsmlVoiceGender.MALE,
        # "ja-JP-Wavenet-D": tts.SsmlVoiceGender.MALE,
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
    
    # crafting the request:
    print(input)
    request = tts.SynthesizeLongAudioRequest(
        parent=f"projects/{PROJECT_ID}/locations/us-central1",
        input=input,
        audio_config=audio_config,
        voice=voice,
        output_gcs_uri=gcs_output_uri_audio,
    )
    operation = client.synthesize_long_audio(request=request)


    try:
        print("Waiting for long audio synthesis to complete...")
        operation.result(timeout=300)
        print("Synthesis completed successfully! The audio file should now be in your GCS bucket.")
    
    except Exception as e:
        print(f"An error occurred during long audio synthesis: {e}")

if __name__ == "__main__":
    # videoID = input("Enter the video ID code: ")
    # synthesize_from_file_japanese(videoID)
    synthesize_from_file_japanese("nZ1Oa_uHsLo")
