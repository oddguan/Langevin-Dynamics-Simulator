===========================
Langevin Dynamics Simulator
===========================


.. image:: https://travis-ci.org/oddguan/Langevin-Dynamics-Simulator.svg?branch=master
        :target: https://travis-ci.org/oddguan/Langevin-Dynamics-Simulator

.. image:: https://readthedocs.org/projects/langevin-dynamics-simulator/badge/?version=latest
        :target: https://langevin-dynamics-simulator.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://coveralls.io/repos/github/oddguan/Langevin-Dynamics-Simulator/badge.svg?branch=master
        :target: https://coveralls.io/github/oddguan/Langevin-Dynamics-Simulator?branch=master


Overview
--------
This is a 1-D Langevin Dynamics Simulator implemented in Python. This simulator caculates the final position and velocity of a given 
particle, by providing the initial position and velocity, damping coefficient, total time and the time step of integration.

This simulator uses the Euler Integrator. 

* Free software: MIT license
* Documentation: https://langevin-dynamics-simulator.readthedocs.io.


Dependencies
--------
In order to run the simulator, you'll need the following denpendencies. 

* git
* python 3
* ``numpy``
* ``scipy``
* ``matplotlib``

I recommend install python and packages via `Anaconda <www.anaconda.com>`_.


Installation
--------
To install the simulator, use the following command:

``git clone https://github.com/oddguan/Langevin-Dynamics-Simulator``

``cd Langevin-Dynamics-Simulator``

``pip install lds``


Example Usage
---------
This simulator collects initial inputs via command prompt. One example of running a simulation would be:

``python lds/langevin_dynamics_simulator.py -x0 0 -v0 0 -temp 50 -dc 10e-5 -ts 0.1 -tt 20 -ws 5 -p .``

You can dig into my source code to see all argument options available in this simulator. 

The final position and the final velocity of the particle will be printed via standard output, and a output file and 
two graphs will be generated: 

* output includes the index, time step, postion and velocity of the particle
* histogram.png: genereated via `matplotlib`, it will plot 100 runs by a given condition into a histogram. The number represents how many times the particle actually hit the wall within the total time. 
* trajectory.png: generated via `matplotlib` as well, and it will show the trjectory of the particle in a single run. 


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
