# Somil's Fancy Movie Ranker
Rank movies with a total ordering rather than a 5-star or 10 point rating that loses relativity quickly.

Sure, a rating is easier to come up with than a ranking, but rankings are pretty easy too! To perfectly rank a new movie if you already have 1,000,000 movies in your collection takes 20 comparisons. If you're truly a movie buff... is that so much to ask?

## Quick Start
Download your Letterboxd watched movies by going to Settings > Import & Export. Then run the following command:

```
❯ python movie_ranker.py rank -letterboxd-watched ~/Downloads/watched.csv
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

Press CTRL+C to exit and your rankings so far will be saved. Your rankings will be created in a **movie-rankings.csv** file in the current working directory by default:
```
❯ cat movie-rankings.csv
Date,Name,Year,Letterboxd URI,Ranking
2021-08-08,Parasite,2019,https://boxd.it/hTha,1
2021-08-08,Pulp Fiction,1994,https://boxd.it/29Pq,2
2021-08-08,Inception,2010,https://boxd.it/1skk,3
2021-08-08,Knives Out,2019,https://boxd.it/jWEA,4
2021-08-08,Joker,2019,https://boxd.it/h4cS,5
```

Disagree with my movie rankings? Let's see yours *insert inhaling face emoji*!

## Converting Rankings to Ratings and Importing to Letterboxd
Now that you have rankings of all of your movies, you can create very accurate ratings as well. Just run the following which will ask you a series of questions to try to find the greatest lower bound for each star ranking:
```
❯ python3 movie_ranker.py convert_to_ratings
Onward (2020) : is the worst 1-star movie better or worse than this movie?
Legally Blonde (2001) : is the worst 1-star movie better or worse than this movie?
Cars (2006) : is the worst 1-star movie better or worse than this movie?
Mad Max: Fury Road (2015) : is the worst 1-star movie better or worse than this movie?
Black Widow (2021) : is the worst 1-star movie better or worse than this movie?
Captain America: Civil War (2016) : is the worst 1-star movie better or worse than this movie?
Captain Marvel (2019) : is the worst 1-star movie better or worse than this movie?
Captain America: Civil War is the worst 1-star movie.
```
Then, it will linearly interpolate between these base ratings using the rankings file from above to create accurate ratings. You can upload the resulting 'movie-ratings.csv' file to letterboxd. Enjoy!
