# -*- coding: utf-8 -*-

"""Main module."""

import sys
import os
import argparse
import numpy as np 
import matplotlib.pyplot as plt

def parse_args(args):
    """
    An parsing argument function that allows the program
    to read input from the user.

    Args:
        args: Unparsed argument variable.

    Returns:
        vars: a dict containing parsed arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-x0', '--initial_position', type=float, \
    help='The initial position of the particle')
    parser.add_argument('-v0', '--initial_velocity', type=float, \
    help='The intial velocity of the particle')
    parser.add_argument('-temp', '--temperature', type=float, \
    help='The temperauture that the simulator runs at')
    parser.add_argument('-dc', '--damping_coefficient', type=float, \
    help='The damping coefficient of the system')
    parser.add_argument('-ts', '--time_step', type=float, \
    help='Time step of the simulation process')
    parser.add_argument('-tt', '--total_time', type=float, \
    help='The total time of the simulation process')
    parser.add_argument('-ws', '--wall_size', type=float, \
    help='The wall size of the simulation process')
    parser.add_argument('-p', '--path', type=str, default='.', \
    help='Path to save the output file and graph, default to current directory')
    return vars(parser.parse_args(args))


def random_force(temperature, damping_coefficient, kB=1, dirac_delta=1):
    """
    Calculates the random force in langevin dynamics.
    Calculate the variance first, then plug into a 
    normal distribution to generate the random force.

    Args:
        temperature: the current operating temperature of the system.
        damping_coefficient: the damping coefficient of the system.
        kB: The Boltzman constant. Default to 1 in reduce unit.
        dirac_delta: dirac delta distribution of t-t'. Default to 1.
    
    Returns:
        a float contains the random force generated from gaussian distribution.
    """

    variance = 2 * temperature * damping_coefficient * kB * dirac_delta
    std_dev = np.sqrt(variance) # standard deviation is sqrt of variance
    return float(np.random.normal(0.0, std_dev))


def euler_integrator(damping_coefficient, initial_velocity, total_time, time_step, \
                    temperature, initial_position, wall, kB=1, dirac_delta=1):
    """
    A Euler Integration method.

    Args:
        damping_coefficient: the damping coefficient of the system.
        initial_velocity: the initial velocity of the particle.
        time: the total simulation time.
        time_step: the time step (dt) to be integrated on.
        temperature: the temperature of the system.
        initial_position: the initial position of the particle in the system.
        wall: the wall boundary for the system.
        kB: the Boltzman constant. Default to 1 in reduce unit.
        dirac_delta: dirac delta distribution of t-t'. Default to 1.

    Returns:
        velocity_list: a list of velocities of the particle at each time step.
        position_list: a list of positions of the partile at each time step.
        time_list: a list of time steps.
    """

    num_steps = int(total_time // time_step)
    drag_force = -damping_coefficient * initial_velocity
    velocity_list = list()
    position_list = list()
    time_list = list()
    velocity_list.append(initial_velocity)
    position_list.append(initial_position)
    time_list.append(0.0)

    for s in range(num_steps):
        Xi = random_force(temperature, damping_coefficient, kB, dirac_delta)
        acceleration = drag_force + Xi
        new_velocity = velocity_list[-1]+acceleration*time_step 
        new_position = position_list[-1]+velocity_list[-1]*time_step
        if new_position>wall or new_position<-wall:
            break
        new_time = time_list[-1] + time_step
        velocity_list.append(new_velocity)
        position_list.append(new_position)
        time_list.append(new_time)

    return velocity_list, position_list, time_list


def hit_wall(position_list, wall):
    """
    checks the current position of the particle. If the current position is 
    beyond the wall, return false. Otherwise return true.

    Args:
        position_list: a list that contains all positions of the particle at
        a each time step.
        wall: wall boundary for the system.

    Returns:
        boo: a boolean telling whether the particle hit the wall or not.
    """
    if(position_list[-1]<-wall or position_list[-1]>wall):
        return True
    return False

def output_file(velocity_list, position_list, time_list, file):
    """
    Output results from calculation to the given path. 

    Args:
        velocity_list: a list contains the velocity at each time step.
        position_list: a list contains the position at each time step.
        time_list: a list contains each time step.
        file: a file writer, either StringIO or opened file in 'w' mode.
    """
    for i, t in enumerate(time_list):
        file.write('{0} {1:.2f} {2:.6f} {3:.6f}\n'\
        .format(i, t, position_list[i], velocity_list[i]))


def plot_figures(wall_hitted, path, time_list, position_list):
    """
    Output the plot of the whole simulation.

    Args:
        wall_hitted: a numpy array that keeps track of how many times the 
        particle hits the wall in 100 runs at what time step.
        path: the path to save figures.
        time_list: a list contains each time step.
        position_list: a list contains the postion at each time step.
    
    Returns:
        hist_path: the path saved for the histogram.
        traj_path: the path saved for the trajectory.
    """
    plt.figure(0)   
    plt.hist(wall_hitted)
    plt.xlabel('Time (s)')
    plt.ylabel('# of time hit wall')
    hist_path = os.path.join(path, 'histogram.png')
    plt.savefig(hist_path)

    plt.figure(1)
    plt.plot(time_list, position_list, '.')
    plt.xlabel('Time (s)')
    plt.ylabel('position')
    plt.ylim([-6, 6])
    plt.axhline(5, color='r')
    plt.axhline(-5, color='r')
    traj_path = os.path.join(path, 'trajectory.png')
    plt.savefig(traj_path)
    return hist_path, traj_path


def main(args):
    velocity_list, position_list, time_list = \
    euler_integrator(args['damping_coefficient'], \
    args['initial_velocity'], \
    args['total_time'], \
    args['time_step'], \
    args['temperature'], \
    args['initial_position'], \
    args['wall_size'])

    print('The final position: ', position_list[-1])
    print('The final velocity: ', velocity_list[-1])
    
    print("Making a histogram by running 100 times the same simulation...")

    wall_hitted = np.zeros(100)
    for i in range(100):
        v_list, p_list, t_list = \
        euler_integrator(0.1, 0, 1000, 0.1, 300, 0, 5)
        wall_hitted[i] = t_list[-1]
    plot_figures(wall_hitted, args['path'], time_list, position_list)
    print('histogram.png and trajectory.png saved')
    return velocity_list, position_list, time_list

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    velocity_list, position_list, time_list = main(args)
    with open(os.path.join(args['path'], 'output'), 'w') as file:
        output_file(velocity_list, position_list, time_list, file)
