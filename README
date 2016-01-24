		     		fastsnmpy README
			Python classes that extend the 
		Functionality of 'netsnmp' Extension Module

### Main Features

Fastsnmpy is a module that leverages python-extensions that come 
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


### Quick example - Running in interactive mode
<pre>
Python 2.7.10 (default) 

>>> import netsnmp
>>> from fastsnmpy import SnmpSession

>>> hosts =['c7200-2','c7200-1','c2600-1','c2600-2']
>>> oids = ['ifDescr', 'ifIndex', 'ifName', 'ifDescr']
>>> newsession = SnmpSession ( targets = hosts, oidlist = oids, community='oznet' )

>>> results = newsession.snmpbulkwalk(workers=15)
>>> len(results)
171031
>>> 
</pre>
Note: To use the module in scripts, please see the example.py 
included with the package.


### Benchmarks
(1) Walking 30 nodes for ifDescr using snmpwalk():
	
	time ./fastsnmpy.py
	real    0m18.63s
	user    0m1.07s
	sys     0m0.38s

(2) Walking 30 nodes for ifDescr using snmpbulkwalk():

	time ./fastsnmpy.py
	real    0m9.17s
	user    0m0.48s
	sys     0m0.11s

(3) Walking 30 nodes for ifDescr using snmpwalk(workers=10):

	time ./fastsnmpy.py
	real    0m2.27s
	user    0m2.87s
	sys     0m0.66s

(4) Walking 30 nodes for ifDescr using snmpbulkwalk(workers=10):

	time ./fastsnmpy.py
	real    0m0.90s
	user    0m2.44s
	sys     0m0.40s

As you can see, fastsnmpy's bulkwalk mode is almost 20 times faster 
than using python's native snmp bindings for walking
	

### Requirements:
fastsnmpy module makes use of net-snmp and python extensions for 
net-snmp. To use these classes, all you need to do is install net-snmp
along with python bindings.
Please review the LICENSE agreements for both, that are available from 
their respective websites.

There are two ways to install this.
(1) You can just copy all the classes in the code and paste it into
your script. This provides a quick, but very dirty way of using fastsnmpy
(2) Download the fastsnmpy distribution, and install it as follows. This
is the neatest method to use fastsnmpy:
	- untar the download
	- navigate to the directory
	- run "python setup.py install"
If you get stuck at any point, refer to the online documentation.
http://www.ajaydivakaran.com/fastsnmpy


### Release:
The most recent release should be available from PyPy, or from the 
author's website at http://www.ajaydivakaran.com/fastsnmpy


### How to use
See example.py included with this build. I plan to put up more examples
on the website. So you may want to check there as well. 


### Acknowledgments:
The net-snmp-coders and the authors of 'python netsnmp extension'
Thanks in advance to any who supply patches, suggestions and feedback.

### License:

          fastsnmpy classes for 'netsnmp extension module'
                    Copyright (c) 2010-2016 Ajay Divakaran

'fastsnmpy' is free to use . This includes the classes and modules of 
fastsnmpy as well as any examples and code contained in the package.
I am hereby releasing this under BSD, which is the most permissive form
of licensing - giving you the freedom to do what you want with this code.

A linkback would be appreciated to www.ajaydivakaran.com.

Copyright (c) <2010-2016> <www.ajaydivakaran.com>

Permission is hereby granted, free of charge, to any person obtaining 
a copy of this software and associated documentation files 
(the “Software”), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS 
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR 
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE. 3


Additional requirements : You need to have netsnmp and the python 'netsnmp'
modules installed. All License terms of those packages should be followed. 
Please read  and review license terms for python 'netsnmp' extension module
and net-snmp itself.

