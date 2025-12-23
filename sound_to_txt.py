import os
import json
from dotenv import load_dotenv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



def select_audio_file():
    root = Tk()
    root.withdraw()
    root.update()

    file_path = askopenfilename(
        title="오디오 파일을 선택하세요",
        filetypes=[("Audio Files", "*.mp3 *.mp4 *.mpeg *.mpga *.m4a *.wav")]
    )
    root.destroy()
    if not file_path:
        return None
    return file_path

def transcribe_with_diarize(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe-diarize",
            file=audio_file,
            response_format="diarized_json",
            chunking_strategy="auto",
        )
    return transcript

def extract_segments(transcript_obj):
    segments_info = []
    for idx, seg in enumerate(transcript_obj.segments, start=1):
        segments_info.append({
            "번호": idx,
            "시작": round(float(seg.start), 2),
            "끝": round(float(seg.end), 2),
            "발화자": seg.speaker,
            "대화 내용": seg.text
        })
    return segments_info

def sound_to_txt():
    path = select_audio_file()
    if not path:
        return None

    transcript = transcribe_with_diarize(path)
    segments_info = extract_segments(transcript)
    output = {"segments": segments_info}
    return json.dumps(output, ensure_ascii=False, indent=2)
