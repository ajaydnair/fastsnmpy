from fastsnmpy import SnmpSession

'''
This example demonstrates the usage of snmpwalk, and snmpbulkwalk 
methods of fastsnmpy package.

snmpwalk, just provides an interface to net-snmp's python-bindings.
On top of it, this also provides a way to run queries in parallel
using multiple workers. This greatly speeds up snmpwalk's operation.

snmpbulkwalk, is a fastsnmpy method. By performing get-operations 
in bulk, it greatly enhances the speed of snmpwalk. It also reduces
the number of packets sent to/from the end device, thereby 
decreasing chattiness of the session. 
This method also supports the 'workers' attribute, to parallelize 
snmpbulkwalk operations for a much quicker run.
'''


if __name__ == '__main__':

    hosts =['localhost']
    oids = ['.1.3.6.1.2.1.1.9.1']

    newsession = SnmpSession ( targets = hosts,
        oidlist = oids,
        community='public'
    )

#    print newsession.snmpwalk(workers=5)  # For snmpwalk -default

    print newsession.snmpbulkwalk(workers=15) # Fastsnmpy - bulkwalk

