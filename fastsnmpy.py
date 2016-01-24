#!/usr/local/bin/python

""" fastsnmpy is a collection of classes that greatly increase
the speed of snmp discovery, providing methods like snmpbulkwalk
and multiwalk (for multithreaded snmp) """
import netsnmp
from multiprocessing import Process, Queue

class SnmpSession:
    """ The main snmpsession class gets defined here. You may 
    later call one of the several methods defined on this class"""
    def __init__(self,
                oidlist = ["sysDescr"],
                version = 2,
                targets = [""],
                community = "public",
                maxreps  = 8,
                ):
        self.oidlist = oidlist        
        self.version = version
        self.targets = targets 
        self.community = community
        self.maxreps = maxreps
        self.results = []

    def seqwalk(self):
        """ This is the most basic walk. It runs the default 
        snmpwalk from netsnmp's python bindings """
        for target in self.targets:
            for oid in self.oidlist:
                print "Getting %s from %s " %(oid,target)
                # Instantiate Session class from netsnmp
                mysession = netsnmp.Session(
                                    Version = self.version,
                                    DestHost = target,
                                    Community = self.community
                                    )
                vars = netsnmp.VarList(
                        netsnmp.Varbind(oid)
                        )
                result = mysession.walk(vars)
                # Format and returns result
                for i in vars:
                    i.hostname = target
                    i.oid = oid
                    self.results.append(i)
        return self.results
        
    def bulkwalk(self):
        """ This class uses the default getbulk methods to
        actually provide a bulkwalk method superior to snmpwalk"""
        for target in self.targets:
            for oid in self.oidlist:
                print "Getting %s from %s " %(oid,target)
                # Instantiate Session class from netsnmp
                mysession = netsnmp.Session(
                                    Version = self.version,
                                    DestHost = target,
                                    Community = self.community
                                    )
                # Start from ifindex 0, and use getbulk operations
                startindex = 0
                thistree = oid
                while (thistree == oid):
                    vars = netsnmp.VarList(
                            netsnmp.Varbind(oid,startindex)
                            )
                    result = mysession.getbulk(0,self.maxreps,vars)
                    for i in vars:
                        if i.tag == thistree:
                            i.hostname = target
                            i.oid = oid
                            self.results.append(i)
                    # If startindex is null ( Bug Fix )
                    if not vars[-1].iid:
                        break
                    # Refresh thistree name and increment startindex
                    else:
                        thistree = vars[-1].tag
                        startindex = int(vars[-1].iid)
                    # If startindex still 0 ( Bug Fix for 6500s )
                    if startindex == 0 :
                        break
        return self.results
        
    def multiwalk(self,mode = 'seqwalk'):
        """ Multiwalk is a multithreaded implementation. It uses
        either sequential or getbulk methods, to walk a node """

        ### Define number of threads
        hosts = self.targets
        numthreads = len(hosts)

        for thisoid in self.oidlist:
            #Create queues for threadinput and threadoutput
            threadinput = Queue()
            threadoutput = Queue()
            #put each targethost into the queue
            for target in self.targets:
                threadinput.put(target)
            #Call the thread worker process on the queue for as many targets
            for i in range(numthreads):
                Process(target=self.multiworker, 
                        args=(threadinput, threadoutput,thisoid,mode)).start()
            #Collect results from threads
            for i in range(numthreads):
                myresp = threadoutput.get()
                for resp in myresp:
                    self.results.append(resp)
            #Tell child processes to stop
            for i in range(numthreads):
                threadinput.put('STOP')
                print "Stopping %s" %i

        return self.results    
            
    # Function run by worker processes
    def multiworker(caller,input, output, oid, mode):
        for target in iter(input.get, 'STOP'):
            print "Getting %s from %s " %(oid,target)
            threadresults = []
            mysession = netsnmp.Session(
                                Version = caller.version,
                                DestHost = target,
                                Community = caller.community
                                        )
            if mode == 'seqwalk':
                # For seqwalk mode, we just call netsnmp's implementn
                vars = netsnmp.VarList(
                        netsnmp.Varbind(oid)
                        )
                result = mysession.walk(vars)
                for i in vars:
                    i.hostname = target
                    i.oid = oid
                    threadresults.append(i)

            if mode == 'bulkwalk':
                # Our custom method to do bulkwalks, very speedy!
                startindex = 0
                thistree = oid
                while (thistree == oid):
                    vars = netsnmp.VarList(
                            netsnmp.Varbind(oid,startindex)
                            )
                    result = mysession.getbulk(0,caller.maxreps,vars)
                    for i in vars:
                        if i.tag == thistree:
                            i.hostname = target
                            i.oid = oid
                            threadresults.append(i)
                    # If startindex is null ( Bug Fix )
                    if not vars[-1].iid:
                        break
                    # Refresh thistree name and increment startindex
                    else:
                        thistree = vars[-1].tag
                        startindex = int(vars[-1].iid)
                    # If startindex still 0 ( Bug Fix for 6500s )
                    if startindex == 0 :
                        break

            output.put(threadresults)

""" Actual code begins below this line. The classes above dont need
to be modified. They can just be copied and pasted .
Installation is a much cleaner way though. 
You can see the documentation at http://www.ajaydivakaran.com/fastsnmpy"""

""" EXAMPLE CODE   

if __name__ == "__main__":
    #clients and Oids
    hosts =['sny-j1']
    oids = ['ifDescr']

    newsession = SnmpSession ( targets = hosts, 
            oidlist = oids,
            community='robotech' 
            )
#    results = newsession.bulkwalk()   # For seqwalk -default
    results = newsession.multiwalk(mode = 'bulkwalk')
    for identifier,eachline in results.iteritems():
        print identifier,eachline.tag,eachline.iid,eachline.val

    EXAMPLE CODE ENDS """
