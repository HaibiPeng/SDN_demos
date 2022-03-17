#!/usr/bin/env bash

function create_ns() {
    echo "Creating the namespace $1"
    ip netns add $1
}


function create_ovs_bridge() {
    echo "Creating the OVS bridge $1"
    ovs-vsctl add-br $1
    ovs-vsctl set bridge $1 protocol=OpenFlow13
}


function attach_ns_to_ovs() {
    echo "Attaching the namespace $1 to the OVS $2"
    ip link add $3 type veth peer name $4
    ip link set $3 netns $1
    ovs-vsctl add-port $2 $4 -- set Interface $4 ofport_request=$5
    ip netns exec $1 ip addr add $6/24 dev $3
    ip netns exec $1 ip link set dev $3 up
    ip link set $4 up
}


function attach_ovs_to_ovs() {
    echo "Attaching the OVS $1 to the OVS $2"
    ip link add name $3 type veth peer name $4
    ip link set $3 up
    ip link set $4 up
    ovs-vsctl add-port $1 $3 -- set Interface $3 ofport_request=$5
    ovs-vsctl add-port $2 $4 -- set Interface $4 ofport_request=$5
}


function attach_ovs_to_sdn() {
    echo "Attaching the OVS bridge to the ONOS controller"
    ovs-vsctl set-controller $1 tcp:$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -q  --filter ancestor=onosproject/onos)):6653
}


# add linear topology
function add_linear() {
    switch_num=$1
    ns_num=$2
    # create switches
    for (( i=1; i<=$switch_num; i++ ))
    do
        create_ovs_bridge "br-$i"
        # attach ovs to sdn
        attach_ovs_to_sdn br-$i
    done

    # create ns
    for (( i=1; i<=$ns_num; i++ ))
    do
        create_ns "ns-$i"
        # attach ns to ovs
        attach_ns_to_ovs "ns-$i" "br-$i" "veth-ns-$i" "veth-ns-$i-br" 2 "10.0.0.$i"
    done

    # attach ovs to ovs    
    for (( i=1; i<$switch_num; i++ ))
    do
        # attach ovs to ovs
        attach_ovs_to_ovs "br-$i" "br-$(($i+1))" br-ovs$i-$(($i+1)) br-ovs$(($i+1))-$i 1
    done

    ip netns exec ns-1 ping -c 1 10.0.0.2
    ip netns exec ns-2 ping -c 1 10.0.0.3
    ip netns exec ns-3 ping -c 1 10.0.0.4
    ip netns exec ns-4 ping -c 1 10.0.0.5
    ip netns exec ns-5 ping -c 1 10.0.0.2
}


# add tree topology
function add_tree() {
    depth=$1
    fanout=$2
    last_layer_switch_num=$(($fanout**(($depth-1))))
    ns_num=$(($last_layer_switch_num*$fanout))
    total_switch_num=0
    for (( i=0; i<$depth; i++ ))
    do
        total_switch_num=$(($total_switch_num+$fanout**$i))
    done
    
    # create switches
    for (( i=1; i<=$total_switch_num; i++ ))
    do
        create_ovs_bridge "br-$i"
        # attach ovs to sdn
        attach_ovs_to_sdn br-$i
    done

    # create ns
    switch_with_ns=$last_layer_switch_num
    for (( i=1; i<=$ns_num; i++ ))
    do
        create_ns "ns-$i"
        # attach ns to ovs
        attach_ns_to_ovs "ns-$i" "br-$switch_with_ns" "veth-ns-$i" "veth-ns-$i-br" 2 "10.0.0.$i"
        if (( $i % $fanout == 0 )); then
            switch_with_ns=$(($switch_with_ns+1))
        fi
    done

    # attach ovs to ovs    
    switch_without_ns=$(($total_switch_num-$last_layer_switch_num))
    for (( i=1; i<=$switch_without_ns; i++ ))
    do
        # attach ovs to ovs
        for (( j=$((($i-1)*$fanout+2)); j<=$(($i*$fanout+1)); j++ ))
        do
            attach_ovs_to_ovs "br-$i" "br-$j" "br-ovs$i-$j" "br-ovs$j-$i" 1
        done
    done

    ip netns exec ns-1 ping -c 1 10.0.0.3
    ip netns exec ns-2 ping -c 1 10.0.0.4
    ip netns exec ns-3 ping -c 1 10.0.0.5
    ip netns exec ns-4 ping -c 1 10.0.0.6
    ip netns exec ns-5 ping -c 1 10.0.0.2
}


echo "topo: $1"
echo "switchs: $2"
echo "hosts: $3"

if [ $1 == "linear" ]
then
    add_linear $2 $3
elif [ $1 == "tree" ]
then
    add_tree $2 $3
else
    echo "wrong topo name"
fi
