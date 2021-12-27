import csv
import os.path
from functools import partial
import signal
import get_char

def up_or_down():
    input_ch = ord(get_char.getch())
    if input_ch == 46:
        return True
    if input_ch == 44:
        return False
    if input_ch == 115:
        return None
    if input_ch == 3:
        os.kill(os.getpid(), signal.SIGINT)
    print("Invalid key pressed: {}".format(input_ch))
    print("Press ',' if it is worse and '.' if it is better (press 's' to skip if you haven't seen it). ")
    return up_or_down()

def read_csv_as_dictionary(csv_file):
    with open(csv_file, 'r') as f:
        rows = [{k: v for k, v in row.items()}
             for row in csv.DictReader(f, skipinitialspace=True)]
    return rows

movie_rankings_header = ['Date',"Name","Year","Letterboxd URI", "Ranking"]
def read_or_create_movie_rankings(movie_rankings_file):
    if not os.path.isfile(movie_rankings_file):
        with open(movie_rankings_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(movie_rankings_header)
    rows = read_csv_as_dictionary(movie_rankings_file)
    movie_rankings = sorted(rows, reverse=True, key=lambda movie:int(movie["Ranking"]))
    exit_signal_handler = partial(exit_and_save_rankings, movie_rankings, movie_rankings_file)
    signal.signal(signal.SIGINT, exit_signal_handler)
    signal.signal(signal.SIGTERM, exit_signal_handler)
    return movie_rankings

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
