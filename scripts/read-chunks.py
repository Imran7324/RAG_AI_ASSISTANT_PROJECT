# import requests
# r=requests.post("http://localhost:11434/api/embeddings",json={
#                 "model":"nomic-embed-text",
#                 "prompt": "My name is Imran and I am studying data science.",
#                 "stream": False
#               })
# # print(r.json())
# embeddings=r.json()["embedding"]
# print(embeddings[0:5])
import requests
import json, os
import pandas as pd
import joblib
def create_embeddings(text_list):
  r=requests.post("http://localhost:11434/api/embed", json={
    "model":"nomic-embed-text",
    "input":text_list
  })
  embeddings=r.json()['embeddings']
  return embeddings
# a=create_embeddings(['Harry is poor', 'Imran is good'])
# print(a)
my_dict=[]
jsons=os.listdir("newjsons")
# print(jsons)
for json_file in jsons:
  with open(f"newjsons/{json_file}","r") as f:
    content=json.load(f)
  print(f"Creating embeddings for {json_file}")
  # A list comprehension to get the embeddings text for calculating embeddings for each text of the chunks
  embedding_text=[c['text'] for c in content['chunks']]
  # print(embedding_text)
  cal_embedding=create_embeddings(embedding_text)
  for i,chunk in enumerate(content['chunks']):
    #Now, we will add the embeddings key-value pair in each chunks of the json files
    chunk['embeddings']=cal_embedding[i]
    my_dict.append(chunk)
  
# print(my_dict)
df=pd.DataFrame.from_records(my_dict)
joblib.dump(df,'df_embeddings.joblib') # This saves the Pandas Dataframe and into a joblib file and remain persists.
