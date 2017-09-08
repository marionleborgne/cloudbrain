# -*- coding: utf-8 -*-

# Copyright Puzzlebox Productions, LLC (2010-2016)
#
# Ported from Puzzlebox Synapse
# ThinkGear code imported from Puzzlebox.Synapse.ThinkGear.Protocol
# http://puzzlebox.io
#
# This code is released under the GNU Pulic License (GPL) version 3
# For more information please refer to http://www.gnu.org/copyleft/gpl.html
#
# Author: Steve Castellotti <sc@puzzlebox.io>


__changelog__ = """
Last Update: 2016.02.02
"""

__todo__ = """

 - When a "MindSet" is configured as "MindWave" hardware:
   File "~/development/jigsaw/trunk/Puzzlebox/Synapse/Protocol.py", line 868, 
   in run self.device.device.write('\xc1')

 - needs to handle:
   serial.serialutil.SerialException:
   could not open port /dev/rfcomm0:
   [Errno 16] Device or resource busy: '/dev/rfcomm0'
"""

__doc__ = """
Puzzlebox.Synapse.Protocol

usage:
  from Puzzlebox.Synapse import Protocol

Modules:
  Protocol.ProtocolHandler()
  Protocol.SerialDevice()

SPEC:

 CODE Definitions Table
 Single-Byte CODEs
 Extended             (Byte)
 Code Level   [CODE] [LENGTH] Data Value Meaning
 ----------   ------ -------- ------------------
           0    0x02        - POOR_SIGNAL Quality (0-255)
           0    0x04        - ATTENTION eSense (0 to 100)
           0    0x05        - MEDITATION eSense (0 to 100)
           0    0x16        - Blink Strength. (0-255) Sent only
                              when Blink event occurs.
 Multi-Byte CODEs
 Extended             (Byte)
 Code Level   [CODE] [LENGTH] Data Value Meaning
 ----------   ------ -------- ------------------
           0    0x80        2 RAW Wave Value: a single big-endian
                                16-bit two's-compliment signed value
                                (high-order byte followed by
                                low-order byte) (-32768 to 32767)
           0    0x83       24 ASIC_EEG_POWER: eight big-endian
                                3-byte unsigned integer values
                                representing delta, theta, low-alpha
                                high-alpha, low-beta, high-beta,
                                low-gamma, and mid-gamma EEG band
                                power values
         Any    0x55        - NEVER USED (reserved for [EXCODE])
         Any    0xAA        - NEVER USED (reserved for [SYNC])

MindWave Connection CODEs
[CODE] [DATA]    Data Value Meaning
------ --------- ------------
 0xC0  0xAB 0xCD Connect to headset with ID "ABCD"
 0xC1          - Disconnect
 0xC2          - Connect to first available headset

MindWave Response CODEs
Extended             (Byte)
Code Level   [CODE] [LENGTH] Data Value Meaning
----------   ------ -------- ------------------
         0    0xD0        3 Headset Connect Success
         0    0xD1        2 Headset Not Found
         0    0xD2        3 Headset Disconnected
         0    0xD3        0 Request Denied
         0    0xD4        1 Standby/Scan Mode

Linux Bluetooth serial protocol profile example:
    rfcomm connect rfcomm0 00:13:EF:00:1B:FE 3
"""

import sys, time
import serial
import copy
import threading

if sys.platform != 'win32' and sys.platform != 'darwin':
    import bluetooth


class Configuration():
    def __init__(self):

        # Ported from Puzzlebox.Synapse.Configuration

        self.DEBUG = 1

        self.DEFAULT_THINKGEAR_DEVICE_SERIAL_PORT_WINDOWS = 'COM2'
        self.DEFAULT_THINKGEAR_DEVICE_SERIAL_PORT_LINUX = '/dev/rfcomm0'

        if sys.platform == 'win32':
            self.THINKGEAR_DEVICE_SERIAL_PORT = \
                self.DEFAULT_THINKGEAR_DEVICE_SERIAL_PORT_WINDOWS
        else:
            self.THINKGEAR_DEVICE_SERIAL_PORT = \
                self.DEFAULT_THINKGEAR_DEVICE_SERIAL_PORT_LINUX

        self.THINKGEAR_EEG_POWER_BAND_ORDER = ['delta',
                                               'theta',
                                               'lowAlpha',
                                               'highAlpha',
                                               'lowBeta',
                                               'highBeta',
                                               'lowGamma',
                                               'highGamma']


# import Puzzlebox.Synapse.Configuration as configuration
configuration = Configuration()

DEBUG = configuration.DEBUG

THINKGEAR_DEVICE_SERIAL_PORT = configuration.THINKGEAR_DEVICE_SERIAL_PORT
DEFAULT_SERIAL_BAUDRATE = 115200

THINKGEAR_DEVICE_BLUETOOTH_CHANNEL = 3

THINKGEAR_DEVICE_AUTOCONNECT_INTERVAL = 4  # seconds between attempting
# to send auto-connect packets
# THINKGEAR_DEVICE_ID = configuration.THINKGEAR_DEVICE_ID
# THINKGEAR_DEFAULT_DEVICE_ID = '\x7d\x68'
# THINKGEAR_DEFAULT_DEVICE_ID = '\xe4\x68'

PROTOCOL_SYNC = '\xAA'
PROTOCOL_EXCODE = '\x55'

EEG_POWER_BAND_ORDER = configuration.THINKGEAR_EEG_POWER_BAND_ORDER

DEVICE_BUFFER_CHECK_TIMER = 60 * 1000  # Check buffer size once every minute
DEVICE_READ_BUFFER_CHECK_TIMER = 10 * 1000  # Check buffer size once x seconds
DEVICE_BUFFER_MAX_SIZE = 180  # Reset buffer if it grow this large
# as this would indicate the processing
# algorithm is not keeping up with the device
# According to protocol specification,
# "...a complete, valid Packet is ... a maximum
# of 173 bytes long (possible if the Data Payload
# is the maximum 169 bytes long)."
# Therefore we reset if our buffer has grown longer
# than the maximum packet length as this means
# the processing algorthim is at least one full
# packet behind.

DEBUG_BYTE_COUNT = 819200
DEBUG_PACKET_COUNT = 1024


class puzzlebox_synapse_protocol_thinkgear(threading.Thread):
    def __init__(self, log,
                 serial_device,
                 device_model='NeuroSky MindWave',
                 DEBUG=DEBUG,
                 parent=None):

        # QtCore.QThread.__init__(self,parent)
        # threading.Thread.__init__ (self,parent)
        threading.Thread.__init__(self)

        self.log = log
        self.DEBUG = DEBUG
        self.parent = parent

        # self.device_id = device_id
        self.device_model = device_model

        self.device = None
        self.buffer = ''
        # self.payload_timestamp = time.time()
        self.payload_timestamp = int(time.time() * 1000000)

        self.device = serial_device
        # self.auto_connect_timestamp = time.time()
        self.auto_connect_timestamp = int(time.time() * 1000000)

        self.data_packet = {}
        self.data_packet['eegPower'] = {}
        self.data_packet['eSense'] = {}

        self.current_signal = 200
        self.current_attention = 0
        self.current_meditation = 0
        self.detection_threshold = 70
        self.current_detection = 0

        self.keep_running = True

    def hexStringEndianSwap(self, theString):
        """Rearranges character-couples in a little endian hex string to
        convert it into a big endian hex string and vice-versa. i.e. 'A3F2'
        is converted to 'F2A3'

        @param theString: The string to swap character-couples in
        @return: A hex string with swapped character-couples. -1 on error.

        Taken from:
         http://bytes.com/topic/python/answers/
         652429-convert-little-endian-hex-string-number#post2588668"""

        # We can't swap character couples in a string that has an odd number
        # of characters.
        if len(theString) % 2 != 0:
            return -1

        # Swap the couples
        swapList = []
        for i in range(0, len(theString), 2):
            swapList.insert(0, theString[i:i + 2])

        # Combine everything into one string. Don't use a delimeter.
        return ''.join(swapList)

    def processRawEEGValue(self, data_values):

        """SPEC: This Data Value consists of two bytes, and represents a
        single raw wave sample. Its value is a signed 16-bit integer that
        ranges from -32768 to 32767. The first byte of the Value represents
        the high-order bits of the twos-compliment value, while the second
        byte represents the low-order bits. To reconstruct the full raw
        wave value, simply shift the rst byte left by 8 bits, and
        bitwise-or with the second byte:

        short raw = (Value[0]<<8) | Value[1];

        where Value[0] is the high-order byte, and Value[1] is the
        low-order byte. In systems or languages where bit operations are
        inconvenient, the following arithmetic operations may be
        substituted instead:

        raw = Value[0]*256 + Value[1];
        if( raw >= 32768 ) raw = raw - 65536;

        where raw is of any signed number type in the language that can
        represent all the numbers from -32768 to 32767.

        Each ThinkGear model reports its raw wave information in only
        certain areas of the full -32768 to 32767 range. For example,
        MindSet reports raw waves that fall between approximately -2048 to
        2047. By default, output of this Data Value is enabled, and is
        outputed 512 times a second, or approximately once every 2ms."""

        high_order = data_values[0:2]
        low_order = data_values[2:4]

        # high_order = high_order.encode("hex")
        high_order = int(high_order, 16)

        # low_order = low_order.encode("hex")
        low_order = int(low_order, 16)

        raw = high_order * 256 + low_order

        if raw >= 32768:
            raw = raw - 65536

        return (raw)

    def processAsicEegPower(self, data_values):

        """SPEC: This Data Value represents the current magnitude of 8
        commonly-recognized types of EEG (brain-waves). This Data Value
        is output as a series of eight 3-byte unsigned integers in
        little-endian format.
        The eight EEG powers are output in the following order:
        delta (0.5 - 2.75Hz),
        theta (3.5 - 6.75Hz),
        low-alpha (7.5 - 9.25Hz),
        high-alpha (10 - 11.75Hz),
        low-beta (13 - 16.75Hz),
        high-beta (18 - 29.75Hz),
        low-gamma (31 - 39.75Hz), and
        mid-gamma (41 - 49.75Hz).
        These values have no units and therefore are only meaningful compared
        to each other and to themselves, to consider relative quantity and
        temporal uctuations. By default, output of this Data Value is enabled,
        and is typically output once a second."""

        eegPower = {}

        eegPower['delta'] = data_values[0:6]
        eegPower['theta'] = data_values[6:12]
        eegPower['lowAlpha'] = data_values[12:18]
        eegPower['highAlpha'] = data_values[18:24]
        eegPower['lowBeta'] = data_values[24:30]
        eegPower['highBeta'] = data_values[30:36]
        eegPower['lowGamma'] = data_values[36:42]
        eegPower['highGamma'] = data_values[42:48]

        for key in eegPower.keys():
            eegPower[key] = self.hexStringEndianSwap(eegPower[key])
            eegPower[key] = int(eegPower[key], 16)

        return (eegPower)

    def processDataRow(self,
                       extended_code_level,
                       code,
                       length,
                       data_values,
                       timestamp):

        '''CODE Definitions Table
           Single-Byte CODEs
           Extended             (Byte)
           Code Level   [CODE] [LENGTH] Data Value Meaning
           ----------   ------ -------- ------------------
                     0    0x02        - POOR_SIGNAL Quality (0-255)
                     0    0x04        - ATTENTION eSense (0 to 100)
                     0    0x05        - MEDITATION eSense (0 to 100)
                     0    0x16        - Blink Strength. (0-255) Sent only
                                        when Blink event occurs.
           Multi-Byte CODEs
           Extended             (Byte)
           Code Level   [CODE] [LENGTH] Data Value Meaning
           ----------   ------ -------- ------------------
                     0    0x80        2 RAW Wave Value: a single big-endian
                                          16-bit two's-compliment signed value
                                          (high-order byte followed by
                                          low-order byte) (-32768 to 32767)
                     0    0x83       24 ASIC_EEG_POWER: eight big-endian
                                          3-byte unsigned integer values
                                          representing delta, theta, low-alpha
                                          high-alpha, low-beta, high-beta,
                                          low-gamma, and mid-gamma EEG band
                                          power values
                   Any    0x55        - NEVER USED (reserved for [EXCODE])
                   Any    0xAA        - NEVER USED (reserved for [SYNC])

           MindWave CODEs
           Extended             (Byte)
           Code Level   [CODE] [LENGTH] Data Value Meaning
           ----------   ------ -------- ------------------
                     0    0xD0        3 Headset Connect Success
                     0    0xD1        2 Headset Not Found
                     0    0xD2        3 Headset Disconnected
                     0    0xD3        0 Request Denied
                     0    0xD4        1 Standby/Scan Mode'''

        packet_update = {}

        packet_update['timestamp'] = timestamp

        self.parent.incrementPacketCount()

        if extended_code_level == 0:

            if code == '02':
                poor_signal_quality = int(data_values, 16)
                if self.DEBUG > 1:
                    print() # Empty line at the beginning of most packets
                    print("poorSignalLevel: %s" % poor_signal_quality)

                self.current_signal = copy.copy(poor_signal_quality)

                packet_update['poorSignalLevel'] = poor_signal_quality

                self.current_signal = poor_signal_quality

            elif code == '04':
                attention = int(data_values, 16)
                if self.DEBUG > 1:
                    print("attention: %s" % attention)

                self.current_attention = copy.copy(attention)

                if (attention > self.detection_threshold):
                    self.current_detection = 1
                else:
                    self.current_detection = 0

                packet_update['eSense'] = {}
                packet_update['eSense']['attention'] = attention

            elif code == '05':
                meditation = int(data_values, 16)
                if self.DEBUG > 1:
                    print("meditation: %s" % meditation)

                self.current_meditation = copy.copy(meditation)

                packet_update['eSense'] = {}
                packet_update['eSense']['meditation'] = meditation

            elif code == '16':
                blink_strength = int(data_values, 16)
                if self.DEBUG > 1:
                    print("blinkStrength: %s" % blink_strength)

                packet_update['blinkStrength'] = blink_strength

            elif code == '80':
                raw_wave_value = data_values
                if self.DEBUG > 3:
                    print("Raw EEG: %s" % raw_wave_value)
                raw_eeg_value = self.processRawEEGValue(data_values)
                if self.DEBUG > 2:
                    print("Raw EEG Value: %s" % raw_eeg_value)

                packet_update['rawEeg'] = raw_eeg_value

            elif code == '83':
                asic_eeg_power = data_values
                if self.DEBUG > 2:
                    print("ASIC_EEG_POWER: %s" % asic_eeg_power)
                eegPower = self.processAsicEegPower(data_values)
                if self.DEBUG > 1:
                    for key in EEG_POWER_BAND_ORDER:
                        print("%s: %i" % (key, eegPower[key]))

                packet_update['eegPower'] = {}
                for key in eegPower.keys():
                    packet_update['eegPower'][key] = eegPower[key]

            elif code == 'd0':
                if self.DEBUG:
                    print("INFO: ThinkGear Headset Connect Success")
                self.parent.resetSessionStartTime()
                self.parent.setPacketCount(0)
                self.parent.setBadPackets(0)

            elif code == 'd1':
                current_time = int(time.time() * 1000000)
                if (current_time - self.auto_connect_timestamp >
                        THINKGEAR_DEVICE_AUTOCONNECT_INTERVAL):
                    if self.DEBUG:
                        print("INFO: ThinkGear device not found. "
                              "Writing auto-connect packet.")
                    self.auto_connect_timestamp = current_time
                    self.device.device.write('\xc2')

            elif code == 'd2':
                current_time = int(time.time() * 1000000)
                if (current_time - self.auto_connect_timestamp >
                        THINKGEAR_DEVICE_AUTOCONNECT_INTERVAL):
                    if self.DEBUG:
                        print("INFO: ThinkGear device disconnected. "
                              "Writing auto-connect packet.")
                    self.auto_connect_timestamp = current_time
                    self.device.device.write('\xc2')

            elif code == 'd3':
                current_time = int(time.time() * 1000000)
                if (current_time - self.auto_connect_timestamp >
                        THINKGEAR_DEVICE_AUTOCONNECT_INTERVAL):
                    if self.DEBUG:
                        print("INFO: ThinkGear device request denied. "
                              "Writing auto-connect packet.")
                    self.auto_connect_timestamp = current_time
                    self.device.device.write('\xc2')


            elif code == 'd4':
                current_time = int(time.time() * 1000000)
                if (current_time - self.auto_connect_timestamp >
                        THINKGEAR_DEVICE_AUTOCONNECT_INTERVAL):
                    if self.DEBUG:
                        print("INFO: ThinkGear device in standby/scan mode. "
                              "Writing auto-connect packet.")
                    self.auto_connect_timestamp = current_time
                    self.device.device.write('\xc2')

            else:
                self.parent.incrementBadPackets()
                if self.DEBUG:
                    print("ERROR: data payload row code not matched: %s" % code)

        return (packet_update)

    def processDataPayload(self, data_payload, timestamp):

        """A DataRow consists of bytes in the following format:
        ([EXCODE]...) [CODE] ([VLENGTH])   [VALUE...]
        ____________________ ____________ ___________
        ^^^^(Value Type)^^^^ ^^(length)^^ ^^(value)^^"""

        if self.DEBUG > 3:
            print("data payload:")
            for byte in data_payload:
                print(byte.encode("hex"))
            print()

        byte_index = 0

        # Parse the extended_code_level, code, and length
        while (byte_index < len(data_payload)):
            extended_code_level = 0

            # 1. Parse and count the number of [EXCODE] (0x55)
            #    bytes that may be at the beginning of the
            #    current DataRow.
            while (data_payload[byte_index] == PROTOCOL_EXCODE):
                extended_code_level += 1
                byte_index += 1

            # 2. Parse the [CODE] byte for the current DataRow.
            code = data_payload[byte_index]
            byte_index += 1
            code = code.encode("hex")

            # 3. If [CODE] >= 0x80, parse the next byte as the
            #    [VLENGTH] byte for the current DataRow.
            if (code > '\x7f'.encode("hex")):
                length = data_payload[byte_index]
                byte_index += 1
                length = length.encode("hex")
                length = int(length, 16)
            else:
                length = 1

            if self.DEBUG > 3:
                print("EXCODE level: %s" % extended_code_level)
                print(" CODE: %s" % code)
                print(" length: %s" % length)

            data_values = ''
            value_index = 0

            # 4. Parse and handle the [VALUE...] byte(s) of the current
            #    DataRow, based on the DataRow's [EXCODE] level, [CODE],
            #    and [VLENGTH] (refer to the Code De nitions Table).
            while value_index < length:
                # Uh-oh more C mojo
                try:
                    value = data_payload[(byte_index + value_index)]  # & 0xFF
                except:
                    if self.DEBUG:
                        print("ERROR: failed to parse and handle the "
                               "[VALUE...] bytes of the current DataRow")
                    break
                data_values += value.encode("hex")
                value_index += 1

            if self.DEBUG > 3:
                print("Data Values: %s\n" % data_values)

            packet_update = self.processDataRow(extended_code_level,
                                                code,
                                                length,
                                                data_values,
                                                timestamp)

            self.updateDataPacket(packet_update)

            byte_index += length

            # 5. If not all bytes have been parsed from the payload[] array,
            # return to step 1. to continue parsing the next DataRow.

    def parseStream(self):

        """Each Packet begins with its Header, followed by its Data Payload,
        and ends with the Payload's Check-sum Byte, as follows:
        [SYNC] [SYNC] [PLENGTH]      [PAYLOAD...]         [CHKSUM]
        _______________________      _____________     ____________
        ^^^^^^^^(Header)^^^^^^^      ^^(Payload)^^     ^(Checksum)^"""

        # Loop forever, parsing one Packet per loop...
        # packet_count = 0
        self.parent.setPacketCount(0)

        while self.keep_running:

            # Synchronize on [SYNC] bytes
            # Read from stream until two consecutive [SYNC] bytes are found
            byte = self.device.read()

            if (byte != PROTOCOL_SYNC):
                continue

            byte = self.device.read()
            if (byte != PROTOCOL_SYNC):
                continue

            self.payload_timestamp = int(time.time() * 1000000)

            # Parse [PLENGTH] byte

            # SPEC: [PLENGTH] byte indicates the length, in bytes, of the
            # Packet's Data Payload [PAYLOAD...] section, and may be any value
            # from 0 up to 169. Any higher value indicates an error
            # (PLENGTH TOO LARGE). Be sure to note that [PLENGTH] is the length
            # of the Packet's Data Payload, NOT of the entire Packet.
            # The Packet's complete length will always be [PLENGTH] + 4.

            byte = self.device.read()
            packet_length = byte.encode("hex")
            packet_length = int(packet_length, 16)

            if (packet_length > 170):
                self.parent.incrementBadPackets()
                if self.DEBUG:
                    print("ERROR: packet length bad")
                    continue

            # Collect [PAYLOAD...] bytes
            data_payload = self.device.read(packet_length)

            # Calculate [PAYLOAD...] checksum

            # SPEC: The [CHKSUM] Byte must be used to verify the integrity of
            # the packet's Data Payload. The Payload's Checksum is defined as:
            #  1. summing all the bytes of the Packet's Data Payload
            #  2. taking the lowest 8 bits of the sum
            #  3. performing the bit inverse (one's compliment inverse)
            #     on those lowest 8 bits

            payload_checksum = 0
            for byte in data_payload:
                value = byte.encode("hex")
                value = int(value, 16)
                payload_checksum += value

            # Take the lowest 8 bits of the calculated payload_checksum
            # and invert them. Serious C code mojo follows.
            payload_checksum &= 0xff
            payload_checksum = ~payload_checksum & 0xff

            # Parse [CKSUM] byte
            packet_checksum = self.device.read()
            packet_checksum = packet_checksum.encode("hex")
            packet_checksum = int(packet_checksum, 16)

            # Verify [CKSUM] byte against calculated [PAYLOAD...] checksum
            if packet_checksum != payload_checksum:
                self.parent.incrementBadPackets()

                if self.DEBUG > 1:
                    print("ERROR: packet checksum does not match")
                    print("       packet_checksum: %s" %  packet_checksum)
                    print("       payload_checksum: %s" % payload_checksum)

                continue


            else:
                # Since [CKSUM] is OK, parse the Data Payload
                if self.DEBUG > 3:
                    print("packet checksum correct")

                self.processDataPayload(data_payload, self.payload_timestamp)

    def updateDataPacket(self, packet_update):

        if 'eSense' in packet_update.keys():
            process_packet = {'eSense': {}}
            for key in packet_update['eSense'].keys():
                self.data_packet['eSense'][key] = packet_update['eSense'][key]
                process_packet['eSense'][key] = packet_update['eSense'][key]

        else:
            self.data_packet.update(packet_update)
            process_packet = packet_update

        process_packet['timestamp'] = packet_update['timestamp']

        if self.DEBUG > 3:
            print(self.data_packet)

        if self.parent is not None:
            # NOTE: is it possible this call is blocking the Protocol
            #       thread from continuing to parse data?

            self.parent.processPacketThinkGear(process_packet)

    def disconnectHardware(self):

        if self.device is not None and self.device.device is not None:
            if self.device_model == 'NeuroSky MindWave':
                if self.DEBUG:
                    print("INFO: ThinkGear device model MindWave selected. "
                           "Writing disconnect packet.")
                try:
                    self.device.device.write('\xc1')
                except Exception, e:
                    if self.DEBUG:
                        print("ERROR: failed to write disconnect packet: %s" %e)

    def resetSessionStartTime(self):

        if self.parent is not None:
            self.parent.resetSessionStartTime()

    def resetSession(self):

        self.parent.setPacketCount(0)
        self.parent.setBadPackets(0)
        self.parent.resetSessionStartTime()

    def run(self):

        try:
            self.resetSession()
        except Exception, e:
            if self.DEBUG:
                print("ERROR: self.resetSession(): %s" % e)

        if self.device is not None and self.device.device is not None:
            if self.device_model == 'NeuroSky MindWave':
                if self.DEBUG:
                    print("INFO: ThinkGear device model MindWave selected. "
                           "Writing disconnect packet.")
                self.device.device.write('\xc1')
                if self.DEBUG:
                    print("INFO: ThinkGear device model MindWave selected. "
                           "Writing auto-connect packet.")
                self.device.device.write('\xc2')
            else:
                if self.device_model != None and self.DEBUG:
                    print("INFO: %s device model selected" % self.device_model)

            self.parseStream()

    def exitThread(self, callThreadQuit=True):

        self.disconnectHardware()

        try:
            self.device.stop()
        except:
            pass

        if callThreadQuit:
            if self.DEBUG:
                print("self.join()")
            self.join()


class SerialDevice(threading.Thread):
    def __init__(self, log,
                 device_address=THINKGEAR_DEVICE_SERIAL_PORT,
                 DEBUG=DEBUG,
                 parent=None):

        threading.Thread.__init__(self)

        self.log = log
        self.DEBUG = DEBUG
        self.parent = parent

        self.device_address = device_address
        self.device = None
        self.buffer = ''

        if self.device_address.count(':') == 5:
            # Device address is a Bluetooth MAC address
            if self.DEBUG:
                print("INFO: Initializing Bluetooth Device: %s"
                      % self.device_address)
            self.device = self.initializeBluetoothDevice()
        else:
            # Device address is a serial port address
            if self.DEBUG:
                print("INFO: Initializing Serial Device: %s"
                      % self.device_address)
            self.device = self.initializeSerialDevice()

        self.keep_running = True

    def initializeBluetoothDevice(self):

        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        try:
            socket.connect(
                (self.device_address, THINKGEAR_DEVICE_BLUETOOTH_CHANNEL))

        except Exception, e:
            if self.DEBUG:
                print("ERROR: %s" % e)
                sys.exit()

        return socket

    def initializeSerialDevice(self):

        device = None

        baudrate = DEFAULT_SERIAL_BAUDRATE
        bytesize = 8
        parity = 'NONE'
        stopbits = 1
        software_flow_control = 'f'
        rts_cts_flow_control = 'f'
        timeout = 5

        # convert bytesize
        if bytesize == 5:
            init_byte_size = serial.FIVEBITS
        elif bytesize == 6:
            init_byte_size = serial.SIXBITS
        elif bytesize == 7:
            init_byte_size = serial.SEVENBITS
        elif bytesize == 8:
            init_byte_size = serial.EIGHTBITS
        else:
            init_byte_size = serial.EIGHTBITS

        # convert parity
        if parity == 'NONE':
            init_parity = serial.PARITY_NONE
        elif parity == 'EVEN':
            init_parity = serial.PARITY_EVEN
        elif parity == 'ODD':
            init_parity = serial.PARITY_ODD
        else:
            init_parity = serial.PARITY_NONE

        # convert stopbits
        if stopbits == 1:
            init_stopbits = serial.STOPBITS_ONE
        elif stopbits == 2:
            init_stopbits = serial.STOPBITS_TWO
        else:
            init_byte_size = serial.STOPBITS_ONE

        # convert software flow control
        if software_flow_control == 't':
            init_software_flow_control = 1
        else:
            init_software_flow_control = 0

        # convert rts cts flow control
        if rts_cts_flow_control == 't':
            init_rts_cts_flow_control = 1
        else:
            init_rts_cts_flow_control = 0

        try:
            device = SerialWrapper(port=self.device_address,
                                   baudrate=baudrate,
                                   bytesize=init_byte_size,
                                   parity=init_parity,
                                   stopbits=init_stopbits,
                                   xonxoff=init_software_flow_control,
                                   rtscts=init_rts_cts_flow_control,
                                   timeout=timeout)

            device.flushInput()

        except Exception, e:
            if self.DEBUG:
                print("ERROR: %s" % e)
                print(self.device_address)
                return (None)
        return (device)

    def checkBuffer(self):

        if self.DEBUG > 1:
            print("INFO: Buffer size check: %s" % len(self.buffer),)
            print("(maximum before reset is %i)" % DEVICE_BUFFER_MAX_SIZE)

        if DEVICE_BUFFER_MAX_SIZE <= len(self.buffer):

            if self.DEBUG:
                print("ERROR: Buffer size has grown too large, resetting")

            self.reset()

    def checkReadBuffer(self):

        if self.DEBUG > 1:
            print("INFO: Read buffer timer check")

        current_time = int(time.time() * 1000000)

        if self.parent is not None and self.parent.protocol is not None:

            if (current_time - self.parent.protocol.payload_timestamp >
                    DEVICE_BUFFER_CHECK_TIMER):

                if self.DEBUG:
                    print("ERROR: Read buffer timer has expired, "
                           "resetting connection")

            self.parent.resetDevice()

    def reset(self):

        self.buffer = ''

    def read(self, length=1):

        # Sleep for 2 ms if buffer is empty
        # Based on 512 Hz refresh rate of NeuroSky MindSet device
        # (1/512) * 1000 = 1.9531250
        while len(self.buffer) < length:
            try:
                time.sleep(0.002)
            except Exception, e:
                pass

        bytes = self.buffer[:length]

        self.buffer = self.buffer[length:]

        return (bytes)

    def stop(self):

        self.keep_running = False
        try:
            self.buffer_check_timer.stop()
        except Exception, e:
            if self.DEBUG:
                print("ERROR: Protocol failed to call "
                       "self.buffer_check_timer.stop() in stop() %s" % e)

        try:
            self.read_buffer_check_timer.stop()
        except Exception, e:
            if self.DEBUG:
                print("ERROR: Protocol failed to call "
                       "self.read_buffer_check_timer.stop() in stop(): %s" % e)

        self.buffer = ''

    def exitThread(self, call_thread_quit=True):

        self.stop()
        self.close()

        if call_thread_quit:
            try:
                if self.DEBUG:
                    print("self.join()")
                self.join()
            except Exception, e:
                if self.DEBUG:
                    print("ERROR: Protocol failed to call "
                           "self.join() in exitThread(): %s" % e)

    def close(self):

        if self.device is not None:

            try:
                self.device.close()
            except Exception, e:
                pass

    def run(self):

        if self.device is None:
            self.keep_running = False

        self.buffer = ''

        while self.keep_running:

            try:
                byte = self.device.recv(1)

                if len(byte) != 0:
                    if self.DEBUG > 2:
                        print("Device read: %s" % byte)

                    self.buffer += byte

            except Exception, e:
                if self.DEBUG:
                    print("ERROR: failed to read from serial device: %s" % e)
                break

        self.exitThread()


class SerialWrapper(serial.Serial):
    def recv(self, size=1):
        return self.read(size)
