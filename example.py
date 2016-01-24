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
    for identifier,eachline in results.iteritems():
        print identifier,eachline.tag,eachline.iid,eachline.val

"""    EXAMPLE CODE ENDS """