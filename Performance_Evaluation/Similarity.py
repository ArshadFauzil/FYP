import spacy
import re
import pandas as pd
from spacy.lang.en.stop_words import STOP_WORDS
import pymongo
import difflib
from collections import Counter

# pd.set_option('display.max_columns', -1)
# pd.set_option('display.max_colwidth', -1)

r_match_element = []
sk_match_element = []
unique_parm_match_element = []
matched = []

#Spacy model load
# nlp = spacy.load('C:/Users/Dinusha/PycharmProjects/FYP/customModel')
nlp = spacy.load('en_vectors_web_lg')
# nlp = spacy.load('en_core_web_lg')
nlp_en = spacy.load('en')

#MongoDB Connection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["FYP"]
R_col = mydb["R_Param"]
SK_col = mydb["SK_Param"]
Parm_col = mydb["ML_Parameters"]
r_parm_df = pd.DataFrame(list(R_col.find()))
r_parm_df = r_parm_df.drop(['_id'], axis=1)
sk_parm_df = pd.DataFrame(list(SK_col.find()))
sk_parm_df = sk_parm_df.drop(['_id'], axis=1)
unique_parm_df = pd.DataFrame(list(Parm_col.find()))
unique_parm_df = pd.DataFrame({"Argument" : unique_parm_df['Parameters'][3], "Description" : unique_parm_df['Description'][3]})

#Select Match parmeters by argument name
for i, val1 in enumerate(r_parm_df['Argument']):
    for j, val2 in enumerate(sk_parm_df['Argument']):
        if(val1.lower()==val2.lower()):
            r_match_element.append(i)
            sk_match_element.append(j)
            # print(val1)
            for k,val3 in enumerate(unique_parm_df['Argument']):
                if (val1.lower() == val3.lower()):
                    unique_parm_match_element.append(k)

#Create dataframe for perfecly match parameters
perfcMatch_R_df = r_parm_df.loc[r_match_element]
perfcMatch_R_df = perfcMatch_R_df.reset_index(drop=True)
perfcMatch_SK_df = sk_parm_df.loc[sk_match_element]
perfcMatch_SK_df = perfcMatch_SK_df.reset_index(drop=True)

#Remove match parameters from comparision
r_parm_df = r_parm_df.drop(r_match_element)
r_parm_df = r_parm_df.reset_index(drop=True)
sk_parm_df = sk_parm_df.drop(sk_match_element)
sk_parm_df = sk_parm_df.reset_index(drop=True)
unique_parm_df = unique_parm_df.drop(unique_parm_match_element)
unique_parm_df = unique_parm_df.reset_index(drop=True)


#Find smallest tupled dataframe
parm_df1=''
parm_df2=''
if(len(sk_parm_df)<=len(r_parm_df)):
    parm_df1 = sk_parm_df
    parm_df2 = r_parm_df
    perfcMatch_df = pd.DataFrame({"Argument_1" : perfcMatch_SK_df['Argument'], "Description_1" : perfcMatch_SK_df['Description'], "Default_value_1" : perfcMatch_SK_df['Default_value'], "Argument_2" : perfcMatch_R_df['Argument'], "Description_2" : perfcMatch_R_df['Description'], "Default_value_2" : perfcMatch_R_df['Default_value']})
else:
    parm_df1 = r_parm_df
    parm_df2 = sk_parm_df
    perfcMatch_df = pd.DataFrame({"Argument_1" : perfcMatch_R_df['Argument'], "Description_1" : perfcMatch_R_df['Description'], "Default_value_1" : perfcMatch_R_df['Default_value'], "Argument_2" : perfcMatch_SK_df['Argument'], "Description_2" : perfcMatch_SK_df['Description'], "Default_value_2" : perfcMatch_SK_df['Default_value']})

perfcMatch_df["score_desc"] = 'NaN'
perfcMatch_df["total_score"] = 'NaN'


#Sequence matiching
def similar(a,b):
    seq = difflib.SequenceMatcher(None, a, b)
    d = seq.ratio()
    return d

#Remove punctuvation and lemmertize
def PAL(string):
    x = re.sub("[^A-Za-z0-9\s]+", " ", string)
    doc_lemmertized = ' '.join([str(t.lemma_) for t in nlp(x)])
    doc_lemmertized = doc_lemmertized.replace('-PRON-', '').replace(' ','')
    doc_lemmertized = doc_lemmertized.lower()
    return nlp(doc_lemmertized)

#Remove unwanted words
def RUW(string):
    x = re.sub("[^A-Za-z0-9\s]+", " ",string)
    y = re.sub("[ ]{2,}"," ",x)
    # print(y)
    doc_lemmertized = ' '.join([str(t.lemma_) for t in nlp(y)])
    doc_lemmertized = doc_lemmertized.replace('-PRON-','')
    # print(doc_lemmertized)
    sentence = nlp_en(doc_lemmertized)
    doc_not_stopword = (' '.join([str(t) for t in sentence if not t.is_stop]))
    doc_not_stopword = doc_not_stopword.lower()
    # print(doc_not_stopword)
    doc_POS_Tagged = nlp(' '.join([str(t) for t in nlp_en(doc_not_stopword) if t.pos_ in ['NOUN', 'PROPN', 'VERB']]))
    # print(doc_POS_Tagged)
    return doc_POS_Tagged

def match():
    #Get similarity by differnt scores
    for i, val1 in enumerate(parm_df1['Description']):
        total_score_max = 0.0
        score_arg_max = 0.0
        score_desc_max= 0.0
        similar_arg_no = -2
        for j, val2 in enumerate(parm_df2['Description']):
            # score_arg = 0.0
            score_arg = similar(str(PAL(parm_df1['Argument'][i])),str(PAL(parm_df2['Argument'][j])))
            score_desc = RUW(val1).similarity(RUW(val2))
            # score_val = 0.0
            if(parm_df1['Default_value'][i]!=None and parm_df2['Default_value'][j]!=None):
                score_val = PAL(parm_df1['Default_value'][i]).similarity(PAL(parm_df2['Default_value'][j]))
            # print(score_val)
            total_score = score_desc + score_arg
            if(score_desc_max<score_desc):
                score_desc_max = score_desc
            if(total_score_max<total_score):
                total_score_max = total_score
                similar_arg_no = j
            # print(str(parm_df1['Argument'][i])+' '+str(score_desc)+' '+str(score_arg)+' '+str(parm_df2['Argument'][j])+' '+str(total_score))
        if(score_desc_max>=0.75):
            # print(str(parm_df1['Argument'][i])+' '+str(total_score_max)+' '+str(parm_df2['Argument'][similar_arg_no]))
            matched.append([parm_df1['Argument'][i],parm_df1['Description'][i],parm_df1['Default_value'][i],parm_df2['Argument'][similar_arg_no],parm_df2['Description'][similar_arg_no],parm_df2['Default_value'][similar_arg_no],score_desc_max,total_score_max])

    matched_df = pd.DataFrame(matched,columns=['Argument_1','Description_1','Default_value_1','Argument_2','Description_2','Default_value_2','score_desc','total_score'])
    c = Counter(matched_df['Argument_2'])

    #Remove duplicate matche by higher total score
    for val in set(matched_df['Argument_2']):
        if c[val] > 1:
            select = matched_df.loc[matched_df['Argument_2'] == val]
            max = select['total_score'].idxmax()
            select = select.drop(max)
            matched_df = matched_df.drop(select.index.values)

    #Select perfectMatch and Match arguments
    allMatch_df = pd.concat([perfcMatch_df,matched_df])
    allMatch_df = allMatch_df.reset_index(drop=True)

    #Select not matched arguments
    notMatchTemp_df1 = parm_df1.copy()
    notMatchTemp_df2 = parm_df2.copy()
    for val in allMatch_df['Argument_1']:
        indexNames = notMatchTemp_df1[notMatchTemp_df1['Argument'] == val].index
        notMatchTemp_df1.drop(indexNames, inplace=True)
    for val in allMatch_df['Argument_2']:
        indexNames = notMatchTemp_df2[notMatchTemp_df2['Argument'] == val].index
        notMatchTemp_df2.drop(indexNames, inplace=True)

    notMatch_df1 = pd.DataFrame({"Argument_1" : notMatchTemp_df1['Argument'], "Description_1" : notMatchTemp_df1['Description'], "Default_value_1" : notMatchTemp_df1['Default_value']})
    notMatch_df1 = notMatch_df1.reset_index(drop=True)
    notMatch_df2 = pd.DataFrame({"Argument_2" : notMatchTemp_df2['Argument'], "Description_2" : notMatchTemp_df2['Description'], "Default_value_2" : notMatchTemp_df2['Default_value']})
    notMatch_df2 = notMatch_df2.reset_index(drop=True)
    notMatch_df = pd.concat([notMatch_df1,notMatch_df2], axis=1)
    notMatch_df["score_desc"] = 'NaN'
    notMatch_df["total_score"] = 'NaN'

    #Final Result
    result = pd.concat([allMatch_df,notMatch_df])
    result = result.reset_index(drop=True)

    return result

# print(match())

# for i , val1 in enumerate(unique_parm_df['Description']):
#     max = 0.0
#     similar_arg_no = -2
#     for j , val2 in enumerate(matched):
#         score1 = RUW(val1).similarity(RUW(val2[3]))
#         score2 = similar(str(PAL(unique_parm_df['Argument'][i])), str(PAL(matched[j][2])))
#         total_score = score1 + score2
#         if (max < total_score):
#             max = total_score
#             similar_arg_no = j
#     print(str(matched[similar_arg_no][4])+' '+str(max)+' '+str(matched[similar_arg_no][2])) #need to edit

# for val in r_parm_df['Default_value']:
#     print(val)