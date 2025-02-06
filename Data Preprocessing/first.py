import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sklearn.linear_model
# load data from the csv file
oecd_bli=pd.read_csv("oecd_bli_2015.csv",thousands=',')
gdp_per_capita=pd.read_csv("gdp_per_capita.csv",thousands=',',delimiter='\t',encoding='latin1',na_values="n/a")

def prepare_country_stats(oecd_bli, gdp_per_capita):
    # Process data
    oecd_bli = oecd_bli[oecd_bli["INEQUALITY"]=="TOT"]
    oecd_bli = oecd_bli.pivot(index="Country", columns="Indicator", values="Value")
    gdp_per_capita.rename(columns={"2015": "GDP per capita"}, inplace=True)
    gdp_per_capita.set_index("Country", inplace=True)
    full_country_stats = pd.merge(left=oecd_bli, right=gdp_per_capita,
                                  left_index=True, right_index=True)
    full_country_stats.sort_values(by="GDP per capita", inplace=True)
    remove_indices = [0, 1, 6, 8, 33, 34, 35]
    keep_indices = list(set(range(36)) - set(remove_indices))
    return full_country_stats[["GDP per capita", 'Life satisfaction']].iloc[keep_indices]
    

 
# prepare the data 
country_stats = prepare_country_stats(oecd_bli, gdp_per_capita)    
x=np.c_[country_stats["GDP per capita"]]
y=np.c_[country_stats["Life satisfaction"]]



# visualize the data    
country_stats.plot(kind='scatter',x="GDP per capita",y='Life satisfaction')
plt.show()

# select a linear model
model=sklearn.linear_model.LinearRegression()

# train the model
model.fit(x,y)

# make a prediction for Cyprus
X_new=[[22587]] # Cyprus' GDP per capita
print(model.predict(X_new)) # outputs
