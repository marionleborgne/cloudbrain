__author__ = 'odrulea'
from abc import ABCMeta, abstractmethod
from cloudbrain.subscribers.PikaSubscriber import PikaSubscriber
from cloudbrain.publishers.PikaPublisher import PikaPublisher
import time

class ModuleAbstract(object):
    __metaclass__ = ABCMeta

    MODULE_NAME = "Abstract"

    def __init__(self, device_name, device_id, rabbitmq_address, input_feature, output_feature=None, module_params = None):
        """
        global constructor for all module classes, not meant to be overwritten by subclasses
        :param device_name:
        :param device_id:
        :param rabbitmq_address:
        :param input_feature:
        :param output_feature:
        :param module_params:
        :return:
        """

        # set global properties common to all
        self.device_name = device_name
        self.device_id = device_id
        self.rabbitmq_address = rabbitmq_address
        self.input_feature = input_feature
        self.output_feature = output_feature
        self.module_params = module_params # subclasses can set further from this in setup()
        self.subscriber = None
        self.publisher = None

        # debug
        self.debug = False
        if 'debug' in self.module_params:
            if self.module_params['debug'] is True:
                self.debug = True


        # call setup()
        self.setup()

    @abstractmethod
    def setup(self):
        """
        Generic setup for any analysis module, can be overriden by implementing in any child class
        This sets up subscriber and publisher based on input and output feature names
        """

        # if input, start subscriber
        if self.input_feature is not None:
            self.subscriber = PikaSubscriber(device_name=self.device_name,
                                                 device_id=self.device_id,
                                                 rabbitmq_address=self.rabbitmq_address,
                                                 metric_name=self.input_feature)

        # if output, start publisher
        if self.output_feature is not None:
            self.publisher = PikaPublisher(device_name=self.device_name,
                                                 device_id=self.device_id,
                                                 rabbitmq_address=self.rabbitmq_address,
                                                 metric_name=self.output_feature)



    def start(self):
        """
        Consume and write data to file
        :return:
        """
        if self.debug:
            print self.MODULE_NAME + ": starting sub"

        self.subscriber.connect()

        if self.publisher is not None:
            if self.debug:
                print self.MODULE_NAME + ": starting pub"
            self.publisher.connect()

        self.subscriber.consume_messages(self.consume)

        return

    def stop(self):
        """
        Unsubscribe and close file
        :return:
        """
        print "Abstract: stopped"
        self.subscriber.disconnect()


    def consume(self, ch, method, properties, body):
        """
        consume the message queue from rabbitmq
        :return:
        """
        print "Abstract: consume"



