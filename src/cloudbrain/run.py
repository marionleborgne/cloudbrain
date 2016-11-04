import simplejson as json
import logging
import time

from argparse import ArgumentParser

from cloudbrain.modules.runner import ModuleRunner



class _CommandLineArgError(Exception):
    """ Error parsing command-line options """
    pass



class _Options(object):
    """Options returned by _parseArgs"""


    def __init__(self, file_conf, json_conf, log_level):
        """
        :param str file_conf: path to JSON file with module configs.
        :param str file_conf: JSON string with module configs.
        :param str log_level: logger verbosity 'info' for logging.INFO or
            'debug' for logging.DEBUG.
        """
        self.file_conf = file_conf
        self.json_conf = json_conf
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

    parser = ArgumentParser(description="Start CloudBrain modules runner.")

    parser.add_argument(
        "--file",
        type=str,
        dest="file_conf",
        default=None,
        help="Path to JSON file with modules configuration.")

    parser.add_argument(
        "--json",
        type=str,
        dest="json_conf",
        default=None,
        help="JSON string with modules configuration.")

    parser.add_argument(
        "--log",
        type=str,
        dest="log_level",
        required=False,
        default='info',
        help="OPTIONAL: logger verbosity. Can be 'info' or 'debug'.")

    options = parser.parse_args()

    if options.file_conf is None and options.json_conf is None:
        raise ValueError("Module configuration must be provided with the "
                         "--file or --json flags.")
    elif options.file_conf and options.json_conf:
        raise ValueError("Only one module configuration can be provided, "
                         "either with the flag --file or --json.")

    return _Options(file_conf=options.file_conf,
                    json_conf=options.json_conf,
                    log_level=options.log_level)



def run(file_conf, json_conf, log_level):
    logging.basicConfig(level=log_level)

    if file_conf:
        with open(file_conf, 'rb') as f:
            module_configs = json.load(f)
    elif json_conf:
        module_configs = json.loads(json_conf)

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
        run(options.file_conf, options.json_conf, options.log_level)
    except Exception as ex:
        logging.exception("Modules runner failed")



if __name__ == '__main__':
    main()
