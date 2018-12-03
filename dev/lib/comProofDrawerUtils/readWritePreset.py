"""
Functions to read and write preset (JSON file)
"""
import json

def readJSONpreset(filePath):
    """
    Read JSON file and return the array as py list
    """
    try:
        with open(filePath, "r") as jsonFile:
            return json.loads(jsonFile.read())

    except FileNotFoundError:
        return []

def writeJSONpreset(filePath, contentList):
    """
    Write py list as JSON array
    """
    with open(filePath, "w+") as fileToWrite:
        fileToWrite.write(json.dumps(contentList, indent=2))
