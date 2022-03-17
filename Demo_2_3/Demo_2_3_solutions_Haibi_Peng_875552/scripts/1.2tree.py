# re-write recursion version of creating tree topology but not tested

import os
import docker

def create_ovs(ovs_name):
    print("Creating the OVS bridge {}".format(ovs_name))
    basic_cmd = 'sudo ovs-vsctl add-br {}'.format(ovs_name)
    protocol_cmd = 'sudo ovs-vsctl set bridge {} protocol=OpenFlow13'.format(ovs_name)
    os.system(basic_cmd)
    os.system(protocol_cmd)


def add_ns(ns_name):
    print("Creating the namespace {}".format(ns_name))
    basic_cmd = 'ip netns add {}'.format(ns_name)
    os.system(basic_cmd)


def attach_ns_to_ovs(ns_name, ovs_name, ns_ovs_interface, ovs_ns_interface, ovs_port, ip_addr):
    print("Attaching the namespace {} to the OVS {}".format(ns_name, ovs_name))
    basic_cmd = 'ip link add name {} type veth peer name {}'.format(ns_ovs_interface, ovs_ns_interface)
    os.system(basic_cmd)

    basic_cmd = "ip link set {} netns {}".format(ns_ovs_interface, ns_name)
    os.system(basic_cmd)

    basic_cmd = "sudo ovs-vsctl add-port {0} {1} -- set Interface {1} ofport_request={2}"\
        .format(ovs_name, ovs_ns_interface, ovs_port)
    os.system(basic_cmd)

    basic_cmd = "ip netns exec {0} ip addr add {1}/24 dev {2}".format(ns_name, ip_addr, ns_ovs_interface)
    os.system(basic_cmd)

    basic_cmd = "ip netns exec {} ip link set dev {} up".format(ns_name, ns_ovs_interface)
    os.system(basic_cmd)

    basic_cmd = "ip link set {} up".format(ovs_ns_interface)
    os.system(basic_cmd)


def attach_ovs_to_ovs(ovs_name_1, ovs_name_2, ovs_interface_1, ovs_interface_2, ovs_port):
    print("Attaching the OVS {} to the OVS {}".format(ovs_name_1, ovs_name_2))

    basic_cmd = 'sudo ip link add name {} type veth peer name {}'.format(ovs_interface_1, ovs_interface_2)
    os.system(basic_cmd)

    basic_cmd = "ip link set {} up".format(ovs_interface_1)
    os.system(basic_cmd)

    basic_cmd = "ip link set {} up".format(ovs_interface_2)
    os.system(basic_cmd)

    basic_cmd = "sudo ovs-vsctl add-port {0} {1} -- set Interface {1} ofport_request={2}"\
        .format(ovs_name_1, ovs_interface_1, ovs_port)
    os.system(basic_cmd)

    basic_cmd = "sudo ovs-vsctl add-port {0} {1} -- set Interface {1} ofport_request={2}"\
        .format(ovs_name_2, ovs_interface_2, ovs_port)
    os.system(basic_cmd)


def attach_ovs_to_sdn(ovs_name):
    print("Attaching the OVS bridge to the ONOS controller")
    client = docker.DockerClient()
    container = client.containers.get("onos")
    ip_add = container.attrs['NetworkSettings']['IPAddress']
    basic_cmd = "ovs-vsctl set-controller {} tcp:{}:6653".format(ovs_name, ip_add)
    os.system(basic_cmd)


class TreeTopo:
    "Topology for a tree network with a given depth and fanout."
    def __init__(self, depth=1, fanout=2):
        # Numbering:  h1..N, s1..M
        self.hostNum = 1
        self.switchNum = 1
        # Build topology
        self.addTree(depth, fanout)

    def addTree(self, depth, fanout):
        """Add a subtree starting with node n.
           returns: last node added"""
        isSwitch = depth > 0
        if isSwitch:
            # node = self.addSwitch('s%s' % self.switchNum, protocols='OpenFlow13')
            node = "br-{}".format(self.switchNum)
            create_ovs(node)
            attach_ovs_to_sdn(node)
            self.switchNum += 1
            for _ in range(fanout):
                child = self.addTree(depth - 1, fanout)
                # self.addLink(node, child)
                # check if child is switch or host
                if child[0] == 'b':
                    # child is switch
                    attach_ovs_to_ovs(child, node, "ovs-{}-{}".format(child, node), "ovs-{}-{}".format(node, child), 1)
                else:
                    # child is host
                    attach_ns_to_ovs(child, node, "veth-{}".format(child), "veth-{}-br".format(child), 2, "10.0.0.{}".format(self.hostNum))
        else:
            # node = self.addHost('h%s' % self.hostNum)
            node = "ns-{}".format(self.hostNum)
            add_ns(node)
            self.hostNum += 1
        return node

if __name__ == '__main__':
    tree = TreeTopo(depth=3, fanout=3)