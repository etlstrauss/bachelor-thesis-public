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


API_URL = "http://141.33.165.24:8000/api/v1/prediction/6b74c5bd-bcf9-4a29-824f-06d0028cce74"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS model_evaluation_rag (id SERIAL PRIMARY KEY, response VARCHAR, question VARCHAR, model VARCHAR, review INTEGER, class VARCHAR);")
con.commit()

for j in config['Models']['list']:
    for i in config['Questions']['list']:
        print(f'Model: {j} Question: {i[0]}')
        output = query({
            "question": i[0],
            "overrideConfig": {
                "modelName": j,
            }
        })

        response = query(output).get('text')
        print(response)
        print("Starting upload to db")
        cur.execute("INSERT INTO model_evaluation_rag (response, question, model, review, class) VALUES (%s, %s, %s, NULL, %s)", (response, i[0], j, i[1]))
        con.commit()

con.close()
