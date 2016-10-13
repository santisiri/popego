import sys, os, glob

def listJobs():
    jobsDir = os.path.dirname(os.path.abspath(
            __import__('popserver.cron',fromlist='__file__').__file__))
    
    moduleNames = map(lambda f: f[:-3], 
                      filter(lambda f: f != '__init__.py', 
                             map(os.path.basename, 
                                 glob.glob(jobsDir + "/*.py"))))

    print "Available Jobs"
    for moduleName in moduleNames:
        module = __import__('popserver.cron.%s' % moduleName,fromlist='__jobDescription__')
        
        print "%20s\t%s" % (moduleName, getattr(module, '__jobDescription__', 'No Description').strip())
    

def executeJob(jobName, args):
    print "Executing %s" % jobName
    module = __import__('popserver.cron.%s' % jobName,fromlist='__jobDescription__')
    module.start(*args)

if len(sys.argv) == 1:
    listJobs()
elif sys.argv[1] == '-h':
    print "Usage: python %s [jobName]" % sys.argv[0]
    sys.exit(1)
elif len(sys.argv) >= 2:
    executeJob(sys.argv[1], sys.argv[2:])


