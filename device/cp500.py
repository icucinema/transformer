from brisa.core.reactors._select import *
reactor = SelectReactor()
import os
from brisa.upnp.device import Device, Service
import serial

#TODO: Bother implementing volume + mute changing when actually necessary$

class CP500(Device):
  BTN_MAP =  {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 'Mute': 0xd}
  VOL_UP =   [0x1, 0x1]
  VOL_DOWN = [0x1, 0x0]
  HEADER =   [0x55, 0xaa]
  SEND =     [0]
  RECV =     [1]
  BTN_SEND = [0]
  BTN_RECV = [8]
  PKT_LEN =  6

  def __init__(self):
    Device.__init__(self, 'urn:schemas-icucinema-co-uk:device:CP500:1', 'CP500')

  @staticmethod
  def makeChecksum(packet):
    return [0xff - (sum(packet) % 0x100)]

  @staticmethod
  def makeChecksumPacket(packet):
    return packet + CP500.makeChecksum(packet)

  @staticmethod
  def makeButtonPacket(button):
    return CP500.makeChecksumPacket(CP500.HEADER + CP500.SEND + CP500.BTN_SEND + [CP500.BTN_MAP.get(button, 0xff)])

  @staticmethod
  def makeVolumeUpPacket():
    return CP500.makeChecksumPacket(CP500.HEADER + CP500.SEND + CP500.VOL_UP)

  @staticmethod
  def makeVolumeDownPacket():
    return CP500.makeChecksumPacket(CP500.HEADER + CP500.SEND + CP500.VOL_DOWN)

  @staticmethod
  def parseButtonRespPacket(packet):
    if packet[0,2] != HEADER:
      raise Exception("invalid header?")
    if packet[2,4] != [RECV, BTN_RECV]:
      raise Exception("not a receipt packet")
    if makeChecksum(packet[0,5]) != packet[5]:
      raise Exception("checksum mismatch")
    return packet[4] + 1 #TODO: handle mute button

class Audio(Service):
  def __init__(self):
    Service.__init__(self, 'Audio', 'urn:schemas-icucinema-co-uk:service:Audio:1',
        '', os.getcwd() + '/Audio-scpd.xml')

    self.serial = serial.Serial('/dev/ttyUSB0', 9600, timeout=5, bytesize=8, parity='N', stopbits=1)

    self.volume = 0
    self.mute = False
    self.source = 0

  def SetMute(self, *args, **kwargs):
    self.mute = kwargs['ShouldMute']
    return {}

  def GetMute(self, *args, **kwargs):
    return {'IsMuted': self.mute}

  def SetVolume(self, *args, **kwargs):
    self.volume = kwargs['NewVolume']
    return {}

  def GetVolume(self, *args, **kwargs):
    return {'CurrentVolume': self.volume}

  def SetSource(self, *args, **kwargs):
    self.source = int(kwargs['NewSource'])
    req = CP500.makeButtonPacket(self.source)
    import binascii
    self.serial.write(bytearray(req))
    resp = self.serial.read(CP500.PKT_LEN)
    return {}

  def GetSource(self, *args, **kwargs):
    return {'CurrentSource': self.source}

if __name__ == "__main__":
  device = CP500()
  device += Audio()

  device.start()
  reactor.add_after_stop_func(device.stop)
  reactor.main()
