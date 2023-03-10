import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from tabulate import tabulate
import seaborn as sns
from scipy import stats



def create_bar_chart(df, n, title, value_column):
    # get the first n rows of the dataframe
    df_first_n = df.head(n)
    df_first_n = df_first_n.sort_values(value_column, ascending=True)

    # plot the bar chart
    fig, ax = plt.subplots(figsize=(18, 7.5))

    # add bars
    bars = plt.barh(df_first_n['Country'], df_first_n[value_column], color="grey")
    bars[-1].set_color('black')  # Change color of the first bar

    # set y-axis
    plt.gca().set_yticklabels(df_first_n["Country"])

    # add title to a bar
    plt.title(title, fontsize=24, y=1.05)

    # rectangle first
    plt.gca().add_patch(
        plt.Rectangle(
            (-0.05, .95),  # location
            0.0125,  # width
            -0.13,  # height
            facecolor='tab:red',
            transform=fig.transFigure,
            clip_on=False,
            linewidth=0
        )
    )

    plt.show()


file_name = "C:/Users/kuczy/Documents/GitHub/Why-nations-rise-and-fall/3.0 gdp_per_capita_ppp_constant_2017.csv"

df = pd.read_csv(file_name)

print("\nPrint the first few rows of the DataFrame")
print(df.head())

df.rename(columns={df.columns[0]: "Country"}, inplace= True)

duplicate_rows = df.duplicated()
print(f"This data contains {duplicate_rows.sum()} duplicated rows.")

print("\nPrint the DataFrame's shape")
print(df.shape)

print("\nPrint the DataFrame's data types")
print(df.dtypes)

print("\nChecking how many rows are there in the dataset?")
print(len(df), '\n')

print("\nFind the missing values for all columns.")
missing_values_per_column = df.isnull().sum()
print(missing_values_per_column)

print("\nChecking which columns has more than 100 mising values")
columns_with_more_than_100_missing_values = missing_values_per_column[missing_values_per_column > 100].index
print(columns_with_more_than_100_missing_values)

print(" \nDropping columns that have more than 100 missing values")
df = df.drop(columns=columns_with_more_than_100_missing_values)
print(df.head())

print("\nChecking which columns are not needed")
#print(df.columns)
df = df.drop(columns=['Indicator Name', 'Indicator Code'])
print(df.columns)

mask = df['2021'].isnull()
#print(mask)
#print(df.loc[mask, :])

print("\nRemoving countries where data for 2020 and 2021 are missing")
mask = df['2020'].isnull() & df['2021'].isnull()
#print(df.loc[mask, :]) #checking the data

print("\nDrop countries without data")
df.drop(df[mask].index, inplace = True)
df_2020_2021 = df.loc[:, ["Country", "2020", "2021"]] #checking data

print("\nChanging datatype from string to float")
cols = [str(year) for year in range(1990, 2022)]
df[cols] = df[cols].apply(lambda x: x.str.replace(',', '.')).astype(float)

print("\nCount growth of all countries from 1990 to 2021")
#fullfill empty series in column 1990 with .bfill() method, which fills missing values with the next non-null value in the column
df = df.bfill( axis= 1)
df = df.ffill( axis= 1)

print("\nAdd column with growth from 1990 to 20221")
df['2021'] = df['2021'].astype(float)
df['1990'] = df['1990'].astype(float)
df['Growth'] = round(df["2021"]/df["1990"] - 1, 2)

# Print 5 random rows from the sorted dataframe
#print(df.sample(5))

#plot a bar chrt for top 10 excnomies:
#create_bar_chart(df=df, n=31, title="Top 10 best growing countries", value_column="Growth")

# float_format is set to a function that formats floating point numbers with a comma as a thousands separator,
# and with no decimal places to read more comfortable data
pd.options.display.float_format = '{:,.2f}'.format

print("\nLoad the 'area.csv' file and skip first 4 rows")
file_area = "3.0 area.csv"
df_area = pd.read_csv(file_area, skiprows=4, encoding='UTF-8')

# Print the loaded dataframe to check Are df
#print("Print the area df:\n", df_area)


print("\nRename the column '2020' to 'Area' in the dataframe 'df_area'")
df_area.rename(columns={"2020" : "Area"}, inplace=True)

print("\nPrint the modified dataframe")
print(df_area.head())

print('\nMerge the dataframes \'df\' and \'df_area\' on the common column \'Country Code\'')

# with the type of merge being 'left'
df = df.merge(df_area[["Country Code", 'Area']], on='Country Code', how='left')

# Check data type of column and column "Area"
#print(df.dtypes)

# Change ',' to '.' to convert column "Area" to float to perform mathematical operations on it
df['Area'] = df['Area'].astype(str).str.replace(',', '.').astype(float)


# Check if column type has changed
#print(df['Area'].dtypes)

print("\nCreate scatter plot of 'Growth' and 'Area'")
sns.regplot(x="Area", y="Growth", data=df, color="#1A00F3")
plt.ylim(0,)
plt.show()

print("\nCheck correlation between Growth of country and its size and P-value of Growth and Area to know the significant of the correlation estimate:")
print('\n', df[["Growth", "Area"]].corr())

df_clean= df.dropna(subset=['Area']) # removing countries with nan value in Area column

pearson_coef, p_value = stats.pearsonr(df_clean['Area'], df_clean['Growth'])

print("\nThe Pearson Correlation Coefficient is", round(pearson_coef, 3), " with a P-value of P =", round(p_value, 4))

'''
Based on the code, the Pearson Correlation Coefficient between the Growth and Area columns is 0.055. 
The P-value, which is the probability of observing a correlation as strong as the one computed from the sample, is 0.3995074419116786. 
Given the P-value is greater than 0.05, we can conclude that there is no statistically significant correlation between Growth and Area.
'''

# Check corelation between population size and economic growth
df_population = pd.read_csv("3.0 population.csv", encoding='UTF-8')

# checking an average size of population for every country from 1990 to 2021 year and adding
# it to new created column called population
df_population["Population"] = df_population.iloc[:, 34:65].mean(axis=1)

# with the type of merge being 'left'
df = df.merge(df_population[["Country Code", 'Population']], on='Country Code', how='left')

# Check data type of column and column "Population"
#print(df.dtypes)

print("\nCheck correlation between Growth of country and its size of Population")
print(df[["Growth", "Population"]].corr())

pearson_coef, p_value = stats.pearsonr(df['Population'], df['Growth'])

print("\nThe Pearson Correlation Coefficient is", round(pearson_coef, 3), " with a P-value of P =", round(p_value, 4), '\n')

print("\nCreate scatter plot of 'Growth' and 'Population'")
sns.regplot(x="Population", y="Growth", data=df, color="#1A00F3")
plt.ylim(0,)
plt.show()

'''
Conclusion: 
Based on the result of the Pearson Correlation Coefficient being 0.156 and the P-value being 0.0153, there is weak evidence that the correlation is significant.
The results of the regression analysis also indicate that population does not have a strong correlation with growth. 
The regression line is close to horizontal, indicating a weak relationship between the two variables. 
Furthermore, the data points are widely dispersed from the fitted line, showing a significant amount of variability. 
These findings suggest that population is not a reliable predictor of growth.
For example, in countries such as India, Brazil, Egypt, and China, despite having large populations, they are considered to be relatively poor. On the other hand, in wealthy countries such as the United States and Japan, there are also large populations. This highlights the complexity of the relationship between population and growth and the need for further analysis to fully understand it.
'''


# Check corelation between economy freedom  and economic growth
# New table new challange

# Load the data into a pandas DataFrame and calculate the mean of the 'Summary Index' column for each country in one line

# Import the data from the csv file into a pandas dataframe
df_economy_freedom = pd.read_csv("3.0 economicdata1990-2020.csv")

# Convert the "Economic Freedom Summary Index" column to a numerical type by first removing the commas and then converting to a float.
df_economy_freedom['Economic Freedom Summary Index'] = df_economy_freedom['Economic Freedom Summary Index'].str.replace(',', '.')
df_economy_freedom['Economic Freedom Summary Index'] = pd.to_numeric(df_economy_freedom['Economic Freedom Summary Index'])

# Print the column names of the dataframe to verify the conversion was successful.
#print(df_economy_freedom.columns)

# Calculate the mean of the "Economic Freedom Summary Index" column for each unique "ISO_Code".
mean = df_economy_freedom.groupby("ISO_Code")["Economic Freedom Summary Index"].mean()

# Reset the index of the mean dataframe to make the "ISO_Code" column a regular column.
mean = mean.reset_index()

# Rename the "ISO_Code" column to "Country Code".
mean = mean.rename(columns={'ISO_Code': 'Country Code'})

# Print the mean dataframe to verify the changes were successful.
#print(mean)

# Merge the mean dataframe with the main dataframe on the "Country Code" column.
df = df.merge(mean.reset_index(), how="left", on="Country Code")

print('\nRename the "Economic Freedom Summary Index" column to "Average Economic Freedom.')
df = df.rename(columns={"Economic Freedom Summary Index": "Average Economic Freedom"})

print('\nCalculate the correlation between the "Growth" and "Average Economic Freedom" columns.')
correlation_with_economic_freedom = df[["Growth","Average Economic Freedom"]].corr()

# Print the correlation results.
print('\n', correlation_with_economic_freedom)

df_clean = df.dropna(subset=['Average Economic Freedom']) # removing countries with nan value in Average Economic Freedom column

pearson_coef, p_value = stats.pearsonr(df_clean['Average Economic Freedom'], df_clean['Growth'])

print("The Pearson Correlation Coefficient is", round(pearson_coef, 3), " with a P-value of P =", round(p_value, 4), '\n')
sns.regplot(x="Average Economic Freedom", y="Growth", data=df, color="#1A00F3")
plt.ylim(0,)
plt.show()

print('\n, Correlation of with economic freedom with gdp per capita for 2021 year')

#df_clean = df.dropna(subset=['Average Economic Freedom']) # removing countries with nan value in Average Economic Freedom column

pearson_coef, p_value = stats.pearsonr(df_clean['Average Economic Freedom'], df_clean['2021'])

print("The Pearson Correlation Coefficient is", round(pearson_coef, 3), " with a P-value of P =", round(p_value, 4), '\n')

sns.regplot(x="Average Economic Freedom", y="2021", data=df, color="#1A00F3")
plt.ylim(0,)
plt.show()


# Print the final dataframe.
print(tabulate(df.head(), headers="keys"))

#save df to csv
df.to_csv("3.1 gdp_per_capita_ppp_constant_2017_modified.csv", index=False)