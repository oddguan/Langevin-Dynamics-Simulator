#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `lds` package."""

import unittest
try:
    # python 3.4+ should use builtin unittest.mock not mock package
    import unittest.mock as mock
except ImportError:
    import mock

import sys
from io import StringIO
import numpy as np
import scipy.stats as ss

import lds.langevin_dynamics_simulator as simulator


class Test_Langevin_Dynamics_Simulator(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_parse_args(self):
        parse = simulator.parse_args(
            [
                '-x0', '5', \
                '-v0', '10', \
                '-temp', '50', \
                '-dc', '10e-5', \
                '-ts', '0.1', \
                '-tt', '20' , \
                '-ws', '5', \
                '-p', '.'
            ]
        )

        self.assertIsInstance(parse, dict)
        self.assertEqual(parse['initial_position'], 5)
        self.assertEqual(parse['initial_velocity'], 10)
        self.assertEqual(parse['temperature'], 50)
        self.assertEqual(parse['damping_coefficient'], 10e-5)
        self.assertEqual(parse['time_step'], 0.1)
        self.assertEqual(parse['total_time'], 20)
        self.assertEqual(parse['wall_size'], 5)
        self.assertEqual(parse['path'], '.')
    
    def test_random_force(self):
        # checking if it always generate 0, if both mu and 
        # std_dev are 0
        for i in range(100):
            random_force = simulator.random_force(0, 0)
            self.assertEqual(0.0, random_force)
        
        # checking if 1000 generations follows a normal 
        # distribution by Shapiro-Wilk test
        force_list = np.zeros(5000)
        for i in range(5000):
            random_force = simulator.random_force(100, 1)
            force_list[i] = random_force
        self.assertGreater(ss.shapiro(force_list)[1], 0.05)
    
    def test_euler_integrator(self):
        # checking when damping coefficient is 0
        v, p, t = simulator.euler_integrator(0, 1e-4, 10, 1, 20, 0, 5)
        # when damp_coeff is 0, v should not change based on time
        for element in v:
            self.assertEqual(1e-4, element)
        
        # checking time steps calculation
        # if total time cannot be divided by the time step,
        # time will stop before it reaches the ideal time 
        v, p, t = simulator.euler_integrator(0, 1e-4, 11, 0.3, 20, 0, 5)
        self.assertLess(t[-1], 11)

        # position is not tested since random force distribution
        # has been tested, and position shouldn't be a problem

    def test_hit_wall(self):
        position_list1 = [0, 1, 2, 3, 4, 5, 6]
        position_list2 = [0, 2, 4, -5, -7]
        position_list3 = [2, 3, 4, 1]
        wall = 5
        self.assertTrue(simulator.hit_wall(position_list1, wall))
        self.assertTrue(simulator.hit_wall(position_list2, wall))
        self.assertFalse(simulator.hit_wall(position_list3, wall))

    def test_output_file(self):
        outfile = StringIO()
        simulator.output_file([7,8,9], [4,5,6], [1,2,3], outfile)
        outfile.seek(0)
        content = outfile.read()
        output_list = content.split('\n')
        for i, line in enumerate(output_list):
            if i==0:
                self.assertEqual(line, '{0} {1:.2f} {2:.6f} {3:.6f}'.format(i, 1, 4, 7))
            elif i==1:
                self.assertEqual(line, '{0} {1:.2f} {2:.6f} {3:.6f}'.format(i, 2, 5, 8))
            elif i==2:
                self.assertEqual(line, '{0} {1:.2f} {2:.6f} {3:.6f}'.format(i, 3, 6, 9))

    def test_plot_figures(self):
        wall_hitted = np.zeros(100)
        path = '.'
        time_list = np.zeros(200)
        position_list = np.zeros(200)
        hist_path, traj_path = simulator.plot_figures(wall_hitted, path, time_list, position_list)
        self.assertEqual(hist_path.split('/')[-1], 'histogram.png')
        self.assertEqual(traj_path.split('/')[-1], 'trajectory.png')

    def test_main(self):
        testargs = ['prog', '-x0', '0', '-v0', \
         '1e-4', '-temp', '30', '-dc', '10', '-ts', \
          '1', '-tt', '30', '-ws', '5']
        with mock.patch.object(sys, 'argv', testargs) as sys_args:
            args = simulator.parse_args(sys_args[1:])
            velocity_list, position_list, time_list = \
            simulator.main(args)
            self.assertIsInstance(velocity_list, list)
            self.assertIsInstance(position_list, list)
            self.assertIsInstance(time_list, list)
            self.assertEqual(velocity_list[0], 1e-4)
            self.assertEqual(position_list[0], 0)
            self.assertEqual(time_list[0], 0.0)



