from brisa.core.reactors._select import *
reactor = SelectReactor()

from brisa.upnp.control_point import ControlPoint
from brisa.core.threaded_call import run_async_function

def main(self):
  commands = {'vol':    cp500_ctl.setvol,
              'mute':   cp500_ctl.setmute,
              'source': cp500_ctl.setsource,
              'raise':  screen_ctl.up,
              'lower':  screen_ctl.down,}

  while True:
    i = raw_input('! ').strip().split(' ')
    if i[0] not in commands:
      print "?"
    else:
      commands[i[0]](self.dev, i[1])

class CP500Controller(ControlPoint):
  def __init__(self):
    ControlPoint.__init__(self)
    self.subscribe('new_device_event', self.device_found)
    self.service = 'urn:schemas-upnp-org:service:Audio:1'
    self.utype = 'urn:schemas-upnp-porg:device:CP500:1'

  def device_found(self, dev):
    print "Found CP500"
    self.dev = dev

  def setvol(self, device, vol):
    s = device.get_self.service_by_type(self.service)
    s.SetVolume(NewVolume=vol)

  def setmute(self, device, mute):
    d = device.get_self.service_by_type(self.service)
    d.SetMute(ShouldMute=mute)

  def setsource(self, device, source):
    sourceName = {'cd' : 1, 'digital' : 3, 'pc': 4, '35mm' : 8}.get(source, None)
    if sourceName is None:
      return
    d = device.get_self.service_by_type(self.service)
    d.SetSource(NewSource=sourceName)

class ScreenController(ControlPoint):
  def __init__(self):
    ControlPoint.__init__(self)
    self.subscribe('new_device_event', self.device_found)
    self.service = 'urn:schemas-icucinema-co-uk:service:RetractingScreen:1'
    self.utype = 'urn:schemas-icucinema-co-uk:device:RetractingScreen:1'

  def device_found(self, dev):
    print "Found Screen"
    self.dev = dev

  def up(self, device):
    d = device.get_service_by_type(self.service)
    d.RaiseScreen()

  def down(self, device):
    d = device.get_service_by_type(self.service)
    d.LowerScreen()

cp500_ctl = CP500Controller()
cp500_ctl.start()
cp500_ctl.start_search(2, cp500_ctl.utype)
reactor.add_after_stop_func(cp500_ctl.destroy)

screen_ctl = ScreenController()
screen_ctl.start()
screen_ctl.start_search(2, screen_ctl.utype)
reactor.add_after_stop_func(screen_ctl.destroy)

run_async_function(main)
reactor.main()
