import argparse
import rank

def run():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser")
    rank.add_subparser(subparsers)
    kwargs = vars(parser.parse_args())
    globals()[kwargs.pop('subparser')].command(**kwargs)
