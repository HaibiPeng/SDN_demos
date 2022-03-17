#!/usr/bin/env bash

# delete all namespaces
ip -all netns delete

# delete all bridges
# get bridge numbers
br=$(sudo ovs-vsctl list-br | wc -l)

for (( i=1; i<=$br; i++ ))
do
    ovs-vsctl del-br "br-$i"
done

# delete all links
# get link lists
declare links=($(sudo ip link show | grep br-ovs | awk -F ': ' '{if(NR%2==1){print $2}}' | awk -F '@' '{print $1}'))

for (( i=0; i<${#links[@]}; i++ ))
do
    ip link delete "${links[$i]}"
done

