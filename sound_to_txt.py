import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def sound_to_txt(uploaded_file):
    if uploaded_file is None:
        return None

    transcript = transcribe_with_diarize(uploaded_file)
    segments_info = extract_segments(transcript)
    output = {"segments": segments_info}
    return json.dumps(output, ensure_ascii=False, indent=2)


def transcribe_with_diarize(uploaded_file):
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-transcribe-diarize",
        file=uploaded_file,
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
