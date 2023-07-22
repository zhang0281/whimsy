#!/bin/bash

usage="Usage: $(basename $0) (e, enable|d, disable) to enable or disable ipv6. Re-open wlan to recover."

function disable_wlan0_ipv6() {
        su root -s /bin/sh -c 'echo "1" >/proc/sys/net/ipv6/conf/wlan0/accept_ra'
        su root -s /bin/sh -c 'echo "1" >/proc/sys/net/ipv6/conf/wlan0/disable_ipv6'
}
function enable_wlan0_ipv6() {

        su root -s /bin/sh -c 'echo "2" >/proc/sys/net/ipv6/conf/wlan0/accept_ra'
        su root -s /bin/sh -c 'echo "0" >/proc/sys/net/ipv6/conf/wlan0/disable_ipv6'
}

case $1 in
disable)
        disable_wlan0_ipv6
        ;;
d)
        disable_wlan0_ipv6
        ;;
enable)
        enable_wlan0_ipv6
        ;;
e)
        enable_wlan0_ipv6
        ;;
*)
        echo "参数错误!"
        echo "$usage"
        ;;
esac
