import requests
import time
import pandas as pd

question = "Please create an hello world REANA workflow."
times = []
answers = []

# ollama call
url = 'http://141.33.165.24:11434/api/generate'
payload = {
"model": 'qwen2.5:32b-instruct-q8_0',
"stream" : False,
"prompt": question,
"options": {
    "temperature": 0.3
},
}

start = time.time()
response = requests.post(url, json=payload).json()
end = time.time()
times.append(end - start)
answers.append([response.get("response")])

#rag call
API_URL = "http://141.33.165.24:8000/api/v1/prediction/6b74c5bd-bcf9-4a29-824f-06d0028cce74"

payload = ({
    "question": question,
    "overrideConfig": {
        "modelName": "qwen2.5:32b-instruct-q8_0",
    }
})

start = time.time()
response = requests.post(API_URL, json=payload).json()
end = time.time()
times.append(end - start)
answers.append([response.get("text")])


# flowise call
API_URL = "http://141.33.165.24:8000/api/v1/prediction/bddddad9-3b09-44f1-af80-e6788a58d906"

payload = {
    "question": question
}


start = time.time()
response = requests.post(API_URL, json=payload).json()
end = time.time()
times.append(end - start)
answers.append([response.get("text")])

# round and format values
times = [round(time, 2) for time in times]
times = [f"{time:.2f}" for time in times]

# lists to df
df = pd.DataFrame(times, columns=["Time(in s)"], index=["Direct Ollama call", "Simple RAG call", "FlowiseAI call"])

df2 = pd.DataFrame(answers, columns=["Answer"], index=["Direct Ollama call", "Simple RAG call", "FlowiseAI call"])

# generate latex tables and save
table = df.to_latex(index=True, escape=True, column_format="|l|r|", caption=r"Time consumption table")
table2 = df2.to_latex(index=True, escape=True, column_format="|l|r|", caption=r"Time consumption table - answers")

file = open("time_evalution.table.tex", "w")
file.write(table)
file.close()

file = open("time_evalution.answers.tex", "w")
file.write(table2)
file.close()

