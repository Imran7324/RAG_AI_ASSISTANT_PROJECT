import os
import subprocess
files=os.listdir("videos")
for file in files:

    if "___" not in file: continue # Faltu files ko skip karne ke liye

    # 1. Topic nikalne ka safer tareeka
    # Pehle '___' par split karo taaki uploader alag ho jaye
    main_content = file.split('___')[0]
    
    # Ab '｜' ya '-' par split karke pehla word lo
    # .strip() se extra spaces hat jayenge
    topic = main_content.split('｜')[0].split('-')[0].strip()
    
    # Emojis hatane ke liye (Optional but recommended)
    topic = topic.replace('🔥', '').strip()

    # 2. Source nikalna (Aapka logic sahi hai)
    source = file.split('___')[1].split('.')[0]
    
    # print(f"{topic} by {source}")
    
    # Ab yahan aap subprocess.run chala sakte hain

    # # print(file)
    # topic=file.split(' ｜ ')[0]
    # print(topic)
    # source=file.split('___')[1].split('.')[0]
    # print(source)
    # # word=["Deep Learning", "Machine Learning", "Python"]
    # cleaned_name=file.replace('_',' ')
    # domain=[d for d in word if d in cleaned_name]
    # print(topic,domain, source)
    
    subprocess.run(["ffmpeg","-i",f"videos/{file}",f"audios/{topic}_{source}.mp3"])