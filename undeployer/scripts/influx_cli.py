#!/usr/bin/env python

import sys
import time
from cloudify_rest_client.executions import Execution
from cloudify_cli.utils import get_rest_client
from influxdb.influxdb08 import InfluxDBClient
from influxdb.influxdb08.client import InfluxDBClientError

client = get_rest_client()
deployment_id = sys.argv[1]
mngr_ip_address = sys.argv[2]
node_name = sys.argv[3]
print 'Executions of deployment {0} on manager {1}'.format(deployment_id,mngr_ip_address)
influx_client = InfluxDBClient(host=mngr_ip_address, port=8086, database='cloudify')

#for execution in client.executions.list(deployment_id=deployment_id):    
#	print '  Execution {0} is in state: {1}'.format(execution.id, execution.status)
relevant_nodes = [node_name , 'xap_container_vm']
nodes = client.nodes.list(deployment_id=deployment_id)
if nodes is not None:	
    for node in nodes:
        #print dir(node)
        print 'Checking node id {0}'.format(node.id)
        if node.id in relevant_nodes:
            print ' ----------------------- '
            print ' Node id: {0}'.format(node.id)
            print ' Node type: {0}'.format(node.type)
            print ' Node type_hierarchy: {0}'.format(node.type_hierarchy)
            print '  blueprint_id:{0}'.format(node.blueprint_id)
            print '  deployment_id: {0}'.format(node.deployment_id)
            #print '  host_id: {0}'.format(node.host_id)
            print '  --- '
            print '  properties: '
            for curr_key in node.properties:
                print '   {0}:{1}'.format(curr_key,node.properties[curr_key])
            print '  --- '
            print '  relationships: '
            #for curr_key in node.relationships:
            #    print '   {0}:{1}'.format(curr_key,node.relationships[curr_key])
            print '  --- '
            print "  Checking instances of {0}".format(node.id)
            for instance in client.node_instances.list(deployment_id=deployment_id, node_id=node.id):
                print '    instance id is {0}'.format(instance.id)
                q_string = 'SELECT MEAN(value) FROM /' + deployment_id + '\.' + node.id + '\.' + instance.id + '\.cpu_total_system/ GROUP BY time(10s) '\
                    'WHERE  time > now() - 600s'
                #q_string = 'select  mean(value) from /xxx0706_v2\..*?\.cpu_total_system/ where  time > now() - 15m     group by time(10)  order asc'
                print '     Query is :{0}'.format(q_string)
                try:
                    result = influx_client.query(q_string)
                    print '     Result is'
                    print '       {0} \n'.format(result)
                    if not result:                    
                        print '     There are no results'
                except InfluxDBClientError as ee:
                    print '     DBClienterror {0}\n'.format(str(ee))
                except Exception as e:
                    print '     {0}'.formatstr(e)

else:
	print "nodes list is empty"		


print 'Done with deployment: {0}'.format(deployment_id)
