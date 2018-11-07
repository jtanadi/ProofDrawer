"""
For converting proof doc into preset file (JSON)
"""

class XMLtagError(Exception):
    pass

def getTags(inputList, tagName):
    """
    Return a list of tags only
    """
    return [item for item in inputList\
            if "<%s>" % tagName in item or "</%s>" % tagName in item]

def checkXMLtagsSequence(listOfTags):
    """
    Make sure open tags have closing ones:
    [<tag>, </tag>, <tag>, </tag>]
    """
    openTag = False
    for tag in listOfTags:
        # Detect open tag and continue
        if not openTag and "<" in tag and "/" not in tag:
            tagName = tag.strip("<").strip(">")
            openTag = True

        # If tag is open, close it if possible
        # if not possible, raise XMLtagError.
        # (Closing tag must match opening tag)
        else:
            if "</%s>" % tagName in tag:
                openTag = False
            else:
                raise XMLtagError("Incorrect <tag></tag> sequence")

    return True

def removeXMLtags(stringWithTags, tagName):
    """
    Return string between <tag></tag>
    If input doesn't follow correct format, an exception will be raised
    Currently unused
    """
    if not ("<%s>" % tagName and "</%s>" % tagName) in stringWithTags:
        raise XMLtagError("Check string formatting: <tag>string</tag>")

    return stringWithTags.replace("<%s>" % tagName, "")\
                         .replace("</%s>" % tagName, "")


def parseProofDoc(proofDocPathOrList, tagName):
    """
    Return a list of dicts from proofDoc formatted like so:
    [{tagName: group title, "contents": [content1, content2, etc.]}]
    tagName is the tag it should look out for.

    Proof doc should be written like example below.
    First line after opening tag is the title
    <group>
    UC, lc, and numerals
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    </group>
    """
    # Will a list ever be passed in?
    if isinstance(proofDocPathOrList, list):
        readList = proofDocPathOrList[:]
    else:
        f = open(proofDocPathOrList, "r")
        readList = f.readlines()
        f.close()

    # Check if tags are in sequence before anything else
    tagsList = getTags(readList, tagName)
    if not checkXMLtagsSequence(tagsList):
        return

    proofList = []
    startGroup = False

    for line in readList:
        # Skip over empty items (linebreak, etc.)
        cleanLine = line.strip()
        if not cleanLine:
            continue

        # Open tag: initialize and move on
        if "<%s>" % tagName in cleanLine:
            group = {}
            startGroup = True
            continue

        # Close tag: add group to proofList and move on
        elif "</%s>" % tagName in cleanLine:
            proofList.append(group)
            continue

        # Title line: add title to group[tagName] and initialize contents list
        if startGroup:
            group[tagName] = line.strip()
            group["contents"] = []
            startGroup = False # not the start of group anymore

        # Middle of block: just add line to group["contents"]
        else:
            group["contents"].append(cleanLine)

    return proofList


if __name__ == "__main__":
    # Simple testing
    tempTag = "group"
    stringToUse = "<%s>UC</%s>" % (tempTag, tempTag)
    print(removeXMLtags(stringToUse, tempTag))

    import os.path

    fileDir = os.path.dirname(__file__)
    testFile = os.path.join(fileDir, "tests", "resources", "proofDocTest.txt")

    testList = parseProofDoc(testFile, "group")
    print(testList)
