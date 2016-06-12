import pika

from cloudbrain.subscribers import SubscriberInterface



class PikaSubscriber(SubscriberInterface):
  def __init__(self, rabbitmq_address, user, password):
    super(PikaSubscriber, self).__init__(rabbitmq_address)
    self.user = user
    self.password = password
    self.connection = None
    self.channels = {}


  def connect(self):
    credentials = pika.PlainCredentials(self.user, self.password)
    self.connection = pika.BlockingConnection(pika.ConnectionParameters(
      host=self.host, credentials=credentials))


  def register(self, routing_key):
    channel = self.connection.channel()
    channel.exchange_declare(exchange=routing_key,
                             type='direct')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=routing_key,
                       queue=queue_name,
                       routing_key=routing_key)

    self.channels[routing_key] = [channel, queue_name]


  def disconnect(self):
    for (routing_key, channel) in self.channels.items():
      channel[0].stop_consuming()
    self.connection.close()


  def subscribe(self, routing_key, callback):
    channel = self.channels[routing_key][0]
    queue_name = self.channels[routing_key][1]

    channel.basic_consume(callback,
                          queue=queue_name,
                          exclusive=True,
                          no_ack=True)

    channel.start_consuming()


  def get_one_message(self, routing_key):
    channel = self.channels[routing_key][0]
    queue_name = self.channels[routing_key][1]
    meth_frame, header_frame, body = channel.basic_get(queue_name)
    return (meth_frame, header_frame, body)
