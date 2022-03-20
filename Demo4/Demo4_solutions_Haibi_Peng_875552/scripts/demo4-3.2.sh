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
    ns_per_switch=$(($2/$1))
    # create switches
    for (( i=1; i<=$switch_num; i++ ))
    do
        create_ovs_bridge "br-$i"
        # attach ovs to sdn
        attach_ovs_to_sdn br-$i
    done

    # create ns
    switch=1
    for (( i=1; i<=$ns_num; i++ ))
    do
        create_ns "ns-$i"
        # attach ns to ovs
        attach_ns_to_ovs "ns-$i" "br-$switch" "veth-ns-$i" "veth-ns-$i-br" 2 "10.0.0.$i"
        if (( $i % $ns_per_switch == 0 )); then
            switch=$(($switch+1))
        fi
    done

    # attach ovs to ovs    
    for (( i=1; i<$switch_num; i++ ))
    do
        # attach ovs to ovs
        attach_ovs_to_ovs "br-$i" "br-$(($i+1))" br-ovs$i-$(($i+1)) br-ovs$(($i+1))-$i 1
    done

    for (( i=1; i<=$(($ns_num-1)); i++ ))
    do
        ip netns exec ns-$i ping -c 1 10.0.0.$ns_num
    done
}

add_linear 5 10