import pandas as pd
import numpy as np

allNumeric_df = pd.read_csv('E:/Campus/FYP/NEW/DataSet/Full numerical/ottawa_bike_counters.csv')
numANDcat_df = pd.read_csv('E:/Campus/FYP/NEW/DataSet/Nu & Cat/fifa19.csv')

colomnDataTypes = allNumeric_df.dtypes
empty = np.where(pd.isnull(allNumeric_df))
allNumeric_df.columns = allNumeric_df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

# print(allNumeric_df)
# print(allNumeric_df[allNumeric_df['date'] == 'NaN'].index)
print(colomnDataTypes[-1])