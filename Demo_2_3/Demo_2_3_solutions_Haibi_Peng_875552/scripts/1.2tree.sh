#!/usr/bin/env bash

declare -i ns_num=1
declare -i bridge_num=1

function create_ns() {
    echo "Creating the namespace $1" >&2
    ip netns add $1
}


function create_ovs_bridge() {
    echo "Creating the OVS bridge $1" >&2
    ovs-vsctl add-br $1
    ovs-vsctl set bridge $1 protocol=OpenFlow13
}


function attach_ns_to_ovs() {
    echo "Attaching the namespace $1 to the OVS $2" >&2
    ip link add $3 type veth peer name $4
    ip link set $3 netns $1
    ovs-vsctl add-port $2 $4 -- set Interface $4 ofport_request=$5
    ip netns exec $1 ip addr add $6/24 dev $3
    ip netns exec $1 ip link set dev $3 up
    ip link set $4 up
}


function attach_ovs_to_ovs() {
    echo "Attaching the OVS $1 to the OVS $2" >&2
    ip link add name $3 type veth peer name $4
    ip link set $3 up
    ip link set $4 up
    ovs-vsctl add-port $1 $3 -- set Interface $3 ofport_request=$5
    ovs-vsctl add-port $2 $4 -- set Interface $4 ofport_request=$5
}


function attach_ovs_to_sdn() {
    echo "Attaching the OVS bridge to the ONOS controller" >&2
    ovs-vsctl set-controller $1 tcp:$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -q  --filter ancestor=onosproject/onos)):6653
}


# I tried to use recursive methods but failed because recursion happens in subshell 
# so other global variables won't be changed when back from the recursion.
# declare -i ns_num=1
# declare -i bridge_num=1
# 
# function add_tree() {
#     if (( $1 > 0 ))
#     then
#         node=$(create_ovs_bridge "br-$bridge_num")
#         echo "node: $node" >&2
#         attach_ovs_to_sdn $node
#         bridge_num=$((bridge_num+1))
#         for (( i=0; i<$2; i++ ))
#         do
#             child=$(add_tree $(($1-1)) $2)
#             echo "child: $child" >&2
#             if (( $1 == 1 ))
#             then
#                 ns_num=$((ns_num+1))
#                 attach_ns_to_ovs $child $node "veth-$child" "veth-$child-br" 2 "10.0.0.$ns_num"
#             else
#                 bridge_num=$((bridge_num+1))
#                 attach_ovs_to_ovs $child $node "ovs-$child-$node" "ovs-$node-$child" 1
#             fi
#         done
#     else
#         echo $ns_num >&2
#         node=$(create_ns "ns-$ns_num")
#         ns_num=$((ns_num+1))
#     fi
#     echo $node
# }


# add tree topology
function add_tree() {
    last_layer_switch_num=$((2**(($1-1))))
    ns_num=$(($last_layer_switch_num*$2))
    switch_num=$((2**$1-1))
    
    # create switches
    for (( i=1; i<=$switch_num; i++ ))
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
        if (( $i % 2 == 0 )); then
            switch_with_ns=$(($switch_with_ns+1))
        fi
    done

    # attach ovs to ovs    
    switch_without_ns=$(($last_layer_switch_num-1))
    for (( i=1; i<=$switch_without_ns; i++ ))
    do
        # attach ovs to ovs
        attach_ovs_to_ovs "br-$i" "br-$(($i*2))" br-ovs$i-$(($i*2)) br-ovs$(($i*2))-$i 1
        attach_ovs_to_ovs "br-$i" "br-$(($i*2+1))" br-ovs$i-$(($i*2+1)) br-ovs$(($i*2+1))-$i 1
    done

    ip netns exec ns-1 ping -c 1 10.0.0.2
    ip netns exec ns-2 ping -c 1 10.0.0.3
    ip netns exec ns-3 ping -c 1 10.0.0.4
    ip netns exec ns-4 ping -c 1 10.0.0.5
    ip netns exec ns-5 ping -c 1 10.0.0.6
    ip netns exec ns-6 ping -c 1 10.0.0.7
    ip netns exec ns-7 ping -c 1 10.0.0.8
    ip netns exec ns-8 ping -c 1 10.0.0.1
}

add_tree 3 2

