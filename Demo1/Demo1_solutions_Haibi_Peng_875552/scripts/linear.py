#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import dumpNodeConnections, irange
from mininet.node import RemoteController, OVSSwitch

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


def run():
    topo = LinearTopo(k=10)

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