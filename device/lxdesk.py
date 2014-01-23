from brisa.core.reactors._select import *
reactor = SelectReactor()
import os
from brisa.upnp.device import Device, Service

class LXDesk(Device):
  def __init__(self):
    Device.__init__(self, 'urn:schemas-icucinema-co-uk:device:LXDesk:1', 'LXDesk')

class Lighting(Service):
  def __init__(self):
    Service.__init__(self, 'Lighting', 'urn:schemas-icucinema-co-uk:service:Lighting:1',
        '', os.getcwd() + '/Lighting-scpd.xml')

if __name__ == "__main__":
  device = LXDesk()
  device += Lighting()

  device.start()
  reactor.add_after_stop_func(device.stop)
  reactor.main()
