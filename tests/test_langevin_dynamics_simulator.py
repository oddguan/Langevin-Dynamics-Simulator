#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `lds` package."""

import unittest

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
                '-tt', '20' 
            ]
        )

        self.assertIsInstance(parse, dict)
        self.assertEqual(parse['initial_position'], 5)
        self.assertEqual(parse['initial_velocity'], 10)
        self.assertEqual(parse['temperature'], 50)
        self.assertEqual(parse['damp_coeff'], 10e-5)
        self.assertEqual(parse['time_step'], 0.1)
        self.assertEqual(parse['total_time'], 20)



