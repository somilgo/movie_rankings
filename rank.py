import csv
import os
import sys
import signal
import get_char
import movie_ranking_io


def read_letterboxd_movies(letterboxd_watched_file):
    return movie_ranking_io.read_csv_as_dictionary(letterboxd_watched_file)

def create_movie_ranking_row(letterboxd_row):
    return { k : v for k,v in letterboxd_row.items() }

def add_subparser(subparsers):
    help = "Use a CSV exported from Letterboxd to create an ordering of all of the movies"
    foo_parser = subparsers.add_parser('rank', help=help, description=help)
    foo_parser.add_argument('-letterboxd-watched-file', required=True, help="Exported watched.csv from Letterboxd")
    foo_parser.add_argument('-movie-rankings-file', required=False,
                            default="./movie-rankings.csv", help="State for storing movie ratings. If it doesn't exist, one will be created as \'movie-ratings.csv\'")

def get_ranked_movie_set(movie_rankings):
    return { ranking['Letterboxd URI'] for ranking in movie_rankings }

def rank_movies(letterboxd_watched, movie_rankings):
    ranked_movies = get_ranked_movie_set(movie_rankings)
    for watched in letterboxd_watched:
        if watched['Letterboxd URI'] in ranked_movies:
            continue
        currently_ranking = watched['Name']
        print("--------------")
        print("Ranking {} ({})".format(currently_ranking, watched['Year']))
        skip = False
        lo = 0
        hi = len(movie_rankings) - 1
        while lo <= hi:
            mid = int((lo + hi) / 2)
            compare_with = movie_rankings[mid]
            print("{} ({}) : is {} better or worse?".format(compare_with['Name'],
                                                            compare_with['Year'],
                                                            currently_ranking))
            result = movie_ranking_io.up_or_down()
            if result == None:
                skip = True
                break
            if result:
                lo = mid + 1
                hi = hi
            else:
                lo = lo
                hi = mid - 1
        if skip:
            print("Skipping...")
        else:
            print("Done ranking!")
            movie_rankings.insert(lo, create_movie_ranking_row(watched))



def command(letterboxd_watched_file, movie_rankings_file):
    letterboxd_watched = read_letterboxd_movies(letterboxd_watched_file)
    movie_rankings = movie_ranking_io.read_or_create_movie_rankings(movie_rankings_file)
    rank_movies(letterboxd_watched, movie_rankings)
    os.kill(os.getpid(), signal.SIGINT)
