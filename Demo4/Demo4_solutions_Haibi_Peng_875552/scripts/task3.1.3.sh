#!/usr/bin/env bash

sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-1 priority=40000,nw_dst=10.0.0.2,action=all

# check flow entry
sudo ovs-ofctl --protocols=OpenFlow13 dump-flows br-1

# test, e.g., icmp packets
sudo ip netns exec green ping -c 1 10.0.0.2
sudo ip netns exec blue ping -c 1 10.0.0.2

sudo ip netns exec green curl -m 10 10.0.0.2
sudo ip netns exec blue curl -m 10 10.0.0.2