#!/bin/env python 

import subprocess


from monasca_agent.collector.checks.check import AgentCheck

PREFIX_ROUTER = 'qrouter-'

class QrouterPlugin(AgentCheck):

    """ Inherit from Agent class and collect router's metrics"""
    def __init__(self, name, init_config, agent_config, instances=None):
        AgentCheck.__init__(self, name, init_config, agent_config, instances)

    def netns_discovery(self):
        routers = []
        #Listing network namespaces present on the host                                                                                  
        ns = subprocess.check_output(['sudo', 'ip', 'netns', 'list'])
        if ns == '':
            self.log.warn("No namespace found. Either DVR agent_mode is enabled"                                           
                           "or routing is centralized.")
        #Extracting router from dhcps namespaces
        qrouter = ns.split()
        if qrouter:
            for ns in qrouter:
                if PREFIX_ROUTER in ns:
                    qrouters.append(ns)

        #Extracting router from dhcps namespaces
        from neutronclient.v2_0 import client
        nu = client.Client(username=self.init_config.get('admin_user'),
                           password=self.init_config.get('admin_password'),
                           tenant_name=self.init_config.get('tenant_name'),
                           auth_url=self.init_config.get('keystone_url'),
                           endpoint_type='internalURL')
        routers = nu.list_routers()['routers']
    
        # Making a dictionary of routers with their corresponding tenant ids
        for router in routers:
            router_tenant[PREFIX_ROUTER + router['id']] = router['tenant_id']
            
            print(router_tenant[qrouters[0]])

    def check(self, instance=None):
        netns = netns_discovery(self)


#Testing
def netns_discovery():
    qrouters = []
    router_tenant = {}
    #Listing network namespaces present on the host                                                                                  
    ns = subprocess.check_output(['sudo', 'ip', 'netns', 'list'])
    if ns == '':
        self.log.warn("No namespace found. Either DVR agent_mode is enabled"                                           
                      "or routing is centralized.")
 
    #converting byte string to string of string    
    qrouter = ns.split()
    if qrouter:
        for ns in qrouter:
            if PREFIX_ROUTER in ns:
                qrouters.append(ns)
    #Extracting router from dhcps namespaces

    from neutronclient.v2_0 import client
    nu = client.Client(username="admin",
                       password="3819292",
                       tenant_name="admin",
                       auth_url="http://192.168.8.101:35357/v2.0",
                       endpoint_type='internalURL')
    routers = nu.list_routers()['routers']
    
    # Making a dictionary of routers with their corresponding tenant ids
    for router in routers:
        router_tenant[PREFIX_ROUTER + router['id']] = router['tenant_id']
 
    print(router_tenant[qrouters[0]])
    print(router_tenant[qrouters[1]])
        

netns_discovery()
