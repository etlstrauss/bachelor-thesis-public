import pandas as pd
import psycopg2

file = open("/home/tom/Documents/AIP/Bachelorarbeit/creds/psql.pass", "r")
passwd = file.read().strip()

data = [['id', 'question', 'model', 'review']]


con = psycopg2.connect( 
    dbname="model_evaluation", 
    user="local", 
    password=passwd, 
    host="141.33.165.24" 
)

cur = con.cursor()
cur.execute("SELECT COUNT(*) FROM model_evaluation_rag;")

for i in range(0, cur.fetchone()[0]):
    cur.execute("SELECT * FROM model_evaluation_rag WHERE id=%s;", (i+1,))
    current = cur.fetchone()
    datatmp = [current[0], current[2], current[3], current[4]]
    data.append(datatmp)

df = pd.DataFrame(data[1:], columns=data[0])

file = open("model_evaluation_table_rag.md", "w")
file.write(df.to_markdown(index=False))
file.close()

