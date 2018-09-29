#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `lds` package."""

import unittest
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
                '-ws', '5'
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
    
    def test_random_force(self):
        # checking if it always generate 0, if both mu and 
        # std_dev are 0
        for i in range(100):
            random_force = simulator.random_force(0, 0)
            self.assertEqual(0.0, random_force)
        
        # checking if 1000 generations follows a normal 
        # distribution by Shapiro-Wilk test
        force_list = np.zeros(3000)
        for i in range(3000):
            random_force = simulator.random_force(100, 1)
            force_list[i] = random_force
        self.assertGreater(ss.shapiro(force_list)[1], 0.05)

    def test_hit_wall(self):
        position_list1 = [0, 1, 2, 3, 4, 5, 6]
        position_list2 = [0, 2, 4, -5, -7]
        position_list3 = [2, 3, 4, 1]
        wall = 5
        self.assertTrue(simulator.hit_wall(position_list1, wall))
        self.assertTrue(simulator.hit_wall(position_list2, wall))
        self.assertFalse(simulator.hit_wall(position_list3, wall))



