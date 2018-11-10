"""
Helper functions
"""

def getValuesFromListOfDicts(listOfDicts, keyToSearch):
    """
    Return a list of values of keyToSearch from a list of dicts
    """
    return [singleDict[keyToSearch] for singleDict in listOfDicts\
           if singleDict[keyToSearch]]
