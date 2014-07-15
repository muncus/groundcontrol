# Common library of basic building blocks for physical interfaces
# originally intended for use with a Raspberry Pi.
# Author: Marc Dougherty <muncus@gmail.com>

import logging
import json
import requests

BASE_URL = 'http://localhost:9292/devices'

class Watcher(object):
  """Base class for controls which respond to state changes."""
  pass

class Actuator(object):
  """ Base class for controls that are manipulated."""

  def __init__(self, name):
    self.name = name

  def send_event(self, event):
    self.parent.send_event(self, event)

  def set_value(self, value):
    """Subclasses must implement this to store value."""
    raise NotImplemented
#alias.
Control = Actuator


class Toggle(Actuator):
  def __init__(self, name, initial_value=False):
    super(Toggle, self).__init__(name)
    self.value = initial_value

  def toggle(self):
    self.value = not self.value
    self.send_event({'value': int(self.value)})

  def set_value(self, value):
    self.value = value['value']

  def as_dict(self):
    return {'type': 'toggle',
            'name': self.name,
            'value': self.value}

  @staticmethod
  def from_json(json):
    x = Toggle(json['name'])
    x.value = json['value']
    return x

class Counter(Actuator):
  def __init__(self, name, initial_value=0):
    super(Counter, self).__init__(name)
    self.value = initial_value

  def set_value(self, value):
    self.value = value['value']

  def inc(self, step=1):
    self.value += step
    self.send_event({'value': self.value})

  def dec(self, step=1):
    self.value -= step
    self.send_event({'value': self.value})

  def as_dict(self):
    return {'type': 'counter',
            'name': self.name,
            'value': self.value}

  @staticmethod
  def from_json(json):
    x = Toggle(json['name'])
    x.value = json['value']
    return x


class ControlPanel(object):
  """Base class for physical interfaces. May contain Actuators and Indicators."""

  # Map json type name to object class.
  type_map = {
    'toggle': Toggle,
    'counter': Counter,
  }

  def __init__(self, name, service_url=BASE_URL):
    self.service_url = service_url
    self.name = name
    self.etag = None # cloudkit requirement.
    self.child_map =  {}
    try:
      self.fetch_state()
    except Exception as e:
      print  e
      print "could not fetch state for %s" % self.name

  def get_url(self):
    return '/'.join([self.service_url, self.name])

  def get(self, name):
    """ Return controls with the given name"""
    if name in self.child_map:
      return self.child_map[name]

  def controls(self):
    #return [item for sublist in self.child_map.values() for item in sublist]
    return self.child_map.values()

  def fetch_state(self):
    """get the current state of this panel from the server."""
    r = requests.get(self.get_url())
    if r.ok:
      self.etag = r.headers['etag']
      state = json.loads(r.content)
      for c in state['controls']:
        self.add_control_from_json(c)
    else:
      # state unknown, or server not available.
      print "Error fetching state."
      print r.status_code
      print r.reason
      print r.content
    
  def add_control_from_json(self, json):
    """Creates a Control object from a given json object."""
    if 'type' not in json.keys():
      print "no type. skipping object: %s"
      return
    else:
      obj = self.type_map[json['type']].from_json(json)
      self.add_control(obj)

  def add_control(self, control):
    control.parent = self
    if control.name not in self.child_map:
      self.child_map[control.name] = []
    #self.child_map[control.name].append(control)
    self.child_map[control.name] = control

  def dump_state(self):
    return json.dumps(
      { 'name': self.name,
        'type': 'controlpanel',
        'controls':
            [ x.as_dict() for x in self.controls() ]
      })

  def send_event(self, actuator, event):
    print event

  def save_state(self):
    #name = source_actuator.name
    #if len(self.child_map[name]) > 1:
    #  #other devices have this name.
    #  pass
    h = {}
    if self.etag:
      print "adding etag"
      h['If-Match'] = self.etag
    url = self.get_url()
    r = requests.put(url, self.dump_state(), headers=h)
    if r.ok:
      self.etag = json.loads(r.content)['etag']
      #r = requests.get(url)
    print r.status_code
    print r.reason
    print r.content



if __name__ == '__main__':
  cp = ControlPanel('testpanel')
  if cp.controls():
    print "found controls from saved state."
  else:
    b = Toggle('button')
    cp.add_control(b)

  print b.as_dict()
  print cp.dump_state()
  cp.save_state()


  #c = Counter('butts', 2)
  #cp.add_control(c)
  #b.toggle()
  #b.toggle()
  #b.toggle()
  #c.inc()
  #c.inc()
  #c.dec()
