# Proof Preset
A Preset object for `ProofDrawer()`.

## Structure
Preset objects are nested collections (lists and dicts) and have this structure:
```python
{
  "name": "My Favorite Preset",
  "groups" [
    {
      "name": "UC characters",
      "type size": 10,
      "leading": 12,
      "print": True,
      "contents": [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ
      ]
    },
    {
      "name": "LC characters",
      "type size": 10,
      "leading": 12,
      "print": False,
      "contents": [
        "abcdefghijklmnopqrstuvwxyz"
      ]
    }
  ]
}
```

At initialization, a `ProofPreset()` object only has `name` (`"myPreset"` by default, unless passed in by user) and `groups`, which is an empty `list`.

## Public Methods
A Preset object comes with a handful of public methods. These methods are "plugged-in" to the `ProofDrawer()` UI

### Getting Stuff
Users have access to all data through `ProofDrawer()`, either through the main window or its auxiliary windows (Proof Inspector, Preset Inspector).

The only thing that `ProofDrawer()` generates on its own is each group's "order" number, which is simply that group's index within `ProofPreset["groups"]` + 1.

#### getPresetName()
```python
ProofPreset("My First Preset").getPresetName()
```

