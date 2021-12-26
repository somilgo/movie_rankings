# Somil's Fancy Movie Rater
Rate movies with a total ordering rather than a 5-star or 10 point rating that loses relativity quickly. 

Sure, a rating is easier to come up with than a ranking, but rankings are pretty easy too! To perfectly rank a new movie if you already have 1,000,000 movies in your collection takes 20 comparisons. If you're truly a movie buff... is that so much to ask?

## Quick Start
Download your Letterboxd watched movies by going to Settings > Import & Export. Then run the following command:

```
❯ python movie_rater.py rank -letterboxd-watched ~/Downloads/watched.csv
--------------
Ranking Inception
Knives Out : is Inception better or worse?
Pulp Fiction : is Inception better or worse?
bad key pressed!
Press ',' if it is worse and '.' if it is better
Done ranking!
--------------
Ranking Get Out
Inception : is Get Out better or worse?
```

Press CTRL+C to exit and your rankings so far will be saved. Your rankings will be created in a movie-ratings.csv file in the current working directory by default:
```
❯ cat movie-ratings.csv
Date,Name,Year,Letterboxd URI,Ranking
2021-08-08,Parasite,2019,https://boxd.it/hTha,1
2021-08-08,Pulp Fiction,1994,https://boxd.it/29Pq,2
2021-08-08,Inception,2010,https://boxd.it/1skk,3
2021-08-08,Knives Out,2019,https://boxd.it/jWEA,4
2021-08-08,Joker,2019,https://boxd.it/h4cS,5
```

Disagree with my movie rankings? Let's see yours *insert inhaling face emoji*!
