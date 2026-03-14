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

'''Explanation:-

Chalo iska ek-ek step aur logic samajhte hain:
1. Yeh Code kar kya raha hai? (The Goal)
Abhi tak aapke JSON mein ek chunk sirf 5-8 seconds ka tha (lagbhag ek line).
Problem: Itni choti line mein pura "meaning" nahi nikalta.
Solution: Yeh code har 5 segments (n=5) ko uthakar ek bada "Super Chunk" bana raha hai. Isse LLM ko padhne ke liye zyada context milta hai aur search results better aate hain.
2. Step-by-Step Logic Breakdown:
num_group = math.ceil(num_chunk/n):
Maan lo ek video mein 103 segments hain. Agar hum 5-5 ka group banayein, toh total 103/5 = 20.6 yaani 21 groups banenge. math.ceil isliye taaki aakhiri bache hue segments bhi cover ho jayein.
Indexing Logic (start_idx & end_idx):
Jab i=0: 0 se 5 tak ke segments lega.
Jab i=1: 5 se 10 tak ke segments lega.
min((i+1)*n, num_chunk) isliye lagaya hai taaki agar segments khatam ho jayein, toh loop crash na ho.
Metadata Management:
"start": chunk_group[0]["start"]: Group ka pehla second.
"end": chunk_group[-1]['end']: Group ka aakhiri second (5th segment ka end).
"text": "".join(...): Saare 5 segments ke text ko aapas mein chipka kar ek bada paragraph bana diya.
3. Folder aur File Path kaise manage ho rahe hain?
os.path.join("jsons", file): Yeh Python ka standard tareeka hai path banane ka. Yeh ensure karta hai ki Windows (\) ya Linux (/) dono par code bina kisi error ke chale.
os.makedirs("newjsons", exist_ok=True): Yeh sabse smart line hai.
Yeh check karta hai ki kya newjsons naam ka folder hai?
Agar nahi hai, toh bana deta hai.
exist_ok=True ka matlab hai ki agar pehle se hai, toh "Error" mat dena, bas aage badho.
json.dump(...): Yeh naye "Super Chunks" ko ek nayi JSON file mein newjsons/ folder ke andar save kar deta hai, purani files ko touch kiye bina.
Why it is needed? (Kyun zaroori hai?)
Better Embeddings: Jab nomic-embed-text pura paragraph padhta hai, toh wo zyada accha "Vector" banata hai as compared to a single sentence.
Less Noise: read-chunks.py mein ab kam rows hongi (Total rows / 5), isliye similarity search 5 guna fast ho jayegi.
Human-like Answer: Jab user puchega, toh Llama 3.2 ko pura paragraph milega, toh wo adha-adhura jawab nahi dega.'''
