"""SUMO co-simulation."""

import logging
import os
import sys
import threading
import time
from math import hypot

if 'SUMO_HOME' is os.environ:
    SUMO_HOME = os.environ['SUMO_HOME']
    sys.path.append(os.path.join(SUMO_HOME, 'tools'))
    os.environ['PATH'] += os.pathsep + os.path.join(SUMO_HOME, 'bin')

import traci

from .mobility_input import MobilityInput

logger = logging.getLogger(__name__)

class SUMOMobilityInput(MobilityInput):
    """SUMOMobilityInput is an interface to the SUMO simulation environment.

    This mobility input supports two modes:

    * | **Remote Mode**: In this mode the testbed connects to an external already running SUMO instance.
      | You configure the host and port where the SUMO server is running via the ``sumo_host`` and ``sumo_port`` argument.
    * | **Embedded Mode**: In this mode the testbed starts an embedded version of SUMO.
      | You configure the simulation via the ``config_path`` argument.
        If SUMO is not installed globally you need to set the ``SUMO_HOME`` environment variable.

    Parameters
    ----------
    name : str
        The name of the MobilityInput.
    steps : int
        The number of steps to run the SUMO simulation.
    sumo_host : str
        The host on which the SUMO simulation is running.
    sumo_port : int
        The TraCI port.
    config_path : str
         The path to the simulation configuration (.cfg).
    """

    def __init__(self, name="SUMO External Simulation", steps=1000,
                 sumo_host='localhost', sumo_port=8813, config_path=None):
        super().__init__(name)
        #: The host on which the SUMO simulation is running.
        #:
        #: When running on a devcontainer, this is probably ``localhost``.
        self.sumo_host = sumo_host
        #: The TraCI port.
        #:
        #: Can be specified on the server with the ``--remote-port`` option.
        self.sumo_port = sumo_port
        #: The path to the simulation scenario configuration.
        self.config_path = config_path
        #: The number of steps to simulate.
        self.steps = steps
        #: The number of steps to simulate in SUMO.
        self.step_counter = 0

    def prepare(self, simulation):
        """Connect to SUMO server."""
        logger.info('Starting SUMO for simulation "%s".', self.name)
        if self.config_path is None:
            traci.init(host=self.sumo_host, port=self.sumo_port)
        else:
            traci.start(['sumo', '-c', self.config_path])
        self.step_counter = 0

    def start(self):
        """Start a thread stepping through the sumo simulation."""
        logger.info('Starting SUMO stepping for %s.', self.name)
        def run_sumo():
            try:
                while self.step_counter < self.steps:
                    traci.simulationStep()

                    # Update positions:
                    for node in self.node_mapping:
                        x, y = self.__get_position_of_node(node)
                        node.set_position(x, y, 0)

                    self.step_counter = self.step_counter + 1
                    time.sleep(traci.simulation.getDeltaT())
            except traci.exceptions.FatalTraCIError:
                logger.warning('Something went wrong with SUMO for %s. Maybe the connection was closed.', self.name)

        thread = threading.Thread(target=run_sumo)
        thread.start()

    def add_node_to_mapping(self, node, sumo_vehicle_id, obj_type="vehicle"):
        self.node_mapping[node] = (sumo_vehicle_id, obj_type)

    def __get_position_of_node(self, node):
        if node not in self.node_mapping:
            print("Unknown node "+str(node.name))
        else:
            if self.node_mapping[node][1] == "person":
                return traci.person.getPosition(self.node_mapping[node][0])
            elif self.node_mapping[node][1] == "vehicle":
                return traci.vehicle.getPosition(self.node_mapping[node][0])
            elif self.node_mapping[node][1] == "junction":
                return traci.junction.getPosition(self.node_mapping[node][0])
            else:
                print("Unknown type " + str(self.node_mapping[node][1]))

    def destroy(self):
        """Stop SUMO."""
        logger.info('Trying to close SUMO for %s.', self.name)
        # Trigger abort of loop.
        self.step_counter = self.steps
        traci.close()
