import csv
import os.path
import sys
import signal
import get_char
from functools import partial

def read_csv_as_dictionary(csv_file):
    with open(csv_file, 'r') as f:
        rows = [{k: v for k, v in row.items()}
             for row in csv.DictReader(f, skipinitialspace=True)]
    return rows

def read_letterboxd_movies(letterboxd_watched_file):
    return read_csv_as_dictionary(letterboxd_watched_file)


movie_rankings_header = ['Date',"Name","Year","Letterboxd URI", "Ranking"]
def read_or_create_movie_rankings(movie_rankings_file):
    if not os.path.isfile(movie_rankings_file):
        with open(movie_rankings_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(movie_rankings_header)
    rows = read_csv_as_dictionary(movie_rankings_file)
    return sorted(rows, reverse=True, key=lambda movie:int(movie["Ranking"]))

def exit_and_save_rankings(movie_rankings, movie_rankings_file, *args):
    with open(movie_rankings_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(movie_rankings_header)
        ranking_counter = 0
        for ranking in reversed(movie_rankings):
            ranking_counter += 1
            ranking["Ranking"] = ranking_counter
            writer.writerow([ranking[col] for col in movie_rankings_header])
    exit()

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

def up_or_down():
    input_ch = ord(get_char.getch())
    if input_ch == 46:
        return True
    if input_ch == 44:
        return False
    if input_ch == 115:
        return None
    if input_ch == 3:
        exit_signal_handler()
    print("Invalid key pressed: {}".format(input_ch))
    print("Press ',' if it is worse and '.' if it is better (press 's' to skip if you haven't seen it). ")
    return up_or_down()

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
            result = up_or_down()
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
    global exit_signal_handler
    letterboxd_watched = read_letterboxd_movies(letterboxd_watched_file)
    movie_rankings = read_or_create_movie_rankings(movie_rankings_file)
    exit_signal_handler = partial(exit_and_save_rankings, movie_rankings, movie_rankings_file)
    signal.signal(signal.SIGINT, exit_signal_handler)
    signal.signal(signal.SIGTERM, exit_signal_handler)
    rank_movies(letterboxd_watched, movie_rankings)
    exit_signal_handler()
