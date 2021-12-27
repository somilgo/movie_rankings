import argparse
import rank
import convert_to_ratings

def run():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser")
    rank.add_subparser(subparsers)
    convert_to_ratings.add_subparser(subparsers)
    kwargs = vars(parser.parse_args())
    globals()[kwargs.pop('subparser')].command(**kwargs)
