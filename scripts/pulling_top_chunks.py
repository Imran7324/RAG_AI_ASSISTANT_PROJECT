import requests
import json, os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
def create_embeddings(text_list):
  r=requests.post("http://localhost:11434/api/embed", json={
    "model":"nomic-embed-text",
    "input":text_list
  })
  embeddings=r.json()['embeddings']
  return embeddings
my_dict=[]
jsons=os.listdir("jsons")
# print(jsons)
for json_file in jsons:
  with open(f"jsons/{json_file}","r") as f:
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
    if(i==10):
        break
  break
# print(my_dict)
df=pd.DataFrame.from_records(my_dict)
incoming_query=input("Ask a question:")
question_embedding=create_embeddings([incoming_query])[0]  
similarities=cosine_similarity(np.vstack(df['embeddings']),[question_embedding]).flatten()
print(similarities)# Example: [0.39455441 0.41792757 0.39588137 0.5271093  0.33414161 0.50162554
#  0.44355278 0.8430927  0.77514029 0.42895711 0.56525006]
print(similarities.argsort())# Will sort this [ 4  0  2  1  9  6  5  3 10  8  7] and pull top 3 similarities
max_index=similarities.argsort()[::-1][0:3]
print(max_index)
new_df=df.loc[max_index]
print(new_df[['id','text']])


