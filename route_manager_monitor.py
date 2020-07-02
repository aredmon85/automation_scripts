from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from pprint import pprint
from time import sleep
import datetime
import re
import argparse
import sys

###This script monitors the output of the PFE level command "show route manager statistics" for FIB changes


#EXAMPLE:
# python route_manager_monitor.py --user neteng --password password123 --device 192.168.1.101


tables = ('ipv4','ipv6','other')
metrics = ('prefix adds','prefix changes','prefix deletes','prefix add failures','prefix delete failures','prefix change failures')
stats_dict = {}

def parse_route_manager_stats(stats_dict,route_manager_output):
    ###parse the output of 'show route manager statistics' and load values into a dictionary
    key = ''
    for i in tables:
        stats_dict[i]['raw'] = []

    for line in route_manager_output.splitlines():
        if 'IPv4 Statistics:' in line:
            key = 'ipv4'
            stats_dict[key]['raw'].append(line)
            continue
        if 'IPv6 Statistics:' in line:
            key = 'ipv6'
            stats_dict[key]['raw'].append(line)
            continue
        if 'Statistics' in line:
            key = 'other'
            stats_dict[key]['raw'].append(line)
            continue
        if key == '':
            continue
        else:
            stats_dict[key]['raw'].append(line)

def load_stats_dict(stats_dict):
    ###sort and pair values of provided dict with appropiate keys
    stats_dict['total_mutations'] = 0
    for key in tables:
        for i in stats_dict[key]['raw']:
            for metric in metrics:
                delta_metric = 'delta_'+metric
                if metric in i:
                    val = i.lstrip().split(' ')[0]
                    stats_dict['total_mutations'] += int(val)
                    if stats_dict[key]['stats'].has_key(metric):
                        stats_dict[key]['stats'][delta_metric] = int(val) - int(stats_dict[key]['stats'][metric])
                    stats_dict[key]['stats'][metric] = val
                    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", help="target device to monitor")
    parser.add_argument("--user", help="username")
    parser.add_argument("--password", help="password")
    parser.add_argument("--interval", default=3, help="interval to run monitoring")
    
    args = parser.parse_args()
    if args.device and args.user and args.password and args.interval:
        print "###Running on device "+args.device+" as user "+args.user+" with an interval of "+str(args.interval)+" seconds###"
        
        iterations = 0
        interval = float(args.interval)
        for i in tables:
            stats_dict[i] = {}
            stats_dict[i]['raw'] = []
            stats_dict[i]['stats'] = {}

        with Device(host=args.device, port=22,username=args.user,password=args.password) as dev:
            dev_shell = StartShell(dev)
            dev_shell.open()
            last_mutation_count = 0   
            while(True):
                route_manager = dev_shell.run('cprod -A fpc0 -c "show route manager statistics"')
                stats = route_manager[1]
                if "Permission denied" in stats:
                    print "Permission to execute cprod command failed"
                    sys.exit(0)
                
                parse_route_manager_stats(stats_dict,stats)
                load_stats_dict(stats_dict)
                timestamp = datetime.datetime.utcnow() 
                
                if last_mutation_count != stats_dict['total_mutations']:
                    if iterations > 0:
                        print str(timestamp) + " Convergence on "+args.device+" is occurring - total FIB mutations: "+str(stats_dict['total_mutations'])
                        for table in tables:
                            for key in stats_dict[table]['stats']:
                                for metric in metrics:
                                    delta_metric = 'delta_'+metric
                                    if metric == key:
                                        if int(stats_dict[table]['stats'][delta_metric]) > 0:
                                            print "   "+str(timestamp)+" "+table+" "+metric +" "+ str(stats_dict[table]['stats'][delta_metric])
                           
                    last_mutation_count = stats_dict['total_mutations']
                    stats_dict['total_mutations'] = 0
                
                else:
                    print str(timestamp) + " No convergence on "+args.device+" is occurring - total FIB mutations: "+str(stats_dict['total_mutations'])
                
                
                iterations += 1 
                sleep(interval)
    else:
        parser.print_usage()

if __name__ == "__main__":
    main()
