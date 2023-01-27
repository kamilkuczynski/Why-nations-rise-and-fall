import pandas as pd

df0 = pd.read_csv('gdp_per_capita_0.csv')
#df0['Country'] = df0['Country'].apply(lambda x: ' '.join(x.split()))
df1 = pd.read_csv('gdp_per_capita_1.csv')
df2 = pd.read_csv('gdp_per_capita_2.csv')
df3 = pd.read_csv('gdp_per_capita_3.csv')
df4 = pd.read_csv('gdp_per_capita_4.csv')

#removing column "country" from all csv files with exception of the first
df1 = df1.drop(columns=['Country'])
df2 = df2.drop(columns=['Country'])
df3 = df3.drop(columns=['Country'])
df4 = df4.drop(columns=['Country'])

#why it wasn't working?
# df_list = [df.drop(columns=['Country']) for df in [df0, df1, df2, df3, df4]]

#merging tables
merged_df = pd.concat([df0, df1, df2, df3, df4], axis=1)
#print(merged_df.head(10))


#removing first colmn named "unnamed" added by function concat
merged_df.drop(columns = ['Unnamed: 0'], inplace = True)
print(merged_df.head(10))


#saving tables to one table
merged_df.to_csv('merged_beautiful_gdp_per_capita.csv', index=True)
