from cloudbrain.modules.runner import ModuleRunner

if __name__ == '__main__':
  runner = ModuleRunner('conf/hackthebrain_modules_config.json')
  runner.start()