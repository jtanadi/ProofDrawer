"""
Functions to read and write preset (JSON file)
"""
import json

def readJSONpreset(filePath):
    """
    Read JSON file and return the array as py list
    """
    try:
        jsonFile = open(filePath, "r")
        jsonList = jsonFile.read()
        jsonFile.close()
        return json.loads(jsonList)
    except FileNotFoundError:
        return []

def writeJSONpreset(filePath, contentList):
    """
    Write py list as JSON array
    """
    jsonContent = json.dumps(contentList, indent=2)
    fileToWrite = open(filePath, "w+")
    fileToWrite.write(jsonContent)
    fileToWrite.close()
