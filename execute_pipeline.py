'''
This file tests the final pipeline on real openeleections questons. 
Choose between different test set sizes defined below AND whether you want to save outputs to a csv (versus just printing).
'''

from build_pipeline import execute_query
import pandas as pd

test_size = "custom"
save_to_csv = 0
questions = ["How many votes did Donald Trump get across all California counties in the 2020 US election for president?"]

##########################
### SELECTING TEST SET ###
##########################
test_query_lst = ''
if test_size == 'custom':
    test_query_lst = questions
elif test_size == "large":
    test_query_lst = ["How many votes did Donald Trump receive in Santa Clara county in each of the 2016 and 2020 presidential elections?",
                "In each county in the 2020 general election for President in Florida, how many votes did each candidate not belonging to the Democratic or Republican party receive?",
                "How many votes did Joe Biden receive in each of California, Florida, New York, and Texas in the 2020 general election for President?",
                "In which California counties did Ro Khana receive votes for U.S. House in each year?",
                "Which New York precincts voted for Republican candidates more than they voted for Democratic candidates in the 2020 general election?",
                "For each year in the Texas general election, what is the difference in the total number of votes given to the Democratic presidential candidate and the Republican presidential candidate?",
                "For each county in the 2020 Texas general election, what proportion of votes were early-voting compared to election-day?",
                "Which candidates received the most votes for Florida State Senate in each of 2018, 2020, and 2022?",
                "How many votes did Hillary Clinton receive in Shasta county in California in the 2016 presidential election?",
                "In each county in Texas in the 2018 election for Governor, how many votes did the Libertarian party candidate receive?",
                "For each year since 2012, how many votes did the Libertarian party receive in the presidential election in Santa Clara, California?",
                "Which precincts in California gave more votes to the Republican candidate than the Democratic candidate for U.S. Senate in 2012?",
                "How many votes did each Republican candidate for the U.S. House receive in New York in the 2020 general election?",
                "Which counties in Florida had the highest number of votes for the Green party candidate in the 2016 presidential election?",
                "How many votes did incumbent candidates receive in the Texas U.S. House elections in 2012?",
                "For each precinct in Los Angeles county in California, how many votes did each presidential candidate receive in the 2020 election?",
                "In each year, what is the total number of votes received by candidates from the Democratic party in New York's gubernatorial elections?",  # testing NER for gubernatorial->state governor
                "How many votes did each third-party candidates receive in the California U.S. House elections in 2018?",
                "Which counties in Texas had more votes for Democratic candidates than Republican candidates in the 2020 general election?",
                "What was the total number of votes for the 2016 presidential election in each county of New York?",
                "What was the total voter turnout for the 2016 presidential election in each county of New York?", # 'voter turnout'
                "Which counties in Texas had the largest reduction in the total number of votes for the Republican presidential candidate between 2012 and 2016 election?",
                "Which counties in Texas had the largest difference in the number of votes for Mitt Romney in 2012 and the nube rof votes for Donald Trump in 2016?", # same question as above
                "Which counties across California, Texas, and New York had the largest difference in the number of votes for Mitt Romney in 2012 and the nube rof votes for Donald Trump in 2016?",  # more states
                "For each New York county in the 2020 general elelction for Senate, what is the percentage of votes cast for a candidate from the Democratic party?",  # do math
                "Which California counties gave more votes for Libertarian candidates than Green party candidates in the 2016 presidential election?",
                "Which Texas counties cast more votes for Donald Trump than Hilary Clinton in the 2016 presidential election, but more votes for Joe Biden than Donald Trump in the 2020 presidential election?",
                "Which Florida candidates for U.S. House received votes in multiple years?",
                "For each Florida candidate for U.S. House that received votes in multiple years, how many votes did they receive in each year?",
                "For each precinct in the 2020 general election for U.S. Senate, what is the difference between the number of early votes and election-day votes"
                ]
elif test_size == "medium":
    test_query_lst = ["How many votes did Donald Trump receive in Santa Clara county in each of the 2016 and 2020 presidential elections?",
                "In each county in the 2020 general election for President in Florida, how many votes did each candidate not belonging to the Democratic or Republican party receive?",
                "How many votes did Joe Biden receive in each of California, Florida, New York, and Texas in the 2020 general election for President?",
                "In which California counties did Ro Khana receive votes for U.S. House in each year?",
                "Which New York precincts voted for Republican candidates more than they voted for Democratic candidates in the 2020 general election?",
                "For each year in the Texas general election, what is the difference in the total number of votes given to the Democratic presidential candidate and the Republican presidential candidate?",
                "In each year, what is the total number of votes received by candidates from the Democratic party in New York's gubernatorial elections?",  # testing NER for gubernatorial->state governor
                "How many votes did each third-party candidates receive in the California U.S. House elections in 2018?",
                "Which counties in Texas had more votes for Democratic candidates than Republican candidates in the 2020 general election?",
                "What was the total number of votes for the 2016 presidential election in each county of New York?",
                ]
else:
    test_query_lst = ["How many votes did Donald Trump receive in Santa Clara county in each of the 2016 and 2020 presidential elections?",
                "In each county in the 2020 general election for President in Florida, how many votes did each candidate not belonging to the Democratic or Republican party receive?",
                "How many votes did Joe Biden receive in each of California, Florida, New York, and Texas in the 2020 general election for President?",
                "In which California counties did Ro Khana receive votes for U.S. House in each year?",
                "Which New York precincts voted for Republican candidates more than they voted for Democratic candidates in the 2020 general election?",
                "For each year in the Texas general election, what is the difference in the total number of votes given to the Democratic presidential candidate and the Republican presidential candidate?"]


##########################################
### PRINTING RESULTS AND SAVING TO CSV ###
##########################################

results_list = []
for i in range(len(test_query_lst)):
    query = test_query_lst[i]
    print(f"Executing query {i+1}...")
    result = execute_query(query)

    # Printing results
    print(f"Question: {result['question']}")
    print(f"Generated lookup SUQL: {result['lookup_suql']}")
    print(f"Relevant tables retrieved: {result['table_names']}")
    print(f"Generated query SUQL: {result['query_suql']}")
    print(f"Output data: {result['output']}\n")
    print("=================\n")

    # Constructing CSV
    results_list.append({
        'question': result['question'],
        'lookup_suql': result['lookup_suql'],
        'table_names': result['table_names'],
        'query_suql': result['query_suql'],
        'output': result['output']
    })

if save_to_csv:
    df = pd.DataFrame(results_list)
    csv_filename = '/Users/sajidfarook/Desktop/SUQL_Research/test_pipeline_results.csv'
    df.to_csv(csv_filename, index=False)
    print(f"Results have been compiled into {csv_filename}")