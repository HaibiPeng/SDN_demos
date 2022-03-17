#!/usr/bin/env bash

# delete all containers
declare lxc=($(sudo lxc-ls --fancy | awk '{if(NR>1){print $1}}'))
for (( i=0; i<${#lxc[@]}; i++ ))
do
    lxc-stop --name "${lxc[$i]}"
    lxc-destroy --name "${lxc[$i]}"
done


# delete all bridges
# get bridge numbers
br=$(sudo ovs-vsctl list-br | wc -l)

for (( i=1; i<=$br; i++ ))
do
    ovs-vsctl del-br "ovs-$i"
done

# delete all links
# get link lists
declare Ovslinks=($(sudo ip link show | grep Ovs | awk -F ': ' '{print $2}' | awk -F '@' '{print $1}'))

for (( i=0; i<${#Ovslinks[@]}; i++ ))
do
    ip link delete "${Ovslinks[$i]}"
done

declare lxclinks=($(sudo ip link show | grep lxc | awk -F ': ' '{print $2}'))

for (( i=0; i<${#lxclinks[@]}; i++ ))
do
    ip link delete "${lxclinks[$i]}"
done

declare intlinks=($(sudo ip link show | grep int | awk -F ': ' '{if(NR%2==1){print $2}}' | awk -F '@' '{print $1}'))

for (( i=0; i<${#intlinks[@]}; i++ ))
do
    ip link delete "${intlinks[$i]}"
done