"""
Test work flow...
"""

from lib.utils.proofPreset import ProofPreset
from lib.utils.readWritePreset import readJSONpreset, writeJSONpreset
import os.path

currentDir = os.path.dirname(__file__)
proofFileDir = os.path.join(currentDir, "resources", "proofDocTest.txt")

proofFile = open(proofFileDir, "r")
proofList = proofFile.readlines()
proofFile.close()

proofPreset = ProofPreset(proofList, "group")
presetList = proofPreset.getPreset()

presetFileDir = os.path.join(currentDir, "resources", "proofPresetTest.json")
writeJSONpreset(presetFileDir, presetList)
