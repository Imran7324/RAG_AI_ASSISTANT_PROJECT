import os
import json,math
n=5
for file in os.listdir("jsons"):
    if file.endswith(".json"):
        file_path=os.path.join("jsons",file)
        with open(file_path,'r',encoding='utf-8') as f:
            data=json.load(f)
            new_chunk=[]
            num_chunk=len(data['chunks'])
            num_group=math.ceil(num_chunk/n)
            for i in range(num_group):
                start_idx=i*n
                end_idx=min((i+1)*n,num_chunk)
                chunk_group=data['chunks'][start_idx:end_idx]
                new_chunk.append({
                    "id":chunk_group[0]['id'],
                    "start":chunk_group[0]["start"],
                    "end":chunk_group[-1]['end'],
                    "topic":data['chunks'][0]['topic'],
                    "text":"".join(c['text']for c in chunk_group)
                    })   
            os.makedirs("newjsons",exist_ok=True)
            with open(os.path.join("newjsons",file),"w",encoding="utf-8") as f:
                json.dump({
                    "chunks":new_chunk,
                    "text":data['text']
                },f,indent=4)