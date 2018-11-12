"""
Test work flow...
"""

from utils.proofPreset import ProofPreset
from utils.readWritePreset import readJSONpreset, writeJSONpreset
import os.path

currentDir = os.path.dirname(__file__)
proofFileDir = os.path.join(currentDir, "resources", "proofDocTest.txt")

with open(proofFileDir, "r") as proofFile:
    proofList = proofFile.readlines()

proofPreset = ProofPreset("proofPreset1")
proofPreset.importProof(proofList, "group")
presetList = proofPreset.getPreset()

presetFileDir = os.path.join(currentDir, "resources", "proofPresetTest.json")
writeJSONpreset(presetFileDir, presetList)
