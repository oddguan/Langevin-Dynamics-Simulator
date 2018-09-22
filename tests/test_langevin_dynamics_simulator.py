#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `lds` package."""

import unittest

import lds


class Test_Langevin_Dynamics_Simulator(unittest.TestCase):
    def setUp(self):
        self.simulator = lds.langevin_dynamics_simulator()
    
    def tearDown(self):
        pass
    
    def test_parse_args(self):
        parse = self.simulator.parse_args(
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
        self.assertEqual(parse['x0'], 5)
        self.assertEqual(parse['v0'], 10)
        self.assertEqual(parse['temp'], 50)
        self.assertEqual(parse['dc'], 10e-5)
        self.assertEqual(parse['ts'], 0.1)
        self.assertEqual(parse['tt'], 20)



