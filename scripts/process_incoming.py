import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import joblib,requests
def create_embeddings(text_list):
  r=requests.post("http://localhost:11434/api/embed", json={
    "model":"nomic-embed-text",
    "input":text_list
  })
  embeddings=r.json()['embeddings']
  return embeddings
def inference(prompt):
  r=requests.post("http://localhost:11434/api/generate", json={
    "model":"llama3.2",
    "prompt":prompt,
    "stream":False
  })
  response=r.json()['response']
  return response
  
df=joblib.load('df_embeddings.joblib')# We will load the embedding files which contains the DataFrame of all the files.
incoming_query=input("Ask a question:")
question_embedding=create_embeddings([incoming_query])[0]
#Now, will use cosine similarity to calculate the similarties between the question embedding and other embeddings
similarities=cosine_similarity(np.vstack(df['embeddings']),[question_embedding]).flatten()
# print(similarities)# Example: [0.39455441 0.41792757 0.39588137 0.5271093  0.33414161 0.50162554
#  0.44355278 0.8430927  0.77514029 0.42895711 0.56525006]
# print(similarities.argsort())# Will sort this [ 4  0  2  1  9  6  5  3 10  8  7] and pull top 3 similarities
top_results=3
max_index=similarities.argsort()[::-1][0:top_results]
# print(max_index)
new_df=df.loc[max_index]
prompt=f'''I am teaching Machine Learning and its related topics. Here, are the video subtitle chunks containing video topic, video
id, start time in seconds and end time in seconds of each particular chunk and at last the text at that time.
{new_df[['topic','id','start','end','text']].to_json()}
-----------------------------------------
{incoming_query}
User has asked this question related to the Machine Learning Course. Now, you have to answer the timestamps of where the asked
topic is taught in the course i.e,the start time and the end time,from where user can get to that topic easily.Convert the seconds
into minutes for the resulted topic video.
Give Response in this format:
Give the video topic name also.
Start: <mm:ss>
End: <mm:ss>
You may also give some information related to that questions that is its definiton and example.
Note, you do not habe to give the chunks information in the response. Just give the related information.
If user asks unrelated question, ask user that you can only answer the questions related to this Machine Learning Course.
'''
with open("prompt.txt","w") as f:
  f.write(prompt)
response=inference(prompt)
print(response)
with open("response.txt","w")as f:
  f.write(response)