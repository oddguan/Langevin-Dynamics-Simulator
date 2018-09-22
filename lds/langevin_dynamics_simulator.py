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
    parser.add_argument('-x0', '--initial_position', type=float, \
    help='The initial position of the particle')
    parser.add_argument('-v0', '--initial_velocity', type=float, \
    help='The intial velocity of the particle')
    parser.add_argument('-temp', '--temperature', type=float, \
    help='The temperauture that the simulator runs at')
    parser.add_argument('-dc', '--damp_coeff', type=float, \
    help='The damping coefficient of the system')
    parser.add_argument('-ts', '--time_step', type=float, \
    help='Time step of the simulation process')
    parser.add_argument('-tt', '--total_time', type=float, \
    help='The total time of the simulation process')

    return vars(parser.parse_args(args))