import requests
import psycopg2
import toml

file = open("/home/tom/Documents/AIP/Bachelorarbeit/creds/psql.pass", "r")
passwd = file.read().strip()

config = toml.load('model_evaluation.toml')

con = psycopg2.connect( 
    dbname="model_evaluation", 
    user="local", 
    password=passwd, 
    host="141.33.165.24" 
)

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS model_evaluation (id SERIAL PRIMARY KEY, response VARCHAR, question VARCHAR, model VARCHAR, review INTEGER, class VARCHAR);")
con.commit()

for j in config['Models']['list']:
    for i in config['Questions']['list']:
        print(f'Model: {j} Question: {i[0]}')
        url = 'http://141.33.165.24:11434/api/generate'
        data = {
        "model": j,
        "stream" : False,
        "prompt": f"{i[0]}",
        "options": {
            "temperature": 0.3
        },
        }


        response = requests.post(url, json=data)

        print(response)

        cur.execute("INSERT INTO model_evaluation (response, question, model, review, class) VALUES (%s, %s, %s, NULL, %s)", (response.json()['response'], i[0], j, i[1]))
        con.commit()

con.close()
