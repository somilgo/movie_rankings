import movie_ranking_io
import csv

def search_for_rating(movie_rankings, rating):
    lo = 0
    hi = len(movie_rankings) - 1
    while lo <= hi:
        mid = int((lo + hi) / 2)
        compare_with = movie_rankings[mid]
        print("{} ({}) : is the worst {}-star movie better or worse than this movie?"
              .format(compare_with['Name'],compare_with['Year'],rating))
        result = movie_ranking_io.up_or_down()
        if result == None:
            print("Can't skip")
            raise BaseException
        if result:
            lo = mid + 1
            hi = hi
        else:
            lo = lo
            hi = mid - 1
    print("{} is the worst {}-star movie.".format(movie_rankings[lo]['Name'], rating))
    return(int(movie_rankings[lo]['Ranking']))




def search_for_ratings(movie_rankings, ratings):
    return [ (rating, search_for_rating(movie_rankings, rating)) for rating in ratings ]

movie_ratings_header = ['Date',"Name","Year","Letterboxd URI", "Rating"]
def to_letterboxd_csv(movie_rankings, movie_ratings_file):
    with open(movie_ratings_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(movie_ratings_header)
        for ranking in movie_rankings:
            writer.writerow([ranking[col] for col in movie_ratings_header])

def add_subparser(subparsers):
    help = "Convert a rankings file to a Letterboxd ratings file. Do a 'rank' first."
    foo_parser = subparsers.add_parser('convert_to_ratings', help=help, description=help)
    foo_parser.add_argument('-movie-rankings-file', required=False,
                            default="./movie-rankings.csv", help="Movie rankings from the 'rank' subcommand")
    foo_parser.add_argument('-movie-ratings-file', required=False,
                            default="./movie-ratings.csv", help="Output file for letterboxd-friendly CSV")

def command(movie_rankings_file, movie_ratings_file):
    movie_rankings = movie_ranking_io.read_or_create_movie_rankings(movie_rankings_file)
    base_ratings = search_for_ratings(movie_rankings, [1, 2, 3, 4, 5])
    base_ratings.append((5,0))
    for movie_ranking in movie_rankings:
        current_ranking = int(movie_ranking['Ranking'])
        prev = (0, len(movie_rankings))
        least_upper_bound = base_ratings[1]
        for rating,ranking in base_ratings:
            if current_ranking >= ranking:
                least_upper_bound = (rating, ranking)
                break
            prev = (rating,ranking)
        rating = (float(prev[1] - float(movie_ranking['Ranking'])) / float(prev[1] - least_upper_bound[1])) * float(least_upper_bound[0] - prev[0]) + prev[0]
        movie_ranking['Rating'] = (round(rating * 2.0) / 2)
    to_letterboxd_csv(movie_rankings, movie_ratings_file)
