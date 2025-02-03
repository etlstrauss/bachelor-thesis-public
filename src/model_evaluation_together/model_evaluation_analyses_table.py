import toml
import psycopg2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# load configurations
config = toml.load('model_evaluation.toml')
file = open("/home/tom/Documents/AIP/Bachelorarbeit/creds/psql.pass", "r")
passwd = file.read().strip()
file.close()

# Connect to the database
con = psycopg2.connect( 
    dbname="model_evaluation",
    user="local", 
    password=passwd, 
    host="141.33.165.24" 
)
cur = con.cursor()


# get the number of evaluations for each class
review_list = []
for i in range(0,3):
    cur.execute(f"SELECT COUNT(*) FROM model_evaluation WHERE review={i} AND model!='opencoder:8b-instruct-fp16';")
    review_list.append(cur.fetchone()[0])
    if(review_list[i] == 0):
        review_list[i] = 0.1
labels = ['bad', 'average', 'great']

review_list2 = []
for i in range(0,3):
    cur.execute(f"SELECT COUNT(*) FROM model_evaluation_rag WHERE review={i};")
    review_list2.append(cur.fetchone()[0])
labels = ['bad', 'average', 'great']

# rounding
review_list = np.round(review_list).astype(int)
review_list2 = np.round(review_list2).astype(int)

overall_list = np.vstack((review_list, review_list2))
# lists to df
df = pd.DataFrame(overall_list, columns=labels, index=["Without RAG", "With RAG"])

# generate and save as .tex
code = df.to_latex(index=True, escape=True, column_format="|c|c|c|c|", caption=r"Model evaluation overall")

file = open("model_evaluation_analyses_table.tex", "w")
file.write(code)
file.close()

cur.close()