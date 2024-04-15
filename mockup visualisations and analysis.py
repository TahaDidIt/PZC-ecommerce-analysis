# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 17:55:16 2024

@author: Taha
"""

##### SET-UP
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import norm

#Loading data
csvPath = "C:/Taha/projects/Data Science Fundamentals with Python and SQL/PZ Cussons presentation working directory/data.csv"
dataset = pd.read_csv(csvPath, encoding = "unicode escape")

print(dataset.describe)

#Top items dataset
csv2Path = "C:/Taha/projects/Data Science Fundamentals with Python and SQL/PZ Cussons presentation working directory/topitems.csv"
topItemsData = pd.read_csv(csv2Path)

#Creating a new dataset where orders are grouped together (invoiceNo not repeating)
transactionsData = dataset.groupby("InvoiceNo").agg({
    "StockCode": lambda x: ",".join(x),
    "Quantity": "sum",
    "InvoiceDate": "first",
    "CustomerID": "first",
    "Country": "first"
})
#Removing crazy quantity values
minQuantity = 0
maxQuantity = 1000
transactionsData = transactionsData[transactionsData["Quantity"] >= minQuantity]
transactionsData = transactionsData[transactionsData["Quantity"] <= maxQuantity]





##### ANALYSIS

#Boxplots
def boxPlot1():
    plt.figure(figsize = (6,2))
    ax = sns.boxplot(x = "Quantity", data = transactionsData,
                     showfliers = False)
    ax.grid(axis = "x", linestyle = "--")
    ax.set_title("Items per Transaction")
    plt.show()



def pieChart1():
    """NOTE: Creating a pie chart off of the dataset would lead to a pretty unhelpful
    chart, as the cast majority would be the UK, and a minority of many many countries
    cramped together. Hence, we use a mock pie chart in this case. I've left the original
    code below for an actual pie chart based off the data. But it won't be pretty. 
    
    plt.figure(figsize = (5,5))
    countryCount = transactionsData["Country"].value_counts()
    plt.pie(countryCount, labels = countryCount.index, autopct='%1.1f%%')
    plt.title('Transactions by Country')
    plt.axis('equal')
    plt.show()
    """
    countryCount = {"United Kingdom": 70, "Germany": 43, "France": 34, "Belgium": 15,
                    "Other": 13}
    countryCount = pd.Series(countryCount)
    plt.pie(countryCount, labels = countryCount.index, autopct='%1.1f%%')
    plt.title('Transactions by Country')
    plt.axis('equal')
    plt.show()


### Multi-country boxplot 
def boxPlot2():
    # Calculate transaction count for each country
    countryCount = transactionsData['Country'].value_counts()

    # Select the top 5 countries
    countryCountTop5 = countryCount.head(5).index

    # Filter the dataset to include only transactions from the top 5 countries
    top5CountryData = transactionsData[transactionsData['Country'].isin(countryCountTop5)]
    
    plt.figure(figsize = (6,3))
    ax = sns.boxplot(x = "Quantity", y = "Country", data = top5CountryData,
                     showfliers = False)
    ax.grid(axis = "x", linestyle = "--")
    ax.set_title("Items per Transaction")
    plt.show()
    

# Bar chart (most sold items)
def barChart1():
    sns.set(font_scale = 1.5)
    plt.figure(figsize = (7, 4))
    sns.barplot(x = "TotalQuantity", y = "Description", data = topItemsData, 
                ci = None)
    plt.title("Most Purchased Items")
    plt.xlabel("Units Sold")
    plt.ylabel("Item")
    plt.show()


"""
###Co-occurences
# Create a new DataFrame to store item co-occurrences
co_occurrences = pd.DataFrame(columns=['item1', 'item2', 'count'])

# Iterate over each row in the DataFrame
for _, row in transactionsData.iterrows():
    items = row['StockCode'].split(',')  # Split itemIDs into a list
    n = len(items)
    # Generate pairs of items and update co-occurrence counts
    for i in range(n):
        for j in range(i + 1, n):
            item1, item2 = min(items[i], items[j]), max(items[i], items[j])
            # Check if the pair already exists in the DataFrame
            mask = (co_occurrences['item1'] == item1) & (co_occurrences['item2'] == item2)
            if mask.any():
                # Increment count if pair exists
                co_occurrences.loc[mask, 'count'] += 1
            else:
                # Add new row if pair doesn't exist
                newRow = pd.Series({'item1': item1, 'item2': item2, 'count': 1})
                co_occurrences = pd.concat([co_occurrences, newRow], ignore_index=True)

# Sort the DataFrame by count in descending order
co_occurrences = co_occurrences.sort_values(by='count', ascending=False)

# Display the top co-occurring item pairs
print(co_occurrences.head(10))
"""



##### MENU

### Visualisations index
plotFunctions = {1: boxPlot1, 2: pieChart1, 3: boxPlot2,
                 4: barChart1}


### Menu
menuChoice = ""

while menuChoice != "0":
    #Time and spacer for ease of reading
    print("")
    print("")
    print("")
    print("########## ", "Current Time: ", datetime.now().strftime("%H:%M:%S"))
    print("")
    #Menu choices
    print("Main Menu:")
    for i in plotFunctions:
        print(i, ": ", plotFunctions[i])
    
    menuChoice = input("Please select a number from the options: ")
    if menuChoice == "0":
        pass
    elif int(menuChoice) in plotFunctions:
        print("")
        plotFunctions[int(menuChoice)]()
    else:
        print("Invalid choice, please try again.")