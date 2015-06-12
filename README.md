# junos-config cookbook

Chef cookbook for pushing any type of Juniper configuration changes. Uses a designated host to push changes by utilizing the [JunOS PyEZ library](https://techwiki.juniper.net/Automation_Scripting/010_Getting_Started_and_Reference/Junos_PyEZ).

## Supported Platforms

All Juniper devices supported by the PyEZ library are supported. Any type of configuration change is supported, not just the set of resources exposed by the [netdev cookbook](https://github.com/opscode-cookbooks/netdev).

## Attributes

## Usage

### junos-config::default

Include `junos-config` in your node's `run_list`:

```json
{
  "run_list": [
    "recipe[junos-config::default]"
  ]
}
```

## License and Authors

Open sourced under the GPLv2 license.

Author: Arne Sund (git@arnesund.no)
