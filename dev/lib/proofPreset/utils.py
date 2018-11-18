"""
Utility functions for ProofPreset object

Here instead of in the same module as ProofPreset()
for cleanliness.

Should these be staticmethods?
"""

from proofPreset.errors import XMLtagError

def cleanList(listToClean, discardBefore=None, discardAfter=None):
    """
    Get rid of leading and trailing whitespaces all at once
    Only include non-empty items in returned list
    """
    cleanList = [item.strip() for item in listToClean if item.strip()]

    if discardBefore:
        startIndex = cleanList.index(discardBefore)
        cleanList = cleanList[startIndex:]

    if discardAfter:
        cleanList.reverse()
        endIndex = len(cleanList) - cleanList.index(discardAfter)
        cleanList.reverse()
        cleanList = cleanList[:endIndex]

    return cleanList



def checkForTags(listOfItems, tagName):
    """
    Make sure object has opening & closing tags at all
    """
    if "<%s>" % tagName not in listOfItems or \
    "</%s>" % tagName not in listOfItems:
        raise XMLtagError("<%s> tags not in this list" % tagName)

def getTags(listOfItems, tagName):
    """
    Return a list of tags from listOfItems
    Tags are either <tagName> or </tagName>
    """
    return [item for item in listOfItems\
            if item in("<%s>" % tagName, "</%s>" % tagName)]

def checkXMLtagsSequence(listOfItems, tagName):
    """
    Look through listOfItems and make sure
    an open tag is always followed by a closing tag,
    and their sequence is exactly:
    [<tag>, </tag>, <tag>, </tag>]

    Tags are <tagName> </tagName>
    """
    openTag = True
    openTagCount = 0
    closeTagCount = 0

    for tag in getTags(listOfItems, tagName):
        if openTag and tag == "<%s>" % tagName:
            openTagCount += 1
            openTag = False # Next is supposed to be close tag
        elif not openTag and tag == "</%s>" % tagName:
            closeTagCount += 1
            openTag = True # Next is supposed to be open tag
        else:
            raise XMLtagError("Incorrect <tag></tag> sequence")

    if openTagCount != closeTagCount:
        raise XMLtagError("Not all tags are paired")