from brisa.core.reactors._select import *
reactor = SelectReactor()
import os
from brisa.upnp.device import Device, Service
import dmx
import parallel

class LXDesk(Device):
  #TODO: are these the right way round?
  DMX_DOWN = 73
  DMX_UP   = 74
 
  #list of: off, dim, on
  LEVEL_UP_MAP   = [0, 100, 255]
  LEVEL_DOWN_MAR = [0, 0, 255]

  def __init__(self):
    Device.__init__(self, 'urn:schemas-icucinema-co-uk:device:LXDesk:1', 'LXDesk')

class Lighting(Service):
  def __init__(self):
    Service.__init__(self, 'Lighting', 'urn:schemas-icucinema-co-uk:service:Lighting:1',
        '', os.getcwd() + '/Lighting-scpd.xml')
    self.par = parallel.Parallel("LPTN")
    self.mn = dmx.ManolatorDmxController(self.par)
    self.mn.start()


if __name__ == "__main__":
  device = LXDesk()
  device += Lighting()

  device.start()
  reactor.add_after_stop_func(device.stop)
  reactor.main()
