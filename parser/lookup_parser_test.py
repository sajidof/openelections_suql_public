from openai import OpenAI
from jinja2 import Environment, FileSystemLoader
from suql import suql_execute

# Testing with LLM-generated SUQL lookup

client = OpenAI()
jinja_environment = Environment(loader=FileSystemLoader('/Users/sajidfarook/Desktop/SUQL_Research/parser/'))
execute_lookup_llm_model_name = 'gpt-4-turbo'
generate_lookup_suql_model_name = 'gpt-4-turbo'

'''
Creates prompt
'''
def fill_template(template_file, prompt_parameter_values):
    template = jinja_environment.get_template(template_file)
    filled_prompt = template.render(**prompt_parameter_values)
    filled_prompt = "\n".join(
        [line.strip() for line in filled_prompt.split("\n")]
    )  # remove whitespace at the beginning and end of each line
    return filled_prompt

'''
Generates lookup SUQL
'''
def question_to_suql(user_query, prompt_file='lookup_table_prompt.prompt'):
    filled_prompt = fill_template(prompt_file, {"query": user_query})
    completion = client.chat.completions.create(
        model='gpt-4-turbo',
        messages=[
            {"role": "system", "content": filled_prompt},
        ],
        max_tokens=200,
        temperature=0.0
    )
    return completion.choices[0].message.content.strip()

'''
Executes generated lookup SUQL and returns output
'''
def execute_lookup_suql(user_query, database_name='openelections', table_w_ids={"lookup_table": "_id"}):
    generated_suql = question_to_suql(user_query)
    results, column_names, cache = suql_execute(generated_suql, table_w_ids, database_name, llm_model_name=execute_lookup_llm_model_name)
    return generated_suql, results

'''
Converts execute_lookup_suql output into list
'''
def clean_suql_output(output):
    result = []
    for tablename in output:
        result.append(tablename[0])
    return result

'''
Takes in natural language question and outputs the list of openelections tables that are relevant to that question.
'''
def question_to_tablenames(query):
    generated_suql, results = execute_lookup_suql(query)
    results = clean_suql_output(results)
    return results, generated_suql
        