"""
For converting proof doc into preset file (JSON)
"""

class XMLtagError(Exception):
    pass

def removeXMLtags(stringWithTags, tagName):
    """
    Returns string between <tag></tag>
    If input doesn't follow correct format, an exception will be raised
    """
    if not ("<%s>" % tagName and "</%s>" % tagName) in stringWithTags:
        raise XMLtagError("Check string formatting: <tag>string</tag>")

    return stringWithTags.replace("<%s>" % tagName, "")\
                         .replace("</%s>" % tagName, "")

def getIndicesOfTag(inputList, tagName):
    return [index for index, item in enumerate(inputList)\
            if "<%s>" % tagName and "</%s>" % tagName in item]

def parseProofDoc(filePath):
    """
    Take a text file and turn it into a list of dicts
    """
    # pass
    f = open(filePath, "r")
    readList = f.readlines()
    f.close()

    xmlTag = "group"
    proofList = []

    for index, line in enumerate(readList):
        if "<%s>" % xmlTag in line:
            group = {}
            group[xmlTag] = removeXMLtags(line, xmlTag).strip()
            group["contents"] = []
        else:
            lineToAppend = line.strip()
            if lineToAppend:
                group["contents"].append(lineToAppend)

        # If we're 1 item before the end of list or if the
        # next item has an xmlTag (ie. end of group), then append group to list
        if index == len(readList) - 1\
        or "<%s>" % xmlTag in readList[index + 1]:
            proofList.append(group)

    return proofList

if __name__ == "__main__":
    from dev.lib.utils import readWritePreset
    # Simple testing
    tag = "group"
    stringToUse = "<%s>UC</%s>" % (tag, tag)
    print(removeXMLtags(stringToUse, tag))

    import os.path

    fileDir = os.path.dirname(__file__)
    testFile = os.path.join(fileDir, "..", "..", "resources", "test.txt")

    testList = parseProofDoc(testFile)
    print(testList)
