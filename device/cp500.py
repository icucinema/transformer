from brisa.core.reactors._select import *
reactor = SelectReactor()
import os
from brisa.upnp.device import Device, Service

class CP500(Device):
  def __init__(self):
    Device.__init__(self, 'urn:schemas-upnp-org:device:CP500:1', 'CP500')

class Audio(Service):
  def __init__(self):
    Service.__init__(self, 'Audio', 'urn:schemas-upnp-org:service:Audio:1',
        '', os.getcwd() + '/Audio-scpd.xml')
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
    self.volume = kwargs['NewSource']
    return {}

  def GetSource(self, *args, **kwargs):
    return {'CurrentSource': self.volume}

if __name__ == "__main__":
  device = CP500()
  device += Audio()

  device.start()
  reactor.add_after_stop_func(device.stop)
  reactor.main()
