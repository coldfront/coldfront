---
icon: lucide/puzzle
---

# Plugins

Plugins are packaged Django apps that can be installed alongside ColdFront
to provide custom functionality not present in the core application.
Plugins can introduce their own models, views, navigation items, and
template content. They cannot modify core ColdFront models or settings.

## Capabilities

The ColdFront plugin architecture allows for the following:

- **Add new data models** — A plugin can introduce one or more models to
  hold data. A model is essentially a table in the SQL database.

- **Add new URLs and views** — Plugins can register URLs under the
  `/plugins` root path to provide browsable views for users.

- **Add content to existing model templates** — A plugin can inject custom
  HTML content within the view of a core ColdFront model. This content can
  appear in the left side, right side, or bottom of the page.

- **Add navigation menu items** — Each plugin can register new links in
  the navigation menu. Each link can have a set of buttons for specific
  actions, similar to the built-in navigation items.

- **Add custom middleware** — Custom Django middleware can be registered
  by each plugin.

- **Declare configuration parameters** — Each plugin can define required,
  optional, and default configuration parameters within its own namespace.
  Plugin configuration parameters are defined by the user under
  `PLUGINS_CONFIG` in `local_settings.py`.

- **Limit installation by ColdFront version** — A plugin can specify a
  minimum and maximum ColdFront version with which it is compatible.

- **Register custom columns on existing tables** — A plugin can add
  columns to existing ColdFront tables using the column registration
  system.

- **Register REST API endpoints** — Plugins can provide their own API
  viewsets and serializers under the `/api/plugins` path.

## Limitations

A plugin may not:

- **Modify core models** — Plugins cannot alter, remove, or override core
  ColdFront models. This rule protects the integrity of the core data
  model.

- **Override core templates** — Plugins can inject additional content
  where supported, but cannot manipulate or remove core content.

- **Modify core settings** — A configuration registry is provided for
  plugins, but they cannot alter or delete the core configuration.

- **Disable core components** — Plugins are not permitted to disable or
  hide core ColdFront components.

## Installing a Plugin

To install a plugin, add it to the `PLUGINS` list in your
`local_settings.py`:

```python
PLUGINS = [
    "my_custom_plugin",
]
```

Plugin-specific configuration can be set in `PLUGINS_CONFIG`:

```python
PLUGINS_CONFIG = {
    "my_custom_plugin": {
        "MY_SETTING": "value",
    },
}
```

See the [development guide](development.md) for information on building
your own plugins.
