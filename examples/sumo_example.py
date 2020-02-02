#!/usr/bin/env python3

from testbed import ArgumentParser, Network, DockerNode, Scenario, WiFiChannel
from testbed.mobility_input import SUMOMobilityInput

def main():
    scenario = Scenario()

    net = Network("10.0.0.0", "255.255.255.0")

    switch = DockerNode('switch', docker_build_dir='./docker/sumo', command="java FileServer")
    train = DockerNode('train', docker_build_dir='./docker/sumo', command="java FileClient")
    net.connect(train, switch, channel_type=WiFiChannel, tx_power=30.0)

    scenario.add_network(net)

    sumo = SUMOMobilityInput(name='Rail-To-X', sumo_port=8081)
    sumo.add_node_to_mapping(switch, 'n0', obj_type='junction')
    sumo.add_node_to_mapping(train, 'train')

    scenario.add_mobility_input(sumo)

    with scenario as sim:
        # To simulate forever, just do not specifiy the simluation_time parameter.
        sim.simulate(simluation_time=30)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.run(main)
