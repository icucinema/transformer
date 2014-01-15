from brisa.core.reactors._select import *
reactor = SelectReactor()

from brisa.upnp.control_point import ControlPoint
from brisa.core.threaded_call import run_async_function

service = 'urn:schemas-upnp-org:service:Audio:1'
cp500_type = 'urn:schemas-upnp-org:device:CP500:1'

class CP500Controller(ControlPoint):
  def __init__(self):
    ControlPoint.__init__(self)

  def volmax(self, device):
    d = device.get_service_by_type(service)
    d.SetVolume(99)

  def volmin(self, device):
    d = device.get_service_by_type(service)
    d.SetVolume(0)

  def mute(self, device):
    d = device.get_service_by_type(service)
    d.SetMute(True)

  def unmute(self, device):
    d = device.get_service_by_type(service)
    d.SetMute(False)

  def main(self):
    commands = {'volmax': self.volmax,
                'volmin': self.volmin,
                'mute':   self.mute,
                'unmute': self.unmute}

    while True:
      input = raw_input('! ').strip()
      if input not in commands:
        print "?"
      else:
        commands[input]()

ctl = CP500Controller()
ctl.start()
ctl.start_search(2, cp500_type)
run_async_function(ctl.main)

reactor.add_after_stop_func(ctl.destroy)
reactor.main()
