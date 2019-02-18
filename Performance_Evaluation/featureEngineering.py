import pandas as pd
import numpy as np
import re
from sklearn import preprocessing
from sklearn.preprocessing import Imputer
import nltk
from nltk.stem import WordNetLemmatizer
# nltk.download('wordnet')
from scipy import stats

wnl = WordNetLemmatizer()

allNumeric_df = pd.read_csv('E:/Campus/FYP/NEW/DataSet/Full numerical/heart.csv',encoding='iso-8859-1')
numANDcat_df = pd.read_csv('E:/Campus/FYP/NEW/DataSet/Nu & Cat/googleplaystore.csv',encoding = "iso-8859-1")

#Find multivaled attributs
pluralColumns = []
multValueColumns = []

def isplural(word):
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False #check it can be plural or not
    return plural

def binarizing(df,col_name,separator):
    dummies = df[col_name].str.lower()
    dummies = pd.DataFrame({col_name:dummies.values})
    dummies = dummies[col_name].str.replace(' ', '')
    dummies = pd.DataFrame({col_name:dummies.values})
    dummies = dummies[col_name].str.get_dummies(sep=separator)
    dummies = dummies.groupby(dummies.columns, axis=1).sum()
    df = df.drop([col_name], axis=1)
    buinarized_df = pd.concat([df, dummies], axis=1, join_axes=[df.index])
    # buinarized_df.to_csv("dummy.csv", index=False, encoding="iso-8859-1" )
    return buinarized_df

def numerization(col):
    strElementCount = 0
    strElement = []
    for i,val in enumerate(numANDcat_df[col]):
        try:
            float(val)
        except:
            strElementCount = strElementCount + 1
            strElement.append(i)
    persentage = (strElementCount/numANDcat_df[col].count())*100
    if persentage<5:
        for no in strElement:
            numANDcat_df.at[no, col] = re.sub('[^0-9.]+','',numANDcat_df[col][no])
        numANDcat_df[col] = pd.to_numeric(numANDcat_df[col])

def removePlusOfNumber(col):
    plusCount = 0
    for val in numANDcat_df[col]:
        try:
            if re.search('(?<=\d)\+',val):
                plusCount = plusCount + 1
        except:
            pass
    persentage = (plusCount/numANDcat_df[col].count())*100
    if persentage>95:
        for i,val in enumerate(numANDcat_df[col]):
            numANDcat_df.at[i, col] = re.sub('((?<=\d)\+)|(,)|(\D)','',numANDcat_df[col][i])
        try:
            numANDcat_df[col] = pd.to_numeric(numANDcat_df[col])
        except:
            print('can not removePlusOfNumber')

def lebleEncorder(column):
    le = preprocessing.LabelEncoder()
    le.fit(numANDcat_df[column].astype(str))
    numANDcat_df[column] = le.transform(numANDcat_df[column].astype(str))

for nn in numANDcat_df.columns.values:
    plural = isplural(nn.lower())
    if(plural==True):
        pluralColumns.append(nn)

separator = None
for pluralCol in pluralColumns:
    for val in numANDcat_df[pluralCol]:
        if(type(val)==str):
            if(val.count(';')>0):
                multValueColumns.append(pluralCol)
                separator = ","
                break
            if (val.count(',') > 0):
                multValueColumns.append(pluralCol)
                separator = ";"
                break

# for mul_col in multValueColumns:
#     numANDcat_df = binarizing(numANDcat_df,mul_col,separator)
#
# numANDcat_df.to_csv("dummy.csv", index=False, encoding="iso-8859-1" )

#get colomn data type
for col in numANDcat_df.columns:
    if numANDcat_df[col].dtype == 'object':
        try:
            numANDcat_df[col] = pd.to_datetime(numANDcat_df[col])
        except ValueError:
            pass

#numarize data set
for col in numANDcat_df.columns:
    numerization(col)

#plus remove
for col in numANDcat_df.columns:
    removePlusOfNumber(col)

colomnDataTypes = numANDcat_df.dtypes

# print(numANDcat_df.columns[0])


#use label encoder
for col,type in enumerate(colomnDataTypes):
    if (type == object):
        lebleEncorder(numANDcat_df.columns[col])



#find duplicate rows
dup_temp = numANDcat_df.duplicated()
duplicate_row = []
for i,val in enumerate(dup_temp):
    if(val==True):
        duplicate_row.append(i)

numANDcat_df = numANDcat_df.drop(duplicate_row)
numANDcat_df = numANDcat_df.reset_index(drop=True)



#Find empty cells , colomn wise
# empty_tp = np.where(pd.isnull(numANDcat_df))
# empty=[]
# for i in numANDcat_df.columns:
#     empty.append([])
# for i,val in enumerate(empty_tp[1]):
#     empty[val].append(empty_tp[0][i])

#fix empty cell
catCol = []
for col,type in enumerate(colomnDataTypes):
    if (type == object):
        catCol.append(numANDcat_df.columns[col])

numANDcat_df = numANDcat_df.dropna(subset=catCol)
numANDcat_df = numANDcat_df.reset_index(drop=True)

temporal = False

for type in colomnDataTypes:
    if re.search('datetime',str(type)):
        temporal = True
        break

if (temporal):
    numANDcat_df = numANDcat_df.fillna(method='ffill')
else:
    fill_NaN = Imputer(missing_values=np.nan, strategy='mean', axis=1)
    imputed_DF = pd.DataFrame(fill_NaN.fit_transform(numANDcat_df))
    imputed_DF.columns = numANDcat_df.columns
    imputed_DF.index = numANDcat_df.index
    numANDcat_df = imputed_DF



#identify outliers(only apply numerical values)
z = np.abs(stats.zscore(numANDcat_df))
# outliers_tp = np.where(z >= 3)
numANDcat_df = numANDcat_df[(z < 5).all(axis=1)]  #delete outliers

# outliers=[]
# for i in allNumeric_df.columns:
#     outliers.append([])
# for i,val in enumerate(outliers_tp[1]):
#     outliers[val].append(outliers_tp[0][i])


#Find corelated attribute
corr_matrix=numANDcat_df.corr().abs()  #Compute pairwise correlation of columns (pearson : standard correlation coefficient)
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool)) # Select upper triangle of correlation matrix
to_drop = [column for column in upper.columns if any(upper[column] > 0.95)] # Find index of feature columns with correlation greater than 0.95

numANDcat_df.drop(to_drop, axis=1)

# #Normalize data set
x = numANDcat_df.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
numANDcat_df = pd.DataFrame(x_scaled, columns=numANDcat_df.columns)
numANDcat_df = numANDcat_df.round(3)

numANDcat_df.to_csv("processed.csv", index=False, encoding="utf-8")