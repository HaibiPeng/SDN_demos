#!/usr/bin/python

import sys
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import dumpNodeConnections, irange
from mininet.node import RemoteController, OVSSwitch

class SingleSwtichTopo(Topo):
    # Builds single-switch topology
    def build(self, k=2, **_opts):
        # Adding one legacy switch
        s1 = self.addSwitch('s1', protocols='OpenFlow13')
        
        # Adding hosts and connecting hosts to switches
        for h in range(k):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, s1)


# Reference: https://github.com/mininet/mininet/blob/master/mininet/topo.py#L329
# Add switch protocols as 'OpenFlow13' in the code
class LinearTopo( Topo ):
    "Linear topology of k switches, with n hosts per switch."
    def build( self, k=2, n=1, **_opts):
        """k: number of switches
           n: number of hosts per switch"""
        self.k = k
        self.n = n

        if n == 1:
            genHostName = lambda i, j: 'h%s' % i
        else:
            genHostName = lambda i, j: 'h%ss%d' % (j, i)

        lastSwitch = None
        for i in irange(1, k):
            # Add switch
            switch = self.addSwitch('s%s' % i, protocols='OpenFlow13')
            # Add hosts to switch
            for j in irange(1, n):
                host = self.addHost( genHostName(i, j))
                self.addLink( host, switch )
            # Connect switch to previous
            if lastSwitch:
                self.addLink(switch, lastSwitch)
            lastSwitch = switch


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
    args = sys.argv
    topoType = args[1]
    if topoType == 'single':
        if len(args) != 3:
            print('Wrong arguments! Please try again.')
        else:
            hostNumber = int(args[2])
            topo = SingleSwtichTopo(hostNumber)
    elif topoType == 'linear':
        if len(args) < 3 or len(args) > 4:
            print('Wrong arguments! Please try again.')
        else:
            switchNumber = int(args[2])
            if len(args) == 4:
                hostNumberPerSwitch = int(args[3])
                topo = LinearTopo(k=switchNumber, n=hostNumberPerSwitch)
            else:
                topo = LinearTopo(k=switchNumber)
    elif topoType == 'tree':
        if len(args) != 4:
            print('Wrong arguments! Please try again.')
        else:
            depth = int(args[2])
            fanout = int(args[3])
            topo = TreeTopo(depth=depth, fanout=fanout)

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