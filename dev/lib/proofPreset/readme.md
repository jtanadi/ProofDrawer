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

At initialization, a `ProofPreset()` object only has `name` (`"myPreset"` by default, unless passed in by user) and `groups`, which is an empty list.

## Public Methods
A Preset object comes with a handful of public methods. These methods are "plugged-in" to the `ProofDrawer()` UI.

### Getting Stuff
Users have access to all data through `ProofDrawer()`, either through the main window or its auxiliary windows (Proof Inspector, Preset Inspector).

The only thing that `ProofDrawer()` generates on its own is each group's "order" number, which is simply that group's index within `ProofPreset["groups"]` + 1.

#### `getGroupNames()`
Return a list of group names.
```python
myPreset.getGroupNames()
>>> ["UC", "lc", "numerals"]
```

#### `getGroups(verbose=True)`
Return a list of groups. By default, return all of the data associated with each group. If `verbose=False`, only return the group name and group contents.
```python
myPreset.getGroups()
>>> [
      {
        "name": "UC",
        "type size": 12,
        "leading": 14,
        "print": True,
        "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
      },
      {
        "name": "lc",
        "type size": 10,
        "leading": 10,
        "print": False,
        "contents": ["abcdefghijklmnopqrstuvwxyz"]
      }
    ]

myPreset.getGroups(verbose=False)
>>> [
      {
        "name": "UC",
        "contents": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
      },
      {
        "name": "lc",
        "contents": "abcdefghijklmnopqrstuvwxyz"
      }
    ]
```

#### `getPresetName()`
Return name of Preset object
```python
myFirstPreset = ProofPreset("My First Preset")
myFirstPreset.getPresetName()
>>> "My First Preset"
```

#### `getPreset(jsonFormat=False)`
Return the entire preset as a python dict. If `jsonFormat=True`, return the JSON object instead (basically a long string) with 2 spaces for indentation.
```python
myPreset.getPreset():
>>> {
      "name": "My Preset",
      "groups": [
        {
          "name": "UC",
          "type size": 10,
          "leading": 12,
          "print": True,
          "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        },
        {
          "name": "lc",
          "type size": 10,
          "leading": 12,
          "print": False,
          "contents": ["abcdefghijklmnopqrstuvwyxz"]
        },
        {
          "name": "numerals",
          "type size": 10,
          "leading": 12,
          "print": False,
          "contents": ["0123456789"]
        },
      ]
    }
```

