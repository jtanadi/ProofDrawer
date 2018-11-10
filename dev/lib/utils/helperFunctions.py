"""
Helper functions
"""

def getValuesFromListOfDicts(listOfDicts, keyToSearch):
    """
    Return a list of values of keyToSearch from a list of dicts
    """
    return [singleDict[keyToSearch] for singleDict in listOfDicts\
           if singleDict[keyToSearch]]

def convertToListOfPyDicts(listOfNSDicts):
    """
    Return a list of Py dicts

    Since dicts in vanilla.List() are converted to __NSDictionaryM,
    we have to transfer them back to Py dicts for some internal funcs,
    like writing to JSON, internal dict manipulations, etc.
    """
    return [{key:value for (key, value) in dictItem.items()}\
            for dictItem in listOfNSDicts]
