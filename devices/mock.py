import client

panel = client.ControlPanel('fakepanel')

if not panel.controls():
  # only create controls if we fail to load state.
  b = client.Toggle('foo')
  c = client.Counter('bar')
  panel.add_control(b)
  panel.add_control(c)

print panel.dump_state()

while True:
  x = raw_input('waiting for input.')
  if x == 't':
    panel.get('foo').toggle()
  if x == 'p':
    panel.get('bar').inc()
  if x == 'm':
    panel.get('bar').dec()
  if x == 's':
    print panel.dump_state()
  if x == 'q':
    panel.save_state()
    break
