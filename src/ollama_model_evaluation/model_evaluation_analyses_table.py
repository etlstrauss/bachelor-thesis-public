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

end_list = []
# get the number of evaluations for each class
for model in config['Models']['list']:
    review_list = []
    for i in range(0,3):
        cur.execute(f"SELECT COUNT(*) FROM model_evaluation WHERE review={i} AND model='{model}';")
        review_list.append(cur.fetchone()[0])
    end_list.append(review_list)
labels = ['bad', 'average', 'great']

review_list = np.round(review_list).astype(int)


df = pd.DataFrame(end_list, columns=labels, index=config['Models']['list'])

code = df.to_latex(index=True, escape=True, column_format="|l|c|c|c|", caption=r"Model evaluation by model without RAG")

file = open("model_evaluation_analyses_table.tex", "w")
file.write(code)
file.close()


overall_list = []

labels_list = ['bad', 'average', 'great']
classes = ['general', 'programming', 'programming-rag']

df_end = pd.DataFrame()
# run sql quries to create lists for the bar chart (bad/average/great per model)
for j in range(0, 3):
        review_list = []
        for model in config['Models']['list']:
                tmp_list = []
                for i in range(0,3):
                    cur.execute(f"SELECT COUNT(*) FROM model_evaluation WHERE model='{model}' AND review={i} AND class='{classes[j]}';")
                    eval = cur.fetchone()[0]
                    tmp_list.append(eval)
                review_list.append(tmp_list)
        df = pd.DataFrame(review_list, columns=labels_list, index=config['Models']['list'])
        df_end = pd.concat([df_end, df])
print(df_end)

code = df_end.to_latex(index=True, escape=True, column_format="|c|c|c|c|", caption=r"Model evaluation without RAG")

#file = open("model_evaluation_analyses_table_detailed.tex", "w")
#file.write(code)
#file.close()

cur.close()