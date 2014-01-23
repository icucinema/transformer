from brisa.core.reactors import install_default_reactor
reactor = install_default_reactor()

from brisa.upnp.control_point import ControlPoint
from brisa.core.threaded_call import run_async_function

def main():
  commands = {'volmax': cp500_ctl.volmax,
              'volmin': cp500_ctl.volmin,
              'mute':   cp500_ctl.mute,
              'unmute': cp500_ctl.unmute,
              'raise':  screen_ctl.up,
              'lower':  screen_ctl.down}

  while True:
    input = raw_input('! ').strip()
    if input[0] not in commands:
      print "?"
    else:
      commands[input]()

class CP500Controller(ControlPoint):
  def __init__(self):
    ControlPoint.__init__(self)
    self.service = 'urn:schemas-upnp-org:service:Audio:1'
    self.utype = 'urn:schemas-upnp-porg:device:CP500:1'

  def volmax(self, device):
    d = device.get_service_by_type(self.service)
    d.SetVolume(99)

  def volmin(self, device):
    d = device.get_service_by_type(self.service)
    d.SetVolume(0)

  def mute(self, device):
    d = device.get_service_by_type(self.service)
    d.SetMute(True)

  def unmute(self, device):
    d = device.get_service_by_type(self.service)
    d.SetMute(False)

class ScreenController(ControlPoint):
  def __init__(self):
    ControlPoint.__init__(self)
    self.service = 'urn:schemas-icucinema-co-uk:service:RetractingScreen:1'
    self.utype = 'urn:schemas-icucinema-co-uk:device:RetractingScreen:1'

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
