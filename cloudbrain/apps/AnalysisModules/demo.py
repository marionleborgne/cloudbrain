__author__ = 'odrulea'
import os
import yaml
import numpy as np
import imp
import json
import threading

########################################
# this is just a "scratch pad" file to test with
# probably should be excluded from github repo, but just leaving it in for now...


from cloudbrain.utils.metadata_info import get_num_channels, get_supported_metrics, get_supported_devices
from cloudbrain.apps.AnalysisModules.utils import json_numpy_obj_hook, NumpyEncoder

__location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)) )
settings_file_path = os.path.join(__location__, 'conf.yml')
print settings_file_path

stream = file(settings_file_path, 'r')


chain = yaml.load(stream)
print chain

for moduleName,settings in chain.iteritems():
    print moduleName
    print "in: " + settings['input_feature']
    #print "out: " + settings['output_feature']


    print "params: " + str(settings['parameters'])
    #print settings['parameters']['window_overlap']

    if 'foo' in settings['parameters']:
        print "There is FOO"
    else:
        print "There is no FOO"

    #module_filepath = os.path.join(__location__, moduleName+'.py')
    #py_mod = imp.load_source(moduleName, module_filepath)
    #class_inst = getattr(py_mod, moduleName)()


def checkThreads(foo):
    mydata = threading.local()
    mydata.count = 0
    while mydata.count < 100:
        print "my name is thread " + str(threading._get_ident()) + " and I say: " + foo
        mydata.count = mydata.count + 1

    return



window = np.zeros((5, 8))

dumped = json.dumps(window, cls=NumpyEncoder)
result = json.loads(dumped, object_hook=json_numpy_obj_hook)

#print result
arr = np.array([0,1,2,3,4,5,6,7])

trimarr = np.arange(3)
result = np.delete(result, trimarr, 0)

#print result

thread = threading.Thread(target=checkThreads, args=("FUN",))
thread.start()

thread = threading.Thread(target=checkThreads, args=("TIMES",))
thread.start()
