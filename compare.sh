#!/bin/bash

###Directories
#public_dir='/home/user/OC_Analysis/public/yang'
public_dir='/home/user/openconfig/public/'
juniper_dir='/home/user/OC_Analysis/juniper/yang'
relevant_models='/home/user/OC_Analysis/relevant_models'
git_dir='/home/user/openconfig/public/'

###Colors
RED='\033[0;31m'
REEN='\033[0;32m'
YELLOW='\033[1;33m'
RESET='\033[0m'

###Read in only relevant models
declare -a relevant_models_array=(
"openconfig-aaa.yang"
"openconfig-acl.yang"
"openconfig-aft-common.yang"
"openconfig-aft-ethernet.yang"
"openconfig-aft-ipv4.yang"
"openconfig-aft-ipv6.yang"
"openconfig-aft-mpls.yang"
"openconfig-aft-network-instance.yang"
"openconfig-aft-pf.yang"
"openconfig-aft-types.yang"
"openconfig-aft.yang"
"openconfig-alarms.yang"
"openconfig-alarm-types.yang"
"openconfig-bgp-common-multiprotocol.yang"
"openconfig-bgp-common-structure.yang"
"openconfig-bgp-common.yang"
"openconfig-bgp-errors.yang"
"openconfig-bgp-global.yang"
"openconfig-bgp-neighbor.yang"
"openconfig-bgp-peer-group.yang"
"openconfig-bgp-policy.yang"
"openconfig-bgp-types.yang"
"openconfig-bgp.yang"
"openconfig-evpn-types.yang"
"openconfig-evpn.yang"
"openconfig-fw-high-availability.yang"
"openconfig-fw-link-monitoring.yang"
"openconfig-if-8021x.yang"
"openconfig-if-aggregate.yang"
"openconfig-if-ethernet-ext.yang"
"openconfig-if-ethernet.yang"
"openconfig-if-ip.yang"
"openconfig-if-poe.yang"
"openconfig-if-sdn-ext.yang"
"openconfig-if-tunnel.yang"
"openconfig-if-types.yang"
"openconfig-inet-types.yang"
"openconfig-interfaces.yang"
"openconfig-isis-lsdb-types.yang"
"openconfig-isis-lsp.yang"
"openconfig-isis-policy.yang"
"openconfig-isis-routing.yang"
"openconfig-isis-types.yang"
"openconfig-isis.yang"
"openconfig-lacp.yang"
"openconfig-license.yang"
"openconfig-lldp-types.yang"
"openconfig-lldp.yang"
"openconfig-local-routing.yang"
"openconfig-messages.yang"
"openconfig-network-instance-l2.yang"
"openconfig-network-instance-l3.yang"
"openconfig-network-instance-policy.yang"
"openconfig-network-instance-types.yang"
"openconfig-network-instance.yang"
"openconfig-p4rt.yang"
"openconfig-packet-match-types.yang"
"openconfig-packet-match.yang"
"openconfig-pf-forwarding-policies.yang"
"openconfig-pf-interfaces.yang"
"openconfig-pf-path-groups.yang"
"openconfig-pf-srte.yang"
"openconfig-platform-cpu.yang"
"openconfig-platform-ext.yang"
"openconfig-platform-fan.yang"
"openconfig-platform-integrated-circuit.yang"
"openconfig-platform-linecard.yang"
"openconfig-platform-pipeline-counters.yang"
"openconfig-platform-port.yang"
"openconfig-platform-psu.yang"
"openconfig-platform-software.yang"
"openconfig-platform-transceiver.yang"
"openconfig-platform-types.yang"
"openconfig-platform.yang"
"openconfig-policy-forwarding.yang"
"openconfig-policy-types.yang"
"openconfig-procmon.yang"
"openconfig-qos-elements.yang"
"openconfig-qos-interfaces.yang"
"openconfig-qos-types.yang"
"openconfig-qos.yang"
"openconfig-rib-bgp-attributes.yang"
"openconfig-rib-bgp-ext.yang"
"openconfig-rib-bgp-shared-attributes.yang"
"openconfig-rib-bgp-table-attributes.yang"
"openconfig-rib-bgp-tables.yang"
"openconfig-rib-bgp-types.yang"
"openconfig-rib-bgp.yang"
"openconfig-routing-policy.yang"
"openconfig-sampling-sflow.yang"
"openconfig-system-grpc.yang"
"openconfig-system-logging.yang"
"openconfig-system-terminal.yang"
"openconfig-system.yang"
"openconfig-types.yang"
"openconfig-yang-types.yang"
)
###Grab all commit ids for openconfig
commit_ids=$(git --git-dir $public_dir.git --no-pager log | egrep '^commit' | sed 's/commit //g')
#latest_commit='2208d7ea0cd5e27dbc0bd13b32035e58af31b161'
latest_commit=`git --git-dir ~/openconfig/public/.git log -1 | grep commit | awk '{ print $2 }'`
echo "filename,present_in_junos,pristine_copy,common_commit,public_version,juniper_version"
for filename in $(find $public_dir -name '*.yang'); do 
		public_file=`basename $filename`
		public_file_version=$(cat $filename | grep openconfig-version | awk '{ print $2 }' | sed 's/;//g')
		repo_file=$(echo $filename | sed 's/\/home\/user\/openconfig\/public//g' | sed 's/^.//')
		public_file_hash=`sha1sum $filename | awk '{ print $1 }'`
		found=0
		if [[ " ${relevant_models_array[*]} " =~ " ${public_file} " ]]; then
			for juniper_filename in "$juniper_dir"/*; do
				basefile=`basename $juniper_filename`
				if [[ "$basefile" == "$public_file" ]]; then
					juniper_file=$basefile
					juniper_file_version=$(cat $juniper_filename | grep openconfig-version | awk '{ print $2 }' | sed 's/;//g')
					juniper_file_hash=`sha1sum $juniper_filename | awk '{ print $1 }'`
					if [[ "$public_file_hash" != "$juniper_file_hash" ]]; then
						filesize=$(wc -c $juniper_filename | awk '{ print $1 }')
						juniper_file_git_hash=`(printf "blob %d\0" $filesize; cat $juniper_filename) | sha1sum | awk '{ print $1 }'`
						for commit in $commit_ids; do
							git --git-dir $public_dir.git show "$commit":"$repo_file" > /dev/null 2>&1
							if [ $? -eq 0 ]; then
								prev_hash=$(git --git-dir $public_dir.git rev-parse -q "$commit":"$repo_file")
								if [[ "$juniper_file_git_hash" == "$prev_hash" ]]; then
									echo -e ${YELLOW} $public_file",true,true,"$commit","$public_file_version","$juniper_file_version ${RESET}
									found=1
									break 2 
								fi
							fi
						done
						echo -e ${RED} $public_file",true,false,null,"$public_file_version","$juniper_file_version${RESET}
						found=1
					else
						echo -e ${GREEN} $public_file",true,true,"$latest_commit","$public_file_version","$juniper_file_version ${RESET}
						found=1
					fi
				fi
			done
			if [ $found -eq 0 ]; then
				echo -e ${RED} $public_file",false,null,null,"$public_file_version",null"${RESET}
			fi
		fi
done
