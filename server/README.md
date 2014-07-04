=== Control Server

The Server is used to checkpoint the state of a control device.

This simple Proof of Concept server uses CloudKit for basic json storage.
Regrettably, we need to specify an older version of Rack for that to run,
so the server should be started with this command:

    sh rackup.sh cloudkit.ru


Eventually, the server will understand control operations directly, like
"toggle" or "increment". (thus avoiding get-mutate-set races).
