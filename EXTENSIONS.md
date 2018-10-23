# Config File

Inside the `mediator`'s config file (`mediaconf.yaml`) there is section for describing extensions:

```yaml
extensions:
  space.colabo.search_extension:
    general:
      exists: true
      active: false
    host: "158.37.63.127"
    port: 12345
```

Each extension consists of the key (like: the `space.colabo.search_extension`) and configuration data. `general` section MUST exist for each extension, otherwise config manager (`ConfigManager.py`) will complain.

+ `general.exists` - tells if the extension exist in the Audio Common ecosystem
+ `general.active` - tells if the extension is currently used in the Audio Common ecosystem

Config manager (`ConfigManager.py`) has helping function for working with extensions:

+ `getExtensionConfig(self, extensionName)` - provides dictionary describing the extension `extensionName`
+ `isExtensionExisting(self, extensionName)` - tells if the extension exists in the AC ecosystem
+ `isExtensionActive(self, extensionName)` - tells if the extension is active in the AC ecosystem