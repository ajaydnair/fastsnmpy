from fastsnmpy import SnmpSession
""" EXAMPLE CODE  """

if __name__ == "__main__":
    #clients and Oids
    hosts =[]
    srcfile = open("hosts")
    for line in srcfile.readlines():
        hosts.append(line.rstrip('\n'))
    srcfile.close()    
    oids = ['ifName']

    newsession = SnmpSession ( targets = hosts, 
            oidlist = oids,
            community='oznet' 
            )
#    results = newsession.bulkwalk()   # For seqwalk -default
    results = newsession.multiwalk(mode = 'bulkwalk')
    for vb in results:
        print vb.__dict__


"""    EXAMPLE CODE ENDS """
