#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import dumpNodeConnections
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


def run():
    topo = SingleSwtichTopo(13)

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