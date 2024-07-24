import csv
import pandas as pd
from parser.lookup_parser_test import question_to_tablenames, fill_template
from openai import OpenAI
from jinja2 import Environment, FileSystemLoader
from suql import suql_execute
from suql.prompt_continuation import llm_generate

prompt_file = 'query_parse_noans.prompt'
client = OpenAI()
jinja_environment = Environment(loader=FileSystemLoader('/Users/sajidfarook/Desktop/SUQL_Research/parser/'))

'''
Takes a single table name and returns a table sigature that can be in putted as a prompt to generate the final SUQL query.
'''
# Functions to construct the table signatures to input to the prompt
def get_signature(tablename, csv_path='/Users/sajidfarook/Desktop/SUQL_Research/lookup_table.csv'):
    signature = ''
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['csv_filename_noext'] == tablename:
                signature = row['col_name_type_tup']  # Convert string representation of tuple to actual tuple
                break

    #print(f"Signature for this table {tablename} is {signature}")
    return signature

'''
Takes list of relevant table names and concatenates their signatures that can be in putted as a prompt to generate the final SUQL query.
'''
def tablenames_to_signatures(table_names):
    name_signature_lst = []
    for table_name in table_names:
        curr_signature = get_signature(table_name)
        table_name = "\"" + table_name + "\""
        name_signature_lst.append(table_name + ": " + curr_signature)
    result = "\n".join(name_signature_lst)
    #print(f"For the tables {table_names}, returned all the signatures which are: \n {result}")
    return result

'''
Takes a natural language question and a list of tablenames and generates SUQL.
'''
def question_to_suql(user_query, table_names, prompt_file=prompt_file):
    prompt_param_dict = {
        "num_tables":len(table_names),
        "user_query":user_query,
        "table_signatures":tablenames_to_signatures(table_names)
    }
    filled_prompt = fill_template(prompt_file, prompt_param_dict)
    #print("The filled prompt being given to the LLM is ", filled_prompt)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": filled_prompt},
        ],
        max_tokens=200,
        temperature=0.0
    )
    response = completion.choices[0].message.content.strip()
    #print("The LLM response generating the query SUQL is: ", response)
    return response
    
'''
Final endpoint - takes in natural language question, gets relevant tablenames, generates SUQL, and executes it against each of those tables. Outputs results.

Note: table_w_ids is wrong, change this later
'''
def execute_query(user_query, database_name='openelections', table_w_ids={"lookup_table": "_id"}):
    #print("The question: ", user_query)
    outputs = []
    tablenames, lookup_suql = question_to_tablenames(user_query)
    #print(f"For the generated lookup SUQL {lookup_suql}, we retrieved the tablenames {tablenames}")
    if len(tablenames)==0:
        print(f"The lookup SUQL failed to retrieve any tables to execute your query on. The lookup SUQL was: {lookup_suql}). The question was: {user_query}")

    query_suql = question_to_suql(user_query, tablenames)
   # print("Final query SUQL is :", query_suql)

    suql_lst = query_suql.split('<NEXTQUERY>')
    for suql in suql_lst:
        #print("the suql thats about to be executed:", suql)
        result, column_names, cache = suql_execute(suql, table_w_ids, database_name)
        #print(f"Executing the query SUQL {suql} returned the results {result}")

        #print("results of suql executions", result)
        outputs.append((result, column_names))

    
    result = {
        "question":user_query,
        "lookup_suql":lookup_suql,
        "table_names":tablenames,
        "query_suql":suql_lst,
        "output":outputs,

    }
    return result