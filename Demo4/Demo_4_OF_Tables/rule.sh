#!/usr/bin/env bash

# block all kinds of packets
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 ip,nw_dst=10.0.0.2,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 ipv6,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 arp,nw_dst=10.0.0.2,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 rarp,nw_dst=10.0.0.2,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 mpls,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 mplsm,action=drop

# only all http/https traffic(tcp, port 80 and 443)
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 tcp,tcp_src=80/443,tcp_dst=80/443,nw_dst=10.0.0.2,action=all