__author__ = 'marion'

import json


class EEGHeadset(object):
    def __init__(self, device_type):
        self.device = device_type

    def __str__(self):
        return json.dumps({'device': self.device})


class Muse(EEGHeadset):
    def __init__(self, path):
        super(Muse, self).__init__('muse')
        self.path = path

    def __str__(self):
        return json.dumps({'device': self.device,
                           'path': self.path})


class MuseAccelerometer(Muse):
    def __init__(self, acc_x, acc_y, acc_z, timestamp):
        """
        :param acc_x: double
        :param acc_y: double
        :param acc_z: double
        :param timestamp: long
        :return:
        """

        super(MuseAccelerometer, self).__init__('/muse/acc')
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.acc_z = acc_z
        self.timestamp = timestamp

    def __str__(self):
        return json.dumps({'path': self.path,
                           'acc_x': self.acc_x,
                           'acc_y': self.acc_y,
                           'acc_z': self.acc_z,
                           'timestamp': self.timestamp})

    def convert_for_batch(self):
        return {'path': self.path,
                'acc_x': str(self.acc_x),
                'acc_y': str(self.acc_y),
                'acc_z': str(self.acc_z),
                'timestamp': str(self.timestamp)}



class MuseConcentration(Muse):
    def __init__(self, concentration, timestamp):
        """
        :param concentration: double in between 0 and 1
        :param timestamp: long
        :return:
        """
        super(MuseConcentration, self).__init__('/muse/elements/experimental/concentration')
        self.concentration = concentration
        self.timestamp = timestamp

    def __str__(self):
        return json.dumps({'path': self.path,
                           'concentration': self.concentration,
                           'timestamp': self.timestamp})

    def convert_for_batch(self):
        return {'path': self.path,
                'concentration': str(self.concentration),
                'timestamp': str(self.timestamp)}


class MuseMellow(Muse):
    def __init__(self, mellow, timestamp):
        """
        :param mellow: double in between 0 and 1
        :param timestamp: long
        :return:
        """
        super(MuseMellow, self).__init__('/muse/elements/experimental/mellow')
        self.mellow = mellow
        self.timestamp = timestamp

    def __str__(self):
        return json.dumps({'path': self.path,
                           'mellow': self.mellow,
                           'timestamp': self.timestamp})

    def convert_for_batch(self):
        return {'path': self.path,
                'mellow': str(self.mellow),
                'timestamp': str(self.timestamp)}


if __name__ == '__main__':
    m = MuseAccelerometer(1, 2, 3, 1000)
    assert m.device == 'muse'
    assert m.path == '/muse/acc'
    assert m.acc_x == 1
    assert m.acc_y == 2
    assert m.acc_z == 3
    assert m.timestamp == 1000

    m = MuseConcentration(1, 1000)
    assert m.device == 'muse'
    assert m.path == '/muse/elements/experimental/concentration'
    assert m.concentration == 1
    assert m.timestamp == 1000

    m = MuseMellow(1, 1000)
    assert m.device == 'muse'
    assert m.path == '/muse/elements/experimental/mellow'
    assert m.mellow == 1
    assert m.timestamp == 1000