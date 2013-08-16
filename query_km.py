import p_g, sys, random, time
from ZODB import DB

from ZEO import ClientStorage
from ZODB.FileStorage import FileStorage

runs = int(sys.argv[1])
dbtype = sys.argv[2]

if dbtype.startswith('f'):
    storage = FileStorage('Data.fs')
else:
    clientid = sys.argv[3]
    addr = ('localhost',1234)
    #storage = ClientStorage.ClientStorage(addr,cache_size=2048*1024*1024,client='shm/p_gclient' +clientid)
    storage = ClientStorage.ClientStorage(addr,cache_size=512*1024*1024,client='p_gclient' +clientid)
    #storage = ClientStorage.ClientStorage(addr,cache_size=0)
    #storage = ClientStorage.ClientStorage(addr)


db = DB(storage)
connection = db.open()
root = connection.root()
g=root['graphdb']

#maxnum = int(sys.argv[1])
maxnum = 1000
# given a topic, query all authors that like that topic (10 points) or have written an
# article on it (3 points) or have worked on a project on it (5 points)

def addpoints(found,name,points):
    found[name] = found.setdefault(name,0) + points

def doqueries():

    print 'go'
    times = []
    for r in range(1,runs+1):
        print 'run', r,

        tid = random.randint(1,maxnum)
        tn = 'topic%s' % tid
        print tn, 
        
        start = time.time()

        #query code
        topic = g.name2node(tn)
        found = dict()
        #import ipdb; ipdb.set_trace()

        for nodeid1 in g.incoming[g.typeids['topic']][topic['id']].values():
            node1 = g.nodes[nodeid1]
            label = node1['label']

            if label=='person':
                addpoints(found,nodeid1,10)
            
            elif label == 'article':
                for nodeid2 in g.outgoing[g.typeids['author']][nodeid1].values():
                    addpoints(found,nodeid2,5)
 
            elif label == 'project':
                for nodeid2 in g.outgoing[g.typeids['member']][nodeid1].values():
                    addpoints(found,nodeid2,3)
    
        
        t = time.time()-start
        times.append(t)
        print 'found', len(found),'in',         
        print t

    print 'average: ', sum(times)/r
doqueries()
#conn.close()
#db.close()

#pygraph.connection.close()