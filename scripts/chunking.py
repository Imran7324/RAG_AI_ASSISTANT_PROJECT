import whisper
import json
import os
files=os.listdir("audios")
model=whisper.load_model("base.en")
for file in files:
    if not file.endswith(".mp3"): continue
    main_part=file.replace(".mp3","")
    topic=main_part.split("_")[0].strip()
    source=main_part.split("_")[1].split(".")[0]
    # print(f"{topic} by {source}")
    # result=model.transcribe(audio=f"audios/Top 10 Applications of Machine Learning_Simplilearn.mp3",
    #                         task="transcribe",fp16=False)
    result=model.transcribe(audio=f"audios/{file}",
                            task="transcribe",fp16=False)
    chunks=[]
    for segment in result['segments']:
        chunks.append(
            {
            "id":segment['id'],
            "start":segment['start'],
            "end":segment["end"],
            "text":segment["text"],
            "topic":topic,
            "source":source
            })
    chunks_with_metadata={
                "chunks":chunks,
                "text":result["text"]}
    with open(f"jsons/{main_part}.json", "w", encoding="utf-8") as f:
        json.dump(chunks_with_metadata,f,indent=4)
        
    