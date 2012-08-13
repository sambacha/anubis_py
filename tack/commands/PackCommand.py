# Authors: 
#   Trevor Perrin
#   Moxie Marlinspike
#
# See the LICENSE file for legal information regarding use of this file.

import sys
from tack.commands.Command import Command
from tack.structures.TackActivation import TackActivation
from tack.structures.TackExtension import TackExtension
from tack.tls.TlsCertificate import TlsCertificate

class PackCommand(Command):

    def __init__(self, argv):
        Command.__init__(self, argv, "otba", "vx")
        self.outputFile, self.outputFileName = self.getOutputFile()
        self.tacks = self.getTacks()
        self.breakSignatures = self.getBreakSignatures()
        self.activationFlags = self._getActivationFlags()

    def execute(self):
        tackExtension = TackExtension.create(self.tacks, self.breakSignatures,
                                                self.activationFlags)

        self.outputFile.write(self.addPemComments(tackExtension.serializeAsPem()))
        self.printVerbose(str(tackExtension))
        
    def _getActivationFlags(self):
        activation_flags = self._getOptionValue("-a")

        if activation_flags is None:
            return TackActivation.NONE

        try:
            activation_flags = int(activation_flags) # Could raise ValueError
            if activation_flags < 0 or activation_flags > TackActivation.BOTH_ACTIVE:
                raise ValueError()
        except ValueError:
            self.printError("Bad activation_flags: %s" % activation_flags)

        return activation_flags


    @staticmethod
    def printHelp():
        print(
"""Takes the input Tacks, Break Sigs, and Activation Flag, and produces a 
TACK_Extension from them.

Optional arguments:
  -v                 : Verbose
  -t TACKS           : Include Tacks from this file.
  -b BREAKSIGS       : Include Break Signatures from this file.
  -a FLAG            : Activation flag (0 or 1)
  -o FILE            : Write the output to this file (instead of stdout)
""")
