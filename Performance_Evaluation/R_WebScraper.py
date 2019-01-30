import bs4
import requests
import lxml
import pandas as pd
import regex
import pymongo

#Varible and arrays
argument_array = []
argument_desc_array = []
arg_name = []
default_value = []
values_in_brackets = []
arg_and_def_values = []

#get gata from web
res = requests.get('https://www.rdocumentation.org/packages/e1071/versions/1.7-0/topics/svm')
soup = bs4.BeautifulSoup(res.text, 'lxml')
argument = soup.find(class_='topic--arguments')
default_parm = soup.find('pre').text.replace('\n',' ').replace('#','\n').replace('\xa0', ' ').replace('\t', '')

#Extract arguments
argument_array.append(argument.dt.text)
for arg in argument.dt.find_next_siblings('dt'):
    argument_array.append(arg.text)

#Extract argument description
argument_desc_array.append(argument.dd.text.replace('\n',' ').replace('\t', ''))
for arg_desc in argument.dd.find_next_siblings('dd'):
    argument_desc_array.append(arg_desc.text.replace('\n',' ').replace('\t', ''))

#regex
outer_bracket_content_regex = "\(([^()]|(?R))*\)"
comma_out_bracket_regex = ",\s*(?![^()]*\))"
before_equal_regex = "^[^=]*"
after_equal_regex = "(?<=\=).*"

matches_outer_bracket = regex.finditer(outer_bracket_content_regex, default_parm, regex.MULTILINE)

#Get text at outer brackets
for match in matches_outer_bracket:
        values_in_brackets.append(match.group())

#Separate argument by commas which not in inner brackets
for val in values_in_brackets:
    val = val[1:]
    val = val[:-1]
    for val1 in regex.split(comma_out_bracket_regex,val):
        arg_and_def_values.append(val1)

#Extract argument before appers in '='
for match in arg_and_def_values:
    if (match.count('=') > 0):
        if(regex.search(before_equal_regex, match) != None):
            select = regex.search(before_equal_regex, match).group()
            arg_name.append(select)

#Extract default_value after appers in '='
for match in arg_and_def_values:
    if(regex.search(after_equal_regex, match) != None):
        select = regex.search(after_equal_regex, match).group()
        default_value.append(select)

#Clean unwanted characters from argument names
for i, val in enumerate(arg_name):
    arg_name[i] = arg_name[i].replace(' ','').replace('\t', '')

default_value_temp = [None] * len(argument_array)

#Fill Default value to an array
for i, val in enumerate(argument_array):
    for j, arg in enumerate(arg_name):
        if(arg==val):
            default_value_temp[i] = default_value[j]

#save data
df = pd.DataFrame({"Argument" : argument_array, "Description" : argument_desc_array, "Default_value" : default_value_temp})
df.to_csv("R_output.csv", index=False, encoding="utf-8")

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["FYP"]
mycol = mydb["R_Param"]
mycol.remove({})
mycol.insert_many(df.to_dict('records'))