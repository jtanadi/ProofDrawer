"""
Utility functions for ProofPreset object

Here instead of in the same module as ProofPreset()
for cleanliness.

Should these be staticmethods?
"""

def cleanList(listToClean):
    """
    Get rid of leading and trailing whitespaces all at once
    Only include non-empty items in returned list
    """
    return [item.strip() for item in listToClean if item.strip()]