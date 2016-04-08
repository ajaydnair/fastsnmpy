
''' 

fastsnmpy is a collection of classes that greatly increase
the speed of snmp discovery, providing methods like snmpbulkwalk
and multiwalk (for multiprocess snmp). 

snmpbulkwalk is not a feature 
of the python-bindings that come with net-snmp as of this release.
By leveraging the getbulk method, this module provides a quick 
snmpbulkwalk utility.

    name      = 'fastsnmpy',
    version     = '1.2.1',
    py_modules   = ['fastsnmpy','example'],
    author     = 'Ajay Divakaran',
    author_email  = 'ajaysdesk@gmail.com'
    url       = 'http://www.ajaydivakaran.com/fastsnmpy',
    description   = 'Superfast snmp bulkwalk method 
        implemented using net-snmp bindings for getbulk'

PROVIDES METHODS:
    snmpwalk(workers=1): runs snmpwalk using net-snmp's bindings
    snmpbulkwalk(workers=1): runs the faster snmpbulkwalk implemented here
 '''

# -------
# IMPORTS
# -------

import netsnmp
from multiprocessing import Queue, Pool
import json


# -------
# CLASSES
# -------

class SnmpSession:

    ''' The main snmpsession class gets defined here. You may 
    later call one of the several methods defined on this class'''

    def __init__(self,
        oidlist = ['sysDescr'],
        version = 2,
        targets = [''],
        community = 'public',
        maxreps = 8,):

        self.oidlist = oidlist    
        self.version = version
        self.targets = targets 
        self.community = community
        self.maxreps = maxreps
        self.results = []


    def snmpwalk(self, workers = 1):

        ''' This is the most basic walk. It runs the default 
        snmpwalk from netsnmp's python bindings '''

        return self._run_queries( worker_snmpwalk, workers )

       
    def snmpbulkwalk(self, workers = 1):

        ''' Bulkwalk is essentially a series of getBulk operations, just
        like walk is a series of get(getNext) operations.

        This is where the power and speed of fastsnmpy shows, as native 
        net-snmp bindings have no equivalent'''

        return self._run_queries( worker_snmpbulkwalk, workers )


    def _run_queries(self, mode, processes):

        in_list = self._build_input_list()
        out_q = Queue() 

        print 'Starting worker pool with %s processes' %int(processes)
        worker_pool = Pool(processes = int(processes))
        worker_pool.map_async(mode, in_list, callback=out_q.put)
        worker_pool.close()
        worker_pool.join()

        return _parse_results(out_q)


    def _build_input_list(self):

        in_q = []
 
        for target in self.targets:
            for oid in self.oidlist:
                entity = { 'target':target, 'oid':oid, 'version':self.version,
                    'community':self.community, 'maxreps':self.maxreps }
                in_q.append(entity)
       
        return in_q
    


# ---------
# FUNCTIONS
# ---------


def worker_snmpbulkwalk(entity):

    ''' worker called by snmpbulkwalk function. operates on a single
    node-mib object '''

    target = entity['target']
    oid = entity['oid']
    maxreps = entity['maxreps']

    print 'Getting %s from %s ' %(oid,target)
    mysession = netsnmp.Session(
        Version = entity['version'],
        DestHost = target,
        Community = entity['community'],
        UseNumeric = 1,
    )
        
    results = []

    # Start from ifindex 0, and use getbulk operations
    startindex = 0

    thistree = oid
    while (thistree == oid):

        vars = netsnmp.VarList(netsnmp.Varbind(oid,startindex))
        result = mysession.getbulk(0,maxreps,vars)

        for i in vars:
            if i.tag == thistree[:len(i.tag)]:
                i.hostname = target
                i.oid = oid
                results.append(i)

        # If startindex is null ( Bug Fix )
        if not vars[-1].iid: break

        # Refresh thistree name and increment startindex
        else:
            thistree = vars[-1].tag
            startindex = int(vars[-1].iid)

        # If startindex still 0 ( Bug Fix for 6500s )
        if startindex == 0 : break

        # -- Format and returns result
        for i in vars:
            i.hostname = target
            i.oid = oid
            results.append(i)

    return results



def worker_snmpwalk(entity):

    ''' worker called by snmpwalk function. operates on a single
    node-mib object '''

    target = entity['target']
    oid = entity['oid']

    print 'Getting %s from %s ' %(oid,target)

    mysession = netsnmp.Session(
        Version = entity['version'],
        DestHost = target,
        Community = entity['community']
    )
        
    vars = netsnmp.VarList( netsnmp.Varbind(oid))
    result = mysession.walk(vars)

    # -- Format and returns result
    results = []
    for i in vars:
        i.hostname = target
        i.oid = oid
        results.append(i)

    return results


def _parse_results(q):

    results = []

    for vb_list in q.get():
        for vb in vb_list:
           results.append(vb.__dict__)

    return json.dumps(results, indent=2)


'''
EXAMPLE :
Actual code begins below this line. The classes above dont need
to be modified. They can just be copied and pasted .
Installation is a much cleaner way though. 
You can see the documentation at http://www.ajaydivakaran.com/fastsnmpy

if __name__ == '__main__':

    hosts =['c7200-2','c7200-1','c2600-1','c2600-2']
    oids = ['ifDescr', 'ifIndex', 'ifName', 'ifDescr']

    newsession = SnmpSession ( targets = hosts, 
        oidlist = oids,
        community='oznet' 
    )

    print newsession.snmpwalk(workers=5)  # For snmpwalk -default

    print newsession.snmpbulkwalk() # Fastsnmpy - bulkwalk

'''

