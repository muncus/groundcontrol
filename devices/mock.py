import client

panel = client.ControlPanel('fakepanel')

if not panel.controls():
  # only create controls if we fail to load state.
  b = client.Toggle('foo')
  c = client.Counter('bar')
  w = client.Watcher('foo')
  panel.add_control(b)
  panel.add_control(c)
  panel.add_control(w)

panel.read_event_stream('http://localhost:8001/e')

def readinput():
  x = raw_input('waiting for input.')
  if x == 't':
    panel.notify('foo', 'toggle')
  if x == 'p':
    panel.notify('bar', 'inc')
  if x == 'P':
    panel.notify('bar', 'inc', 5)
  if x == 'm':
    panel.notify('bar', 'dec')
  if x == 's':
    print panel.dump_state()
  if x == 'q':
    panel.save_state()

def dumpstate():
  panel.dump_state()

panel.callbacks.append(readinput)
panel.run()
