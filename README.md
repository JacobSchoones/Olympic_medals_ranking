# Olympic Medal Analysis

I made this code to determine the best olympic countries. I got this idea from a youtube video: https://www.youtube.com/watch?v=5fR__LXDkRg

When looking at a medal ranking, you can not determine which country is the best in sports.
Countries with more inhabitants will earn more medals. To overcome this problem people have made rankings which show the number of medals per million inhabitants.
This ranking system is also flawed, because it is impossible for big countries to place high in this ranking system.

So a better ranking system is to look at the chance it takes for a country to win as many medals as it won. In this system you assume every person on earth has the same chance to win a medal
Using math you can calculate the probability that a country won as many medals as it did. The country with the lowest probability score has the best sporters. 

The method to use probability to calculate the best olympic country also has some flaws. e.g. bigger countries are still at a disadvantage, because most sports 
have a limit to how many sporters can participate. Also countries with a lot of money have higher chance to win medals, because (most) sports are pay to win.
So it is not perfect ranking system, but a perfect ranking system doesn't exist. 

The Youtuber from which I got this idea already calculated this for the summer and winter games between 1988 and 2016, but as far as I know he didn't make a python script for it which could 
be used for future olympic games. So that is exactly what I did. I used population-size data from this website: https://www.worldometers.info/world-population/population-by-country/ .
I used the medals per country data of the paris olympic games from this website: https://www.bbc.com/sport/olympics/paris-2024/medals .
I don't know anything about copyright, so this could be illegal. But who cares...

The python code combines the data from both websites and will calculate the winning chances of each country. The probability that a country wins a medal in an event is simply the percentage of inhabitants of the country relative to the population of the entire earth. The probability of a country winning X amount of medals or more in the entire olympics (P(medals >= X)) can be calculated using the survival function of a binomial distribution:

\[
P(X > k) =
\sum_{i=k+1}^{n}
\binom{n}{i}
p^i (1-p)^{n-i}.
\]

P(X > k) = Σ(i = k+1 to n) [C(n, i) · p^i · (1-p)^(n-i)]

 in which:
 - n is the total number of medals 
 - k is the number of medals won by a country 
 - p is the population percentage of a country


## Installation

To install the right libraries run the following line:

```bash
pip install -r requirements.txt
```


## Libraries

- numpy
- pandas
- scipy
- requests
- beautifulsoup4
- math 

## License

I don't know anything about this, but feel free to use this however you like.

## Contact

e-mail: jacobschoones05@gmail.com