import pandas as pd

file_name = "C:/Users/kuczy/Documents/GitHub/Why-nations-rise-and-fall/gdp_per_capita_ppp_constant_2017.csv"

df = pd.read_csv(file_name)

df.rename(columns={df.columns[0]: "Country"}, inplace= True)

duplicate_rows = df.duplicated()
print(f"This data contains {duplicate_rows.sum()} duplicated rows.\n")

print("Checking how many rows are there in the dataset?")
print(len(df), '\n')

print("\n Find the missing values for all columns.")
missing_values_per_column = df.isnull().sum()
print(missing_values_per_column)

print("Checking which columns has more than 100 mising values \n")
columns_with_more_than_100_missing_values = missing_values_per_column[missing_values_per_column > 100].index
print(columns_with_more_than_100_missing_values)

print("Dropping columns that have more than 100 missing values \n")
df = df.drop(columns=columns_with_more_than_100_missing_values)
print(df)

print("Checking which columns are not needed")
print(df.columns)
df = df.drop(columns=['Indicator Name', 'Indicator Code'])
print(df.columns)

mask = df['2021'].isnull()
print(mask)
print(df.loc[mask, :])

print("Removing countries where data for 2020 and 2021 are missing")
mask = df['2020'].isnull() & df['2021'].isnull()
print(df.loc[mask, :]) #checking the data

# Drop countries without data
df.drop(df[mask].index, inplace = True)
df_2020_2021 = df.loc[:, ["Country", "2020", "2021"]] #checking data
print(df_2020_2021)

df.to_csv("gdp_per_capita_ppp_constant_2017_modified.csv", index=False)