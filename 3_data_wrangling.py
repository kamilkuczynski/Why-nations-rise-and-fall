import pandas as pd

file_name = "C:/Users/kuczy/Documents/GitHub/Why-nations-rise-and-fall/gdp_per_capita_ppp_constant_2017.csv"

df = pd.read_csv(file_name)

df.rename(columns={df.columns[0]: "Country"}, inplace= True)

duplicate_rows = df.duplicated()
print(f"This data contains {duplicate_rows.sum()} duplicated rows.\n")

print("Checking how many rows are there in the dataset?")
#print(len(df), '\n')

print("\n Find the missing values for all columns. \n")
missing_values_per_column = df.isnull().sum()
#print(missing_values_per_column)

print("Checking which columns has more than 100 mising values \n")
columns_with_more_than_100_missing_values = missing_values_per_column[missing_values_per_column > 100].index
#print(columns_with_more_than_100_missing_values)

print("Dropping columns that have more than 100 missing values \n")
df = df.drop(columns=columns_with_more_than_100_missing_values)
#print(df)

print("Checking which columns are not needed\n")
#print(df.columns)
df = df.drop(columns=['Indicator Name', 'Indicator Code'])
#print(df.columns)

mask = df['2021'].isnull()
#print(mask)
#print(df.loc[mask, :])

print("Removing countries where data for 2020 and 2021 are missing \n")
mask = df['2020'].isnull() & df['2021'].isnull()
#print(df.loc[mask, :]) #checking the data

# Drop countries without data
df.drop(df[mask].index, inplace = True)
df_2020_2021 = df.loc[:, ["Country", "2020", "2021"]] #checking data
#print(df_2020_2021)

# changing datatype from string to float
cols = [str(year) for year in range(1990, 2022)]
df[cols] = df[cols].apply(lambda x: x.str.replace(',', '.')).astype(float)


#save df to csv
df.to_csv("gdp_per_capita_ppp_constant_2017_modified.csv", index=False)

print("Count growth of all countries from 1990 to 2021 \n")
#fullfill empty series in column 1990 with .bfill() method, which fills missing values with the next non-null value in the column
df["1990"].bfill(inplace=True)

#add column with growth from 1990 to 20221
df['Growth'] = round(df["2021"]/df["1990"] - 1, 2)

# Sort values of the dataframe based on column 'Growth' in descending order
df.sort_values(by='Growth', ascending=False, inplace=True)
# Print 5 random rows from the sorted dataframe
print(df.sample(5))

# Load the 'area.csv' file and skip first 4 rows
file_area = "area.csv"
df_area = pd.read_csv(file_area, skiprows=4, encoding='UTF-8')
# Print the loaded dataframe
print(df_area)

# Rename the column '2020' to 'Area' in the dataframe 'df_area'
df_area.rename(columns={"2020" : "Area"}, inplace=True)
# Print the modified dataframe
print(df_area)

# Merge the dataframes 'df' and 'df_area' on the common column 'Country Code'
# with the type of merge being 'left'
df = df.merge(df_area[["Country Code", 'Area']], on='Country Code', how='left')
# Save the merged dataframe to a csv file
df.to_csv("gdp_per_capita_ppp_constant_2017_modified_by-area.csv", index=False)
