from brisa.core.reactors._select import *
reactor = SelectReactor()

from brisa.upnp.control_point import ControlPoint
from brisa.core.threaded_call import run_async_function

service = 'urn:schemas-upnp-org:service:Audio:1'
cp500_type = 'urn:schemas-upnp-org:device:CP500:1'

class CP500Controller(ControlPoint):
  def __init__(self):
    ControlPoint.__init__(self)
    self.subscribe('new_device_event', self.device_found)

  def device_found(self, dev):
    print "Found CP500"
    self.dev = dev

  def setvol(self, device, vol):
    s = device.get_service_by_type(service)
    s.SetVolume(NewVolume=vol)

  def setmute(self, device, mute):
    d = device.get_service_by_type(service)
    d.SetMute(ShouldMute=mute)

  def setsource(self, device, source):
    sourceName = {'mono' : 0, 'sr' : 2, 'digital': 3, '70mm' : 5}.get(source, None)
    if sourceName is None:
      return
    d = device.get_service_by_type(service)
    d.SetSource(NewSource=sourceName)

  def main(self):
    commands = {'vol': self.setvol,
                'mute': self.setmute,
                'source': self.setsource,}

    while True:
      i = raw_input('! ').strip().split(' ')
      if i[0] not in commands:
        print "?"
      else:
        commands[i[0]](self.dev, i[1])

ctl = CP500Controller()
ctl.start()
ctl.start_search(2, cp500_type)
run_async_function(ctl.main)

reactor.add_after_stop_func(ctl.destroy)
reactor.main()
