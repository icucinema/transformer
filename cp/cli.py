from brisa.core.reactors._select import *
reactor = SelectReactor()

from brisa.upnp.control_point import ControlPoint
from brisa.core.threaded_call import run_async_function

def main():
  commands = {'vol':    cp500_ctl.setvol,
              'mute':   cp500_ctl.setmute,
              'source': cp500_ctl.setsource,
              'raise':  screen_ctl.up,
              'lower':  screen_ctl.down,
              'lights': lx_ctl.set}

  while True:
    i = raw_input('! ').strip().split(' ')
    if i[0] not in commands:
      if i[0] == "?":
        print ', '.join(list(commands.viewkeys()))
      else:
        print "?"
    else:
      if len(i) == 3:
        commands[i[0]](i[1], i[2])
      else:
        commands[i[0]](i[1])

class CP500Controller(ControlPoint):
  def __init__(self):
    ControlPoint.__init__(self)
    self.subscribe('new_device_event', self.device_found)
    self.service = 'urn:schemas-icucinema-co-uk:service:Audio:1'
    self.utype = 'urn:schemas-icucinema-co-uk:device:CP500:1'

  def device_found(self, dev):
    print "Found CP500"
    self.dev = dev

  def setvol(self, vol):
    s = self.dev.get_service_by_type(self.service)
    s.SetVolume(NewVolume=vol)

  def setmute(self, mute):
    d = self.dev.get_service_by_type(self.service)
    d.SetMute(ShouldMute=mute)

  def setsource(self, source):
    sourceName = {'cd' : 1, 'digital' : 3, 'pc': 4, '35mm' : 8}.get(source, None)
    if sourceName is None:
      return
    d = self.dev.get_service_by_type(self.service)
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

  def up(self):
    d = self.dev.get_service_by_type(self.service)
    d.RaiseScreen()

  def down(self):
    d = self.dev.get_service_by_type(self.service)
    d.LowerScreen()

class LXController(ControlPoint):
  def __init__(self):
    ControlPoint.__init__(self)
    self.subscribe('new_device_event', self.device_found)
    self.service = 'urn:schemas-icucinema-co-uk:service:Lighting:1'
    self.utype = 'urn:schemas-icucinema-co-uk:device:LXDesk:1'

  def device_found(self, dev):
    print "Found Lighting controller"
    self.dev = dev

  def set(self, up, down):
    d = self.dev.get_service_by_type(self.service)
    d.SetLevels(UpLevel=int(up), DownLevel=int(down))

cp500_ctl = CP500Controller()
cp500_ctl.start()
cp500_ctl.start_search(2, cp500_ctl.utype)
reactor.add_after_stop_func(cp500_ctl.destroy)

screen_ctl = ScreenController()
screen_ctl.start()
screen_ctl.start_search(2, screen_ctl.utype)
reactor.add_after_stop_func(screen_ctl.destroy)

lx_ctl = LXController()
lx_ctl.start()
lx_ctl.start_search(2, lx_ctl.utype)
reactor.add_after_stop_func(lx_ctl.destroy)

run_async_function(main)
reactor.main()
