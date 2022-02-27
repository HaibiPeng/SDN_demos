#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import dumpNodeConnections, irange
from mininet.node import RemoteController, OVSSwitch

# Reference: https://github.com/mininet/mininet/blob/master/mininet/topolib.py#L9
# Add switch protocols as 'OpenFlow13' in the code
class TreeTopo( Topo ):
    "Topology for a tree network with a given depth and fanout."
    def build(self, depth=1, fanout=2):
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
            node = self.addSwitch('s%s' % self.switchNum, protocols='OpenFlow13')
            self.switchNum += 1
            for _ in range(fanout):
                child = self.addTree(depth - 1, fanout)
                self.addLink(node, child)
        else:
            node = self.addHost('h%s' % self.hostNum)
            self.hostNum += 1
        return node


def run():
    topo = TreeTopo(depth=3, fanout=2)

    # Define remote SDN controller, which has been setup using docker
    c1 = RemoteController('c1', ip='172.17.0.2', port=6653)

    net = Mininet(topo=topo, controller=c1, switch=OVSSwitch)

    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()