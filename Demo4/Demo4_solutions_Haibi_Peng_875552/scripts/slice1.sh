#!/usr/bin/env bash

# assign VLAN tags to network interfaces, resulting in traffic isolation between namespaces
ovs-vsctl set port veth-ns-1-br tag=1
ovs-vsctl set port veth-ns-3-br tag=1
ovs-vsctl set port veth-ns-5-br tag=1
ovs-vsctl set port veth-ns-7-br tag=1
ovs-vsctl set port veth-ns-9-br tag=1

ovs-vsctl set port veth-ns-2-br tag=2
ovs-vsctl set port veth-ns-4-br tag=2
ovs-vsctl set port veth-ns-6-br tag=2
ovs-vsctl set port veth-ns-8-br tag=2
ovs-vsctl set port veth-ns-10-br tag=2