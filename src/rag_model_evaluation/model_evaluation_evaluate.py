import psycopg2
from rich.console import Console
from rich.markdown import Markdown

file = open("/home/tom/Documents/AIP/Bachelorarbeit/creds/psql.pass", "r")
passwd = file.read().strip()

console = Console()

con = psycopg2.connect( 
    dbname="model_evaluation", 
    user="local", 
    password=passwd, 
    host="141.33.165.24" 
)

cur = con.cursor()
cur.execute("SELECT COUNT(*) FROM model_evaluation_rag;")
number_of_records = cur.fetchone()[0]

is_true = True
console.clear()
while is_true:
    console.clear()
    console.print("""
                  This is a small command line tool to review the generated responses. Please answer the following questions with y or n. y for true and n for false. Did you understand?
                  In the following you will see a question and a the response.
                  """)
    user_input = input(":")
    if user_input in ["true", "1", "yes", "y", "t"]:
            is_true = False
    elif user_input in ["false", "0", "no", "n", "f"]:
            is_true = True

for i in range(number_of_records):
    console.clear()
    console.print(Markdown(f"### Question:\n"))
    cur.execute(f"SELECT question FROM model_evaluation_rag WHERE id={i+1};")
    console.print(Markdown(cur.fetchone()[0])) 
    
    console.print("\n" * 4)

    console.print(Markdown(f"### Response: \n"))
    cur.execute(f"SELECT response FROM model_evaluation_rag WHERE id={i+1};")
    console.print(Markdown(cur.fetchone()[0])) 

    user_input = int(input(":").strip().lower())

    cur.execute(f"UPDATE model_evaluation_rag SET review={user_input} WHERE id={i+1};")
    con.commit()
    console.clear()

con.close()