import pandas as pd
import psycopg2
import toml

file = open("/home/tom/Documents/AIP/Bachelorarbeit/creds/psql.pass", "r")
passwd = file.read().strip()

data = [['id' , 'question', 'review']]


con = psycopg2.connect( 
    dbname="model_evaluation", 
    user="local", 
    password=passwd, 
    host="141.33.165.24" 
)

cur = con.cursor()
cur.execute("SELECT COUNT(*) FROM model_evaluation_workflow;")

for i in range(0, cur.fetchone()[0]):
    cur.execute("SELECT id, question, review FROM model_evaluation_workflow WHERE id=%s;", (i+1,))
    current = cur.fetchone()
    datatmp = [current[0], current[1], current[2]]
    data.append(datatmp)

df = pd.DataFrame(data[1:], columns=data[0])

toml_data = toml.load("model_evaluation.toml")['Questions']['list']

toml_data = [item[0] for item in toml_data]

order_map = {question: i for i, question in enumerate(toml_data, start=1)}
df['question'] = df['question'].map(order_map)

code = df.to_latex(index=False, escape=True, longtable=True, column_format="|c|c|c|", caption=r"Workflow evaluation table ")

file = open("model_evaluation_table_workflow_latex.tex", "w")
file.write(code)
file.close()


