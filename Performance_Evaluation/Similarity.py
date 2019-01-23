import spacy
import re
import pandas as pd
from spacy.lang.en.stop_words import STOP_WORDS
import pymongo
import difflib

r_match_element = []
sk_match_element = []
unique_parm_match_element = []
matched = []

#Spacy model load
nlp = spacy.load('en_core_web_lg')
nlp_en = spacy.load('en')

#MongoDB Connection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["FYP"]
R_col = mydb["R_Param"]
SK_col = mydb["SK_Param"]
Parm_col = mydb["ML_Parameters"]
r_parm_df = pd.DataFrame(list(R_col.find()))
sk_parm_df = pd.DataFrame(list(SK_col.find()))
unique_parm_df = pd.DataFrame(list(Parm_col.find()))
unique_parm_df = pd.DataFrame({"Argument" : unique_parm_df['Parameters'][3], "Description" : unique_parm_df['Description'][3]})

#Select Match parmeters by argument name
for i, val1 in enumerate(r_parm_df['Argument']):
    for j, val2 in enumerate(sk_parm_df['Argument']):
        if(val1.lower()==val2.lower()):
            r_match_element.append(i)
            sk_match_element.append(j)
            print(val1)
            for k,val3 in enumerate(unique_parm_df['Argument']):
                if (val1.lower() == val3.lower()):
                    unique_parm_match_element.append(k)

#Remove match parameters from comparision
r_parm_df = r_parm_df.drop(r_match_element)
r_parm_df = r_parm_df.reset_index(drop=True)
sk_parm_df = sk_parm_df.drop(sk_match_element)
sk_parm_df = sk_parm_df.reset_index(drop=True)
unique_parm_df = unique_parm_df.drop(unique_parm_match_element)
unique_parm_df = unique_parm_df.reset_index(drop=True)

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
    doc_POS_Tagged = nlp(' '.join([str(t) for t in nlp(doc_not_stopword) if t.pos_ in ['NOUN', 'PROPN', 'VERB']]))
    return doc_POS_Tagged

parm_df1 = r_parm_df
parm_df2 = sk_parm_df
if(len(sk_parm_df)<=len(r_parm_df)):
    parm_df1 = sk_parm_df
    parm_df2 = r_parm_df

#Get similarity by differnt scores
for i, val1 in enumerate(parm_df1['Description']):
    max = 0.0
    similar_arg_no = -2
    for j, val2 in enumerate(parm_df2['Description']):
        score1 = RUW(val1).similarity(RUW(val2))
        score2 = similar(str(PAL(parm_df1['Argument'][i])),str(PAL(parm_df2['Argument'][j])))
        # score2 = 0.0
        total_score = score1 + score2
        if(max<total_score):
            max = total_score
            similar_arg_no = j
        # print(str(parm1['Argument'][i])+' '+str(score1)+' '+str(score2)+' '+str(parm2['Argument'][j]))
    print(str(parm_df1['Argument'][i])+' '+str(max)+' '+str(parm_df2['Argument'][similar_arg_no]))
    matched.append([i,similar_arg_no,parm_df2['Argument'][similar_arg_no],parm_df2['Description'][similar_arg_no],parm_df1['Argument'][i]])

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

