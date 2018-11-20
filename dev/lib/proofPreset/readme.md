# Proof Preset
A Preset object for `ProofDrawer()`.

**TODO**  
Think about making a base preset implementation (`BasePreset()`?) as a parent of `ProofPreset()` so we can make other child preset objects (`ColorPreset()`, `PrintPreset()`, etc. etc.).

## Structure
`ProofPreset()` objects are nested collections (lists and dicts) and have this structure:
```python
{
    "name": "My Favorite Preset",
    "groups" [
        {
            "name": "UC, lc",
            "typeSize": 10,
            "leading": 12,
            "print": True,
            "contents": [
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                "abcdefghijklmnopqrstuvwxyz"
            ]
        },
        {
            "name": "Numerals, symbols",
            "typeSize": 10,
            "leading": 12,
            "print": False,
            "contents": [
                "1234567890",
                "!@#$%^&*()"
            ]
        }
    ]
}
```

Each item in the `contents` list is a line of proof string.

At initialization, a `ProofPreset()` object only has `name` (`"myPreset"` by default, unless passed in by user) and `groups`, which is an empty list.

```python
>>> myPreset = ProofPreset() # Default preset name is "myPreset"
>>> coolPreset = ProofPreset("Cool Preset") # Preset name is "Cool Preset"
```

## Public Methods
A Preset object comes with a handful of public methods. These methods are "plugged-in" to the `ProofDrawer()` UI.

### Importing & Exporting Stuff
Users can import XML-tagged strings or lists, JSON-formatted presets, or Python-formatted presets. Some import methods accept file paths or a python type (`str` or `list`).

#### `importFromJSON(jsonInput, overwrite=False)`
Import an entire preset from a JSON file path or a JSON-like `str` and convert it to a `ProofPreset()` object. Since each `ProofPreset()` object can only contain one preset, if `overwrite=False` and the `ProofPreset()` object isn't empty, a `ProofPresetError` will be raised.

This method simply reads the file path or string, converts the JSON object into a Python dictionary, and passes it to the `importPyDict()` method, so it has the same restrictions / requirements / processes as described next.

If passing a file path, it must be to a `.json` file.

```python
>>> currentDir = os.path.dirname(__file__)
>>> jsonPath = os.path.join(currentDir, "presets", "preset1.json")
>>> myPreset.importFromJSON(jsonPath)
```

#### `importPyDict(pyDictInput, overwrite=False)`
Import an entire preset from a Python dict. If `overwrite=False`, a `ProofPresetError` will be raised if the `ProofPreset()` object isn't empty.

Imported presets must have a name and at least one group (otherwise it's just an empty preset, which is the same as what we get when we initialize `ProofPreset()`). 

Before fully importing, `ProofPreset()` performs some basic tasks:
- Remove unnecessary keys in each group. The only group keys relevant to `ProofPreset()` are `name`, `typeSize`, `leading`, `print`, `contents`; everything else will be removed.
- Add missing keys. If any of the keys listed above are missing, they will be added to the group.

After import, `ProofPreset()` inspects all imported group names and appends a "count" to duplicated names.

```python
>>> newPreset = {
    "name": "New Preset",
    "groups": [
        {
            "name": "UC",
            "typeSize": 8,
            "amazing": False,
            "print": False,
            "contents": [
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ]
        },
        {
            "name": "lc",
            "typeSize": 8,
            "amazing": True,
            "print": True,
            "contents": [
                "abcdefghijklmnopqrstuvwxyz"
            ]
        },
        {
            "name": "lc",
            "typeSize": 10,
            "amazing": True,
            "print": False,
            "contents": [
                "abcdefghijklmnopqrstuvwxyz"
            ]
        },
        {
            "name": "lc",
            "typeSize": 12,
            "print": False,
            "contents": [
                "abcdefghijklmnopqrstuvwxyz"
            ]
        }
    ]
}

>>> myPreset.importPreset(newPreset)
>>> myPreset.getPreset()
{
    "name": "New Preset",
    "groups": [
        {
            "name": "UC",
            "typeSize": 8,
            "leading": "",
            "print": False,
            "contents": [
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ]
        },
        {
            "name": "lc",
            "typeSize": 8,
            "leading": "",
            "print": True,
            "contents": [
                "abcdefghijklmnopqrstuvwxyz"
            ]
        },
        {
            "name": "lc-1",
            "typeSize": 10,
            "leading": "",
            "print": False,
            "contents": [
                "abcdefghijklmnopqrstuvwxyz"
            ]
        },
        {
            "name": "lc-2",
            "typeSize": 12,
            "leading": "",
            "print": False,
            "contents": [
                "abcdefghijklmnopqrstuvwxyz"
            ]
        }
    ]
}
```

#### `importFromXML(xmlTaggedInput)`
Import from XML-tagged proof document. `xmlTaggedInput` can be a file path or a `str` or `list` with XML tags (eg. if user uses `read()` or `readlines()` outside of object.

XML-tagged proof documents aren't presets, but only a list of proof "groups". Each group must be wrapped in `<group>` / `</group>` tags and the first line of each group is its group name. Each subsequent line in a group is an item in that group's `contents` list.

For example:
```
<group>
UC
ABCDEFGHIJKLMNOPQRSTUVWXYZ
</group>

<group>
UC between control chars
|H| |O| HHHOHOHOOOHO
|A| HHHAHAAAOOOAOAAA
|B| HHHBHBBBOOOBOBBB
|C| HHHCHCCCOOOCOCCC
...
</group>
```

Before fully importing, `ProofPreset()` performs some basic cleaning & validation: 
- Remove empty lines or list items and leading or trailing whitespaces
- Check if both `<group>` and `</group>` tags exist at all
- Check if tags are in correct sequence (*exactly* open, close, open, close, etc.). The sequence can't start with a closing tag, all open tags must be closed, and no nesting is allowed.

If any part of the validation process fails, an `XMLtagError` is raised.

Because `xmlTaggedInput` isn't a preset (ie. doesn't contain other data like `typeSize`), `ProofPreset()` will inject empty values into each group.

If passing a file path, it must be to an `.xml` or `.txt` file.

```python
>>> proofStr = "<group>\nUC\nABCDEFGHIJKLMNOPQRSTUVWXYZ\n</group>"
>>> proofList = ["<group>", "UC", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "</group>"]

>>> myPreset.importFromXML(proofList) # Either object is fine
>>> myPreset.getPreset()
{
    "name": "Best Preset",
    "groups": [
        {
            "name": "UC",
            "typeSize": "",
            "leading": "",
            "print": False,
            "contents": [
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            ]
        }
    ]
}
```

#### `exportToJSON(filePath)`
_Should `ProofPreset()` export to a file w/ same name as preset name?_

Export an entire preset to a JSON file. `filePath` must have have `.json` extension. If the file doesn't exist, it will be created.

This method is a helper built ontop of `getPreset(jsonFormat=True)`.

```python
>>> currentDir = os.path.dirname(__file__)
>>> jsonFilePath = os.path.join(currentDir, "presets", "myPreset.json")
>>> myPreset.exportToJSON(jsonFilePath)
# File written in currentDir/presets/myPreset.json
```

File content:
```json
{
  "name": "New Preset",
  "groups": [
    {
      "name": "UC",
      "typeSize": 8,
      "leading": "",
      "print": false,
      "contents": [
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
      ]
    }  
    { 
      "name": "lc",
      "typeSize": 8,
      "leading": "",
      "print": true,
      "contents": [
        "abcdefghijklmnopqrstuvwxyz"
      ]
    },
  ]
}
```

#### `exportToXML(filePath)`
_Should `ProofPreset()` export to a file w/ same name as preset name?_

Export `ProofPreset()` groups as XML-tagged groups. `filePath` must have an `.xml` or `.txt` extension. If the file doesn't exist, it will be created.

This method is a helper built on top of `getXMLGroups()`.

```python
>>> currentDir = os.path.dirname(__file__)
>>> xmlFilePath = os.path.join(currentDir, "proof groups", "myProofGroups.xml")
>>> myPreset.exportToXML(xmlFilePath)
# File written in currentDir/proof groups/myProofGroups.xml
```

File content:
```xml
<group>
UC
ABCDEFGHIJKLMNOPQRSTUVWXYZ
</group>

<group>
lc
abcdefghijklmnopqrstuvwxyz
</group>

<group>
numerals
0123456789
</group>
```

### Getting Stuff
Users have access to all data through `ProofDrawer()`, either through the main window or its auxiliary windows (Proof Inspector, Preset Inspector).

The only thing that `ProofDrawer()` generates on its own is each group's "order" number, which is simply that group's index within `ProofPreset["groups"]` + 1.

#### `getPresetName()`
Return name of `ProofPreset()` object
```python
>>> myFirstPreset = ProofPreset("My First Preset")
>>> myFirstPreset.getPresetName()
"My First Preset"
```

#### `getPreset(jsonFormat=False)`
Return the entire `ProofPreset()` as a Python dict. If `jsonFormat=True`, return the JSON object instead (basically a long string) with 2 spaces for indentation.
```python
>>> myPreset.getPreset()
{
    "name": "My Preset",
    "groups": [
        {
            "name": "UC",
            "typeSize": 10,
            "leading": 12,
            "print": True,
            "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
        },
        {
            "name": "lc",
            "typeSize": 10,
            "leading": 12,
            "print": False,
            "contents": ["abcdefghijklmnopqrstuvwyxz"]
        },
        {
            "name": "numerals",
            "typeSize": 10,
            "leading": 12,
            "print": False,
            "contents": ["0123456789"]
        },
    ]
}
```

#### `getGroupNames(returnCopies=True)`
Return a list of group names.

If `returnCopies=False`, only names without counters will be returned
```python
>>> myPreset.getGroupNames()
["UC", "UC-1", "UC-2", "lc", "lc-1", "numerals", "symbols", "symbols-1"]

>>> myPreset.getGroupNames(returnCopies=False)
["UC", "lc","numerals", "symbols"]
```

#### `getGroups(verbose=True)`
Return a list of groups. By default, return all of the data associated with each group. If `verbose=False`, only return the group name and group contents.
```python
>>> myPreset.getGroups()
[
    {
        "name": "UC",
        "typeSize": 12,
        "leading": 14,
        "print": True,
        "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    },
    {
        "name": "lc",
        "typeSize": 10,
        "leading": 10,
        "print": False,
        "contents": ["abcdefghijklmnopqrstuvwxyz"]
    }
]

>>> myPreset.getGroups(verbose=False)
[
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

#### `getXMLGroups()`
Return `ProofPreset()` groups as XML-tagged groups in a string.

Each group is wrapped by `<group>` / `</group>` tags; groups are separated by empty an empty newline. The first line of each group is always the group name.

```python
>>> myPreset.getXMLGroups()
<group>
UC
ABCDEFGHIJKLMNOPQRSTUVWXYZ
</group>

<group>
lc
abcdefghijklmnopqrstuvwxyz
</group>
```

### Dealing with Presets and Groups

#### `renamePreset(newName)`
Rename a `ProofPreset()` object. `newName` is a string and can be anything, even if the name already exists; the `ProofPreset()` object doesn't do any checking.

```python
>>> newPreset = ProofPreset("New Preset")
>>> newPreset.getPresetName()
"New Preset"

>>> newPreset.renamePreset("Old Preset")
>>> newPreset.getPresetName()
"Old Preset"
```

#### `duplicatePreset(duplicateName=None)`
Duplicate a `ProofPreset()` object. If `duplicateName` is passed in, the duplicated object will have that name; otherwise, it will us the name of the original with "-copy" appended.

The object returned is a `deepcopy` and needs to be captured by a variable.

```python
>>> myPreset = ProofPreset("My Preset")
>>> dupePreset1 = myPreset.duplicate()
>>> dupePreset2 = myPreset.duplicate("Amazing Preset")

>>> dupePreset1.getPresetName()
"My Preset-copy"

>>> dupePreset2.getPresetName()
"Amazing Preset"
```

#### `editGroup(groupToEdit, **kwargs)`
Edit a specified group. `groupToEdit` can be the name of a group or its index within the `groups` list.

`**kwargs` will accept any `key=value` pair. If the `key` passed in isn't part of the necessary set of keys (`name`, `typeSize`, `leading`, `print`, `contents`), it will be ignored.

```python
>>> myPreset.getGroups()
[
    {
        "name": "UC",
        "typeSize": 10,
        "leading": 12,
        "print": False,
        "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    },
    {
        "name": "lc",
        "typeSize": 10,
        "leading": 12,
        "print": False,
        "contents": ["abcdefghijklmnopqrstuvwxyz"]
    }
]

>>> myPreset.editGroup(1, name="numerals", print=True, contents="0123456789", random=True)
>>> myPreset.getGroups()
[
    {
        "name": "UC",
        "typeSize": 10,
        "leading": 12,
        "print": False,
        "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    },
    {
        "name": "numerals",
        "typeSize": 10,
        "leading": 12,
        "print": True,
        "contents": ["0123456789"]
    }
]
```

#### `addGroup(groupToAdd, overwrite=False)`
Add a proof group to the `ProofPreset()` object. The new group is added to the end of the `groups` list. 

`groupToAdd` is a Python dict with at least a `name` key. Much like when importing an entire Preset, `ProofPreset()` checks whether any necessary keys are missing (and adds them) and whether the new group has unneeded keys (and doesn't include them).

If `overwrite=False` and a group of the same name already exists, `ProofPreset()` will add a "count" to the end of the new group's name.

```python
>>> newGroup = {
    "name": "Numerals"
}
>>> myPreset.addGroup(newGroup)
>>> myPreset.getGroups()
[
    {
        "name": "UC",
        "typeSize": 10,
        "leading": 12,
        "print": True,
        "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ]
    },
    {
        "name": "Numerals",
        "typeSize": "",
        "leading": "",
        "print": False,
        "contents": []
    }
]

>>> secondNewGroup = {
    "name": "Numerals",
    "typeSize": 12,
    "contents": ["0123456789"]
}
>>> myPreset.addGroup(secondNewGroup)
>>> myPreset.getGroups()
[
    {
        "name": "UC",
        "typeSize": 10,
        "leading": 12,
        "print": True,
        "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ]
    },
    {
        "name": "Numerals",
        "typeSize": "",
        "leading": "",
        "print": False,
        "contents": []
    },
    {
        "name": "Numerals-1",
        "typeSize": 12,
        "leading": "",
        "print": False,
        "contents": ["0123456789"]
    },
]
```

#### `moveGroup(currentIndex, newIndex)`
Move group of `currentIndex` to `newIndex`.

```python
>>> myPreset.getGroups(verbose=False)
[
    {
        "name": "UC",
        "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    },
    {
        "name": "lc",
        "contents": ["abcdeghijklmnopqrstuvwxyz"]
    },
    {
        "name": "Numerals",
        "contents": ["0123456789"]
    },
    {
        "name": "Symbols",
        "contents": ["!@#$%^&*()"]
    }
]
>>> myPreset.moveGroup(2, 1)
>>> myPreset.getGroups(verbose=False)
[
    {
        "name": "UC",
        "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    },
    {
        "name": "Numerals",
        "contents": ["0123456789"]
    },
    {
        "name": "lc",
        "contents": ["abcdeghijklmnopqrstuvwxyz"]
    },
    {
        "name": "Symbols",
        "contents": ["!@#$%^&*()"]
    }
]
```

#### `removeGroup(groupToRemove)`
Remove a group from the `ProofPreset()` object. `groupToRemove` can be the index of the group within the `groups` list or the name of the group.

```python
>>> myPreset.getGroups(verbose=False)
[
    {
        "name": "UC",
        "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    },
    {
        "name": "Numerals",
        "contents": ["0123456789"]
    },
    {
        "name": "lc",
        "contents": ["abcdeghijklmnopqrstuvwxyz"]
    },
    {
        "name": "Symbols",
        "contents": ["!@#$%^&*()"]
    }
]

>>> myPreset.removeGroup(2)
>>> myPreset.getGroups(verbose=False)
[
    {
        "name": "UC",
        "contents": ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    },
    {
        "name": "Numerals",
        "contents": ["0123456789"]
    },
    {
        "name": "Symbols",
        "contents": ["!@#$%^&*()"]
    }
]
```
