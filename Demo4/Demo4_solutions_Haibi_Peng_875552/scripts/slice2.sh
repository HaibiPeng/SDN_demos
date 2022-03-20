#!/usr/bin/env bash

# add flow entries in bundle
for (( i=1; i<=5; i++))
do
    sudo ovs-ofctl --protocols=OpenFlow13 --bundle add-flows br-$i bundle.txt 
done

# check flow entries of e.g., br-1
sudo ovs-ofctl --protocols=OpenFlow13 dump-flows br-1
# ping failed
sudo ip netns exec ns-1 ping -c 1 10.0.0.2
# ping successful
sudo ip netns exec ns-1 ping -c 1 10.0.0.3
