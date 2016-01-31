__author__ = 'odrulea'

from cloudbrain.utils.metadata_info import get_supported_metrics, get_supported_devices
from cloudbrain.settings import RABBITMQ_ADDRESS, MOCK_DEVICE_ID
import argparse
import imp
import os
import yaml
import time
import threading

_SUPPORTED_DEVICES = get_supported_devices()
_SUPPORTED_METRICS = get_supported_metrics()


class AnalysisModulesService(object):
    """
    Subscribes and writes data to a file
    Only supports Pika communication method for now, not pipes
    """

    def __init__(self, device_name, device_id, rabbitmq_address=None):

        if rabbitmq_address is None:
            raise ValueError("Pika subscriber needs to have a rabbitmq address!")

        # set vars
        self.device_name = device_name
        self.device_id = device_id
        self.rabbitmq_address = rabbitmq_address

        # local relative filepath, used to load config file and to dynamically load classes
        self.location = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)) )

        # this will hold the config yaml info as an array
        self.conf = None

        # setup more vars
        self.setup()

    def setup(self):

        # get config from yaml file (default = ./conf.yml)
        settings_file_path = os.path.join(self.location, 'conf.yml')
        stream = file(settings_file_path, 'r')
        # set local conf property from the yaml config file
        self.conf = yaml.load(stream)

    def start(self):

        # loop through each module and start them
        # passing the output from one to the input of the other
        for moduleName,settings in self.conf.iteritems():

            # input_feature is required
            if 'input_feature' in settings:
                input_feature = settings['input_feature']
            else:
                raise ValueError("Required input_feature missing for Module: " + moduleName)

            # output_feature (optional)
            if 'output_feature' in settings:
                output_feature = settings['output_feature']
            else:
                output_feature = None

            # module parameters (optional)
            if 'parameters' in settings:
                module_params = settings['parameters']
            else:
                module_params = None

            self.launchModule(moduleName, self.device_name, self.device_id, self.rabbitmq_address, input_feature, output_feature, module_params)

        # this is here so that child threads
        while True:
            time.sleep(1)

    def launchModule(self, moduleName, device_name, device_id, rabbitmq_address, input_feature, output_feature, module_params):
        if 'debug' in module_params and module_params['debug'] == True:
            #print module_params['debug'] == True
            # debug
            print
            print "Module: " + moduleName
            print "in: " + input_feature
            print "out: " + str(output_feature)
            print "device_name: " + device_name
            print "device_id: " + device_id
            print "rabbitmq_address: " + rabbitmq_address
            print "module_params: " + str(module_params)

        # dynamically import the module
        module_filepath = os.path.join(self.location, moduleName+'.py')
        py_mod = imp.load_source(moduleName, module_filepath)
        # instantiate the imported module
        moduleInstance = getattr(py_mod, moduleName)(device_name=device_name, device_id=device_id,
                                                     rabbitmq_address=rabbitmq_address, input_feature=input_feature,
                                                     output_feature=output_feature, module_params=module_params)


        # all modules should implement start() and stop()
        thread = threading.Thread(target=moduleInstance.start)
        thread.daemon = True
        thread.start()


        #moduleInstance.stop()



def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--device_id', required=True,
                        help="A unique ID to identify the device you are sending data from. "
                             "For example: 'octopicorn2015'")
    parser.add_argument('-n', '--device_name', required=True,
                        help="The name of the device your are sending data from. "
                             "Supported devices are: %s" % _SUPPORTED_DEVICES)
    parser.add_argument('-c', '--cloudbrain', default=RABBITMQ_ADDRESS,
                        help="The address of the CloudBrain instance you are sending data to.\n"
                             "Use " + RABBITMQ_ADDRESS + " to send data to our hosted service. \n"
                                                         "Otherwise use 'localhost' if running CloudBrain locally")

    opts = parser.parse_args()

    return opts


def main():
    opts = parse_args()

    device_name = opts.device_name
    device_id = opts.device_id
    cloudbrain_address = opts.cloudbrain

    run(device_name,
        device_id,
        cloudbrain_address
        )

def run(device_name='muse',
        device_id=MOCK_DEVICE_ID,
        cloudbrain_address=RABBITMQ_ADDRESS
        ):
    print "Collecting data ... Ctl-C to stop."
    service = AnalysisModulesService(device_name=device_name,
                          device_id=device_id,
                          rabbitmq_address=cloudbrain_address
                          )
    service.start()


if __name__ == "__main__":
    main()


