import threading



def _get_class(package, class_name):
    mod = __import__(package, fromlist=[class_name])
    return getattr(mod, class_name)



class ModuleRunner(object):
    def __init__(self, module_configs):

        self.threads = []
        self.module_configs = module_configs["modules"]


    def start(self):

        for mod_config in self.module_configs:
            Module = _get_class(mod_config["package"], mod_config["name"])

            publishers = []
            for pub_config in mod_config["publishers"]:
                Publisher = _get_class(pub_config["package"], pub_config["name"])
                publisher = Publisher(pub_config["base_routing_key"],
                                      **pub_config["options"])
                publisher.connect()

                for metric_options in pub_config["metrics"]:
                    publisher.register(**metric_options)

                publishers.append(publisher)

            subscribers = []
            for sub_config in mod_config["subscribers"]:
                Subscriber = _get_class(sub_config["package"], sub_config["name"])
                subscriber = Subscriber(sub_config["base_routing_key"],
                                      **sub_config["options"])
                subscriber.connect()

                for metric_options in sub_config["metrics"]:
                    subscriber.register(**metric_options)

                subscribers.append(subscriber)

            module = Module(subscribers, publishers, **mod_config['options'])
            t = threading.Thread(target=module.start)
            t.daemon = True
            self.threads.append(t)
            t.start()


    def stop(self):
        for t in self.threads:
            t.join(0)
