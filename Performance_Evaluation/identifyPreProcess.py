import pandas as pd
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
# nltk.download('wordnet')
from scipy import stats

wnl = WordNetLemmatizer()

allNumeric_df = pd.read_csv('E:/Campus/FYP/NEW/DataSet/Full numerical/heart.csv',encoding='iso-8859-1')
numANDcat_df = pd.read_csv('E:/Campus/FYP/NEW/DataSet/Nu & Cat/zomato.csv',encoding = "iso-8859-1")

#Find multivaled attributs
pluralColumns = []
multValueColumns = []

def isplural(word):
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False #check it can be plural or not
    return plural

for nn in numANDcat_df.columns.values:
    plural = isplural(nn.lower())
    if(plural==True):
        pluralColumns.append(nn)

for pluralCol in pluralColumns:
    for val in numANDcat_df[pluralCol]:
        if(type(val)==str):
            if(val.count(',')>0):
                multValueColumns.append(pluralCol)
                break

#get colomn data type
for col in numANDcat_df.columns:
    if numANDcat_df[col].dtype == 'object':
        try:
            numANDcat_df[col] = pd.to_datetime(numANDcat_df[col])
        except ValueError:
            pass
colomnDataTypes = numANDcat_df.dtypes

#find duplicate rows
dup_temp = allNumeric_df.duplicated()
duplicate_row = []
for i,val in enumerate(dup_temp):
    if(val==True):
        duplicate_row.append(i)

#Find empty cells , colomn wise
empty_tp = np.where(pd.isnull(allNumeric_df))
empty=[]
for i in allNumeric_df.columns:
    empty.append([])
for i,val in enumerate(empty_tp[1]):
    empty[val].append(empty_tp[0][i])

#identify outliers(only apply numerical values)
z = np.abs(stats.zscore(allNumeric_df))
outliers_tp = np.where(z > 3)  #select outliers z is more than 3
outliers=[]
for i in allNumeric_df.columns:
    outliers.append([])
for i,val in enumerate(outliers_tp[1]):
    outliers[val].append(outliers_tp[0][i])

#Find corelated attribute
corr_matrix=allNumeric_df.corr().abs()  #Compute pairwise correlation of columns (pearson : standard correlation coefficient)
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool)) # Select upper triangle of correlation matrix
to_drop = [column for column in upper.columns if any(upper[column] > 0.95)] # Find index of feature columns with correlation greater than 0.95



