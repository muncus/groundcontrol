== Ground Control

Physical controls, manipulating digital state.

=== Design

There are three basic types in play: `ControlPanel`, `Actuator` and `Watcher`.

==== ControlPanel
ControlPanel objects contain Actuators and Watchers. They are responsible for
communicating state changes to the web service, and receiving events from the
web service's event stream.

==== Actuator
Actuators are the base class for physical controls, like buttons and switches.

==== Watcher
Terrible name, but these objects respond to incoming SSEs, and respond to state
changes. For example, an LED turning on and off.

==== Web Service

(Note: most of this is not implemented)

PUT /device/<name> -> store json representation of the named ControlPanel
GET /device/<name> -> returns the json representation of the named ControlPanel
GET /device/<name>/events -> text/event-stream of state updates for the named ControlPanel.

Multiple devices may exist with the same name, but will be manipulating the same state.

=== Simple Use Case

Several coworkers, in separate offices, who like getting coffee together. Each
office has a button, and a light.  When any user presses the button, it toggles
the state of all the lights, alerting them to the opportunity for coffee.

Other software (like cron) can be used to alter the digital state, illuminating
the lights at the appointed time.
