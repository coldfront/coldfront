# Change Logging

ColdFront records every object creation, modification, and deletion in a
persistent change log. 

## How Change Logging Works

When an object is created, updated, or deleted, a serialized copy of the
object is saved to the database. The record includes:

- The time of the change
- The user who made the change
- A request ID that correlates changes from the same request
- The action that was performed (create, update, or delete)
- The object's state before and after the change

A serialized representation of the object is included in JSON format. This
is similar to how objects are conveyed in the REST API but does not include
nested representations.

## Request Correlation

Every request to ColdFront is assigned a random UUID. This UUID is attached
to all change records that result from the request. For example, if you
edit three objects in bulk, you see three change records all with the same
request ID. This shows that all three changes were part of the same request.

## Viewing Changes

The global change log can be viewed in the user interface. Each object
detail page also shows a per-object change log with the changes that
affected that object.

## API Access

Change records are available through the REST API at the read-only endpoint
for object changes. They can also be exported from the web interface in CSV
format.
