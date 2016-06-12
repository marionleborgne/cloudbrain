import json
import threading

def _get_class(package, class_name):
  mod = __import__(package, fromlist=[class_name])
  return getattr(mod, class_name)

class ModuleRunner(object):
  def __init__(self, config_path):

    self.threads = []

    with open(config_path, 'rb') as conf:
      self.config = json.load(conf)
      self.module_configs = self.config['modules']


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
        pass  # TODO: same logic as publishers

      module = Module(subscribers, publishers, **mod_config["options"])
      t = threading.Thread(target=module.start)
      self.threads.append(t)
      t.start()
