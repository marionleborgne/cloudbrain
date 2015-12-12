import argparse

from cloudbrain.publishers.PikaPublisher import PikaPublisher
from cloudbrain.publishers.PipePublisher import PipePublisher
from cloudbrain.utils.metadata_info import get_metrics_names, get_supported_devices
from cloudbrain.settings import RABBITMQ_ADDRESS, MOCK_DEVICE_ID

_SUPPORTED_DEVICES = get_supported_devices()



def validate_opts(opts):
    """
    validate that we've got the right options

    @param opts: (list) options to validate
    @retun opts_valid: (bool) 1 if opts are valid. 0 otherwise.
    """
    opts_valid = True
    if (opts.device_name == "openbci") and (opts.device_port is None):
        opts_valid = False
    return opts_valid



def get_args_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--device_id', required=True,
                        help="A unique ID to identify the device you are sending data from. "
                             "For example: 'octopicorn2015'")
    parser.add_argument('-m', '--mock', action='store_true', required=False,
                        help="Use this flag to generate mock data for a "
                             "supported device name %s" % _SUPPORTED_DEVICES)
    parser.add_argument('-n', '--device_name', required=True,
                        help="The name of the device your are sending data from. "
                             "Supported devices are: %s" % _SUPPORTED_DEVICES)
    parser.add_argument('-c', '--cloudbrain', default=RABBITMQ_ADDRESS,
                        help="The address of the RabbitMQ instance you are sending data to.\n"
                             "Use %s to send data to our hosted service. \n Otherwise use "
                             "'localhost' if running CloudBrain locally" % RABBITMQ_ADDRESS)
    parser.add_argument('-o', '--output', default=None,
                        help="The named pipe you are sending data to (e.g. /tmp/eeg_pipe)\n"
                             "The publisher will create the pipe.\n"
                             "By default this is the standard output.")

    parser.add_argument('-b', '--buffer_size', default=10,
                        help='Size of the buffer ')
    parser.add_argument('-s', '--step_size', default=None,
                        help='Number of samples the chunk advances by (default is equal to buffer size) ')

    parser.add_argument('-p', '--device_port', help="Port used to get data from wearable device.\n"
                                                                  "Common port values:\n"
                                                                  "* 9090 for the Muse\n"
                                                                  "* /dev/tty.usbserial-XXXXXXXX for the OpenBCI")
    parser.add_argument('-M', '--device_mac', help="MAC address of device used for Muse connector.")

    parser.add_argument('-P', '--publisher', default="pika",
                        help="The subscriber to use to get the data.\n"
                             "Possible options are pika, pipe.\n"
                             "The default is pika.")

    return parser



def get_opts():
    parser = get_args_parser()
    opts = parser.parse_args()
    opts_valid = validate_opts(opts)
    if not opts_valid:
        parser.error("You have to speficy the OpenBCI port")
    return opts



def main():
    opts = get_opts()
    mock_data_enabled = opts.mock
    device_name = opts.device_name
    device_id = opts.device_id
    cloudbrain_address = opts.cloudbrain
    buffer_size = int(opts.buffer_size)
    device_port = opts.device_port
    pipe_name = opts.output
    publisher = opts.publisher
    device_mac = opts.device_mac

    step_size = buffer_size
    if opts.step_size is not None:
        step_size = int(opts.step_size)

    run(device_name,
        mock_data_enabled,
        device_id,
        cloudbrain_address,
        buffer_size, step_size,
        device_port,
        pipe_name,
        publisher,
        device_mac)



def run(device_name="muse",
        mock_data_enabled=True,
        device_id=MOCK_DEVICE_ID,
        cloudbrain_address=RABBITMQ_ADDRESS,
        buffer_size=10, step_size=10,
        device_port=None,
        pipe_name=None,
        publisher_type="pika",
        device_mac=None):

    if device_name == "muse" and not mock_data_enabled:
        from cloudbrain.connectors.MuseConnector import MuseConnector as Connector
        if not device_port:
            device_port = 9090
    elif device_name == "openbci" and not mock_data_enabled:
        from cloudbrain.connectors.OpenBCIConnector import OpenBCIConnector as Connector
    elif mock_data_enabled:
        from cloudbrain.connectors.MockConnector import MockConnector as Connector
    else:
        raise ValueError("Device type '%s' not supported. "
                         "Supported devices are:%s" % (device_name, _SUPPORTED_DEVICES))


    metrics = get_metrics_names(device_name)

    if publisher_type == "pika":
        publishers = {metric: PikaPublisher(device_name,
                                            device_id,
                                            cloudbrain_address,
                                            metric) for metric in metrics}
    elif publisher_type == "pipe":
        publishers = {metric: PipePublisher(device_name,
                                            device_id,
                                            metric,
                                            pipe_name) for metric in metrics}
    else:
        raise ValueError("'%s' is not a valid publisher type. "
                         "Valid types are %s." % (publisher_type, "pika, pipe"))

    for publisher in publishers.values():
        publisher.connect()
    connector = Connector(publishers, buffer_size, step_size, device_name, device_port, device_mac)
    connector.connect_device()

    if mock_data_enabled and (publisher_type != 'pipe'):
        print "INFO: Mock data enabled."

    if publisher_type == 'pika':
        print ("SUCCESS: device '%s' connected with ID '%s'\n"
               "Sending data to cloudbrain at address '%s' ...") % (device_name,
                                                                    device_id,
                                                                    cloudbrain_address)
    connector.start()



if __name__ == "__main__":
    #run(device_name='openbci',
    #     mock_data_enabled=False,
    #     device_id='Will',
    #     device_port='/dev/tty.usbserial-DN0095VT')


    #run(device_name='openbci',
    #     mock_data_enabled=True,
    #     device_id='marion')

    main()
