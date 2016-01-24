from distutils.core import setup

setup(
        name            = 'fastsnmpy2',
        version         = '1.2.1',
        py_modules      = ['fastsnmpy','example'],
        author          = 'Ajay Divakaran',
        author_email    = 'ajaysdesk@gmail.com',
        url             = 'http://www.ajaydivakaran.com/fastsnmpy',
	download_url	= 'http://www.github.com/ajaysdesk/fastsnmpy',
	license		= 'BSD',
        description     = 'Superfast snmp bulkwalk method implemented using net-snmp bindings for getbulk',
        long_description     = 
'''Fastsnmpy is a module that leverages python-extensions that come
with net-snmp and provide highly parallelized faster-methods to walk
oid-trees on devices.

In addition, it provides a method to bulkwalk mib-trees. BulkWalk
methods are missing from native python-bindings for net-snmp. By
creating a wrapper around the GetBulk method instead, and maintaining
state while traversing the oid-tree, fastsnmpy provides a clever 
solution to bulkwalk oids much faster.

It provides the following methods as of Fastsnmpy-1.2.1

- snmpwalk(): Native python-bindings distributed with
  net-snmp, combined with fastsnmpy's ability to parallelize
  snmpwalk operations. 

- snmpbulkwalk(): Ability to snmpbulkwalk devices, which makes 
  it several magnitudes faster than net-snmp's implementation of snmpwalk.

  By leveraging the getbulk method, this module provides a quick
  snmpbulkwalk utility.

- PROCESS-POOLS: By passing in a 'workers=n' attribute to the above 
  methods, fastsnmpy can instantiate a process-pool to parallelize
  the snmpwalk and snmpbulkwalk methods, resulting in several devices 
  being walked at the same time, 
  effectively using all cores on a multicore machine.

- One-Line, and Two-Line scripts that enable you to discover/walk
  all devices in a whole datacenter

- Both Linux and Windows support
'''
        )

