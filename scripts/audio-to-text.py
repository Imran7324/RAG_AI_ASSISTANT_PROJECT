import whisper
import json
# The default setting (which selects the turbo model) works well for transcribing English.
# However, the turbo model is not trained for translation tasks. If you need to translate non-English speech into English,
# use one of the multilingual models (tiny, base, small, medium, large) instead of turbo.
model=whisper.load_model("base.en")
result=model.transcribe(audio="audios/Top 10 Applications of Machine Learning_Simplilearn.mp3",task="transcribe")
# print(result)
chunks=[]
for segment in result['segments']:
    chunks.append({
        "id":segment['id'],
        "start":segment['start'],
        "end":segment["end"],
        "text":segment["text"]
        })
with open("chunks.json", "w",encoding='utf-8') as f:
    json.dump(chunks,f,indent=4)