#!/usr/bin/env bash

sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 priority=40000,icmp,nw_src=10.0.0.3,nw_dst=10.0.0.2,action=drop

# check flow entry
sudo ovs-ofctl --protocols=OpenFlow13 dump-flows br-1

# test, e.g., icmp packets
sudo ip netns exec blue ping -c 1 10.0.0.2