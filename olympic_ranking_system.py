# I made this code to determine the best olympic countries. I got this idea from a youtube video: https://www.youtube.com/watch?v=5fR__LXDkRg
#
# When looking at a medal ranking, you can not determine which country is the best in sports.
# Countries with more inhabitants will earn more medals. To overcome this problem people have made rankings which show the number of medals per million inhabitants.
# This ranking system is also flawed, because it is impossible for big countries to place high in this ranking system.
# 
# So a better ranking system is to look at the chance it takes for a country to win as many medals as it won. In this system you assume every person on earth has the same chance to win a medal
# Using math you can calculate the probability that a country won as many medals as it did. The country with the lowest probability score has the best sporters. 
#
# The method to use probability to calculate the best olympic country also has some flaws. e.g. bigger countries are still at a disadvantage, because most sports 
# have a limit to how many sporters can participate. Also countries with a lot of money have higher chance to win medals, because (most) sports are pay to win.
# So it is not perfect ranking system, but a perfect ranking system doesn't exist. 
#
# The Youtuber from which I got this idea already calculated this for the summer and winter games between 1988 and 2016, but as far as I know he didn't make a python script for it which could 
# be used for future olympic games. So that is exactly what I did. I used population-size data from this website: https://www.worldometers.info/world-population/population-by-country/ .
# I used the medals per country data of the paris olympic games from this website: https://www.bbc.com/sport/olympics/paris-2024/medals .
# I don't know anything about copyright, so this could be illegal. But who cares...

from bs4 import BeautifulSoup  #used for HTML scraping 
import requests   #used to enter web pages
import pandas as pd  #used to process tables
import numpy as np 
import math
from scipy.stats import binom

np.set_printoptions(threshold=np.inf)  #makes sure that the entire numpy array is printed

total_population = 0
total_gold = 0
total_silver = 0
total_bronze = 0


page_population = requests.get("https://www.worldometers.info/world-population/population-by-country/")   #load the page with population data
soup_population = BeautifulSoup(page_population.text, "html.parser")  #get the HTML lines of the website


countries1 = soup_population.find_all("a", attrs={"class":"transition-colors text-primary hover:text-primary/80"})    #scrape the country names for the website
populations = soup_population.find_all("td", attrs= {"class":"border-e border-zinc-200 px-2 border-b py-1.5 text-end font-bold"}) #scrape the population data from the website


countries_array = np.array([]) #making an empty country array
population_array = np.array([]) #making an empty population array

for i in range(len(populations)):            
    countries_array = np.append(countries_array, countries1[i].get_text(strip=True)) #putting country names in 1D array and deleting all the html nonsense, so we only have the text
    population_array = np.append(population_array, populations[i].get_text(strip=True)) #putting population data in 1D array

population_array = np.column_stack((countries_array,population_array))  #combining two 1D arrays into a 2D array


#manually add some missing countries
population_array = np.vstack((population_array, np.array(['Kosovo', '1,570,983'])))  #Kosovo wasn't included on the website, since it is not recognized by a lot of countries
population_array = np.vstack((population_array, np.array(['Refugee Olympic Team', '117,800,000']))) #Refugee team wasn't included on the website, since it is not a country 

#Changing the names of some countries, since some names on the medal website differ from the names on the population data website 
for i in range(len(population_array[:,0])):
    match population_array[i][0]:
        case 'United Kingdom':
            population_array[i][0] = 'Great Britain'     
        case 'Czech Republic (Czechia)':
            population_array[i][0] = 'Czech Republic'
        case 'Taiwan':
            population_array[i][0] = 'Chinese Taipei'
        case 'Saint Lucia':    
            population_array[i][0] = 'St Lucia'
        case 'Cabo Verde':
            population_array[i][0] = 'Cape Verde'
        case 'CÃ´te d\'Ivoire':
            population_array[i][0] = 'Ivory Coast'
        case 'Bosnia and Herzegovina':
            population_array[i][0] = 'Bosnia-Herzegovina'
        case 'State of Palestine':
            population_array[i][0] = 'Palestine'
        case 'Sao Tome & Principe':
            population_array[i][0] = 'Sao Tome and Principe'
        case 'Saint Kitts & Nevis':
            population_array[i][0] = 'St Kitts and Nevis'
        case 'St. Vincent & Grenadines':
            population_array[i][0] = 'St Vincent and the Grenadines'
        case 'Timor-Leste':
            population_array[i][0] = 'East Timor'
        case 'U.S. Virgin Islands':
            population_array[i][0] = 'American Virgin Islands'


print("\n\n\n")



url = "https://www.bbc.com/sport/olympics/paris-2024/medals"   #load the page with medal data

tables = pd.read_html(url)    #read the table from the website
table = tables[0]

medals = table[["Country", "GGold", "SSilver", "BBronze"]]  #only take the columns with the information we want
medals_array = medals.to_numpy()   #convert table to 2D numpy array

new_col = np.full((medals_array.shape[0], 4), -1, dtype=medals_array.dtype)  #making space for 8 new columns, these columns are used to store the results of some calculations
medals_array = np.hstack((medals_array, new_col))


for i in range(len(medals_array[:,0])):  #loop through the entire medal table 

#The country names in the table are shown like this: "CHNChina". The first three capital letters (or 2) should be deleted so the names correspond with the names in the population array
    if medals_array[i][0][3].isupper():
        medals_array[i][0] = medals_array[i][0][3:]  #deleting first three capital letters if the fourth letter is uppercase
    elif medals_array[i][0][2].isupper():
        medals_array[i][0] = medals_array[i][0][2:]  #deleting first two capital letters if the fourth letter is lowercase


    for j in range(len(population_array[:,0])):       #loop through the population array
        if medals_array[i][0] == population_array[j][0]:  #when the country names match, the population data gets copied to the medals array
            medals_array[i][4] = int(population_array[j][1].replace(",", ""))  #the population data gets converted from a string to an integer
            break
        elif j == (len(population_array[:,0])-1):  #error handling:  print error message when country name is not found in population array  
            print("!!!!ERROR!!!! \nCould not find a country name match in the population table for " + medals_array[i][0] + "\nAdd/Change the name of this country in the population table, so it matches with the name in the medal table\n\n")
    

    total_population += medals_array[i,4]  #the total population is the sum of all the individual countries
    total_gold += medals_array[i,1]        #summing the gold medals of each country 
    total_silver += medals_array[i,2]      #summing the silver medals of each country 
    total_bronze += medals_array[i,3]      #summing the bronze medals of each country 


total_gold_silver = total_gold + total_silver
total_gold_silver_bronze = total_gold_silver + total_bronze



for i in range(len(medals_array[:,0])):  #looping through the entire medals array
    
    num_gold = medals_array[i][1]           #The amount of gold medals that a country has won 
    num_gold_silver = medals_array[i][2] + num_gold        #The amount of gold and silver medals a country has won
    num_gold_silver_bronze = medals_array[i][3] + num_gold_silver   #The amount of gold, silver and bronze medals a country has won
    p = medals_array[i][4] / total_population        #chance of a country winning a medal is the population of the country divided by total population

    #calculating the chance that a country won as many medals (or more) as it did
    sf_gold = binom.logsf(num_gold-1,total_gold,float(p))/math.log(0.4)     # P(amount_of_medals >= num_gold )  (survival function)
    sf_gold_silver = binom.logsf(num_gold_silver-1,total_gold_silver,float(p))/math.log(0.4)   # P(amount_of_medals >= num_gold + num_silver)  (survival function)
    sf_gold_silver_bronze = binom.logsf(num_gold_silver_bronze-1,total_gold_silver_bronze,float(p))/math.log(0.4) # P(amount_of_medals >= num_gold + num_silver + num_bronze )  (survival function)

    medals_array[i][5] = (sf_gold + sf_gold_silver + sf_gold_silver_bronze) / (3)  #taking the average of the three survival functions


#BONUS: Calculating the deviation from the expected amount of gold medals for each country. This could also be used as a ranking system
    medals_array[i][6] = medals_array[i][1] - (total_gold*p) 
    medals_array[i][7] = total_gold*p



medals_array = medals_array[:,[0,1,2,3,4,5]]  #determine which columns from the array you want to print

df = pd.DataFrame(
    medals_array,
    columns=["Country", "Gold", "Silver", "Bronze", "Population", "Impressiveness Score"]   #give each column a name
)

df = df.sort_values("Impressiveness Score", ascending=False)     #sorting the rows based on the impressiveness score

print(df.to_string()) #printing the table 

