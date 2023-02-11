import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from tabulate import tabulate
import seaborn as sns


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


file_name = "C:/Users/kuczy/Documents/GitHub/Why-nations-rise-and-fall/gdp_per_capita_ppp_constant_2017.csv"

df = pd.read_csv(file_name)

df.rename(columns={df.columns[0]: "Country"}, inplace= True)

duplicate_rows = df.duplicated()
print(f"This data contains {duplicate_rows.sum()} duplicated rows.\n")

print("Checking how many rows are   there in the dataset?")
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

print("Count growth of all countries from 1990 to 2021 \n")
#fullfill empty series in column 1990 with .bfill() method, which fills missing values with the next non-null value in the column
df = df.bfill( axis= 1)

#print(tabulate(df, headers='keys'))
#add column with growth from 1990 to 20221
df['2021'] = df['2021'].astype(float)
df['1990'] = df['1990'].astype(float)
df['Growth'] = round(df["2021"]/df["1990"] - 1, 2)

# Sort values of the dataframe based on column 'Growth' in descending order
top_10 = df.sort_values(by='Growth', ascending=False, inplace=True)
print(top_10)

# Print 5 random rows from the sorted dataframe
#print(df.sample(5))


#plot a bar chrt for top 10 exonomies:
#create_bar_chart(df=df, n=31, title="Top 10 best growing countries", value_column="Growth")

# Load the 'area.csv' file and skip first 4 rows
file_area = "area.csv"
df_area = pd.read_csv(file_area, skiprows=4, encoding='UTF-8')

# Print the loaded dataframe
#print(df_area)

# Rename the column '2020' to 'Area' in the dataframe 'df_area'
df_area.rename(columns={"2020" : "Area"}, inplace=True)
# Print the modified dataframe
#print(df_area)

print('Merge the dataframes \'df\' and \'df_area\' on the common column \'Country Code\'')

# with the type of merge being 'left'
df = df.merge(df_area[["Country Code", 'Area']], on='Country Code', how='left')

# Check data type of column and column "Area"
#print(df.dtypes)

# Change ',' to '.' to convert column "Area" to float to perform mathematical operations on it
df['Area'] = df['Area'].astype(str).str.replace(',', '.').astype(float)

# Check if column type has changed
#print(df['Area'].dtypes)

# Create scatter plot of "Growth" and "Area"
sns.regplot(x="Area", y="Growth", data=df)
plt.ylim(0,)
#plt.show()

# Check correlation between Growth of country and its size
print(df[["Growth", "Area"]].corr())

'''
Conclusion: The regression analysis suggests that the area of a country is not a strong predictor of its growth. The regression line is close to horizontal, indicating a weak relationship between the two variables. Additionally, the data points are widely dispersed and far from the fitted line, demonstrating a high degree of variability. These findings suggest that area is not a reliable variable for predicting growth.
It is worth noting that while the relationship between area and growth may be weak overall, there may be exceptions in specific countries. For instance, large countries such as Russia, Brazil, and China are relatively poor, while other large countries such as Canada, the United States, and Australia are wealthy. This highlights the complexity of the relationship between area and growth and the need for further examination to better understand it.
'''

# Check corelation between population size and economic growth
df_population = pd.read_csv("population.csv", encoding='UTF-8')

# checking an average size of population for every country from 1990 to 2021 year and adding
# it to new created column called population
df_population["Population"] = df_population.iloc[:, 34:65].mean(axis=1)

# float_format is set to a function that formats floating point numbers with a comma as a thousands separator,
# and with no decimal places to read more comfortable data
pd.options.display.float_format = '{:,.0f}'.format

# with the type of merge being 'left'
df = df.merge(df_population[["Country Code", 'Population']], on='Country Code', how='left')

# Check data type of column and column "Population"
#print(df.dtypes)

# Check correlation between Growth of country and its size of Population
print(df[["Growth", "Population"]].corr())

# Create scatter plot of "Growth" and "Population"
sns.regplot(x="Population", y="Growth", data=df)
plt.ylim(0,)
#plt.show()

'''
Conclusion: The results of the regression analysis indicate that population does not have a strong correlation with growth. The regression line is close to horizontal, indicating a weak relationship between the two variables. Furthermore, the data points are widely dispersed from the fitted line, showing a significant amount of variability. These findings suggest that population is not a reliable predictor of growth.
It is important to note that while the relationship between population and growth may be weak in general, there may be exceptions in specific countries. For example, in countries such as India, Brazil, Egypt, and China, despite having large populations, they are considered to be relatively poor. On the other hand, in wealthy countries such as the United States and Japan, there are also large populations. This highlights the complexity of the relationship between population and growth and the need for further analysis to fully understand it.
'''
# Check corelation between economy freedom  and economic growth
# New table new challange


#print(df)
#print(tabulate(df, headers="keys"))

#save df to csv
df.to_csv("gdp_per_capita_ppp_constant_2017_modified.csv", index=False)


