# Customization

Objects in ColdFront can be customized in many ways with needed to write any code.

## Tags

Most objects in ColdFront can be assigned user-created tags. Tags help
with organization and filtering. Each tag can have a color for quicker
differentiation in the user interface. Tags can be restricted to specific
object types.

Objects can be filtered by the tags they have applied. The `tag` filter
can be specified multiple times to match only objects that have all the
specified tags.

## Custom Fields

ColdFront administrators can create custom fields on objects to store
additional data. Custom fields support many types:

- **Text** — A single line of text
- **Integer** — A whole number
- **Boolean** — A true or false value
- **Date** — A date value
- **Select** — A single choice from a predefined list
- **Multi-select** — Multiple choices from a predefined list
- **Object reference** — A reference to another ColdFront object
- **JSON** — Arbitrary JSON data

Custom field data is stored directly alongside the object in the database.
Custom field data can be written and read through the REST API, just like
built-in fields.

## Custom Field Choice Sets

Choice fields use reusable choice sets defined as `CustomFieldChoiceSet`
objects. Each choice set has a name, description, and a list of choices.
Choice sets can be ordered alphabetically and reused across multiple
custom fields.

## Resource Attribute Schemas

Resources have a `schema` JSON field that defines custom attributes that are
captured on each allocation. The schema uses JSON Schema format and supports
various field types. Here's an example schema that would capture:

```json
{
    "properties": {
        "gpu": {
            "title": "GPU",
            "type": "string"
        },
        "interface": {
            "enum": [
                "PCIe 4.0",
                "PCIe 4.0 x8",
                "PCIe 4.0 x16",
                "PCIe 5.0 x16"
            ],
            "type": "string"
        },
        "memory": {
            "description": "Total memory capacity (in GB)",
            "title": "Memory (GB)",
            "type": "integer"
        }
    },
    "required": [
        "memory"
    ]
}
```
