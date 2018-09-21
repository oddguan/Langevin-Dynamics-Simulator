# -*- coding: utf-8 -*-

"""Main module."""

import argparse

def parse_args(args):
    """
    An parsing argument function that allows the program
    to read input from the user.

    Args:
        args: Unparsed argument variable.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--init_pos', \
    help='The initial position of the particle')
    parser.add_argument('--velocity', \)