#!/usr/bin/env bash

for (( i=1; i<=5; i++))
do
    for (( j=1; j<=5; j++))
    do
        sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-$i priority=40000,icmp,nw_src=10.0.0.$((2*$i)),nw_dst=10.0.0.$((2*$j-1)),action=drop
        sudo ovs-ofctl --protocols=OpenFlow13 add-flow br-$i priority=40000,icmp,nw_src=10.0.0.$((2*$i-1)),nw_dst=10.0.0.$((2*$j)),action=drop
    done
done

# check flow entries of e.g., br-1
sudo ovs-ofctl --protocols=OpenFlow13 dump-flows br-1
# ping failed
sudo ip netns exec ns-1 ping -c 1 10.0.0.2
# ping successful
sudo ip netns exec ns-1 ping -c 1 10.0.0.3

