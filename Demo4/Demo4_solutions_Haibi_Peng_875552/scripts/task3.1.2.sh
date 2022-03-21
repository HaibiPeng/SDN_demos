#!/usr/bin/env bash

# block all kinds of packets
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 ip,nw_dst=10.0.0.2,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 ipv6,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 icmp,nw_dst=10.0.0.2,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 icmp6,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 tcp,nw_dst=10.0.0.2,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 tcp6,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 udp,nw_dst=10.0.0.2,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 udp6,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 sctp,nw_dst=10.0.0.2,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 sctp6,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 arp,nw_dst=10.0.0.2,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 rarp,nw_dst=10.0.0.2,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 mpls,action=drop
sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 mplsm,action=drop

# check flow entry
sudo ovs-ofctl --protocols=OpenFlow13 dump-flows br-1

# test, e.g., icmp packets
sudo ip netns exec green ping -c 1 10.0.0.2
sudo ip netns exec blue ping -c 1 10.0.0.2

sudo ip netns exec green curl -m 10 10.0.0.2
sudo ip netns exec blue curl -m 10 10.0.0.2