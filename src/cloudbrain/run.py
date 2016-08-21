import json
import logging
import time
# import validictory
# import pkg_resources

from argparse import ArgumentParser

from cloudbrain.modules.runner import ModuleRunner



class _CommandLineArgError(Exception):
    """ Error parsing command-line options """
    pass



class _Options(object):
    """Options returned by _parseArgs"""


    def __init__(self, module_configs, log_level):
        """
        :param str module_configs: path to JSON file with module configs.
        :param str log_level: logger verbosity 'info' for logging.INFO or 'debug' for logging.DEBUG.
        """
        self.module_configs = module_configs

        if log_level == 'info':
            self.log_level = logging.INFO
        elif log_level == 'debug':
            self.log_level = logging.DEBUG



def _parseArgs():
    """
    Parse command-line args
    :rtype: _Options object
    :raises _CommandLineArgError: on command-line arg error
    """

    parser = ArgumentParser(description=("Start CloudBrain modules runner."))

    parser.add_argument(
        "--conf",
        type=str,
        dest="module_configs",
        required=True,
        help="REQUIRED: path to JSON file with modules configuration.")

    parser.add_argument(
        "--log",
        type=str,
        dest="log_level",
        required=False,
        default='info',
        help="OPTIONAL: logger verbosity. Can be 'info' or 'debug'.")

    options = parser.parse_args()

    # TODO: validate module configurations schema
    # with pkg_resources.resource_stream(__name__,
    #                                    "module_configs_schema.json") as modulesSchema:
    #
    #     try:
    #         validictory.validate(json.load(options.module_configs), json.load(modulesSchema))
    #     except validictory.ValidationError as exc:
    #         logging.exception("JSON schema validation of --conf file failed")
    #         parser.error("JSON schema validation of --conf file failed: {}"
    #                      .format(exc))

    return _Options(module_configs=options.module_configs, log_level=options.log_level)



def run(module_configs_file, log_level):
    logging.basicConfig(level=log_level)

    with open(module_configs_file, 'rb') as f:
        module_configs = json.load(f)
        runner = ModuleRunner(module_configs)
        try:
            runner.start()
            while 1:
                time.sleep(0.1)
        except KeyboardInterrupt:
            runner.stop()



def main():
    try:
        options = _parseArgs()
        run(options.module_configs, options.log_level)
    except Exception as ex:
        logging.exception("Modules runner failed")



if __name__ == '__main__':
    main()
