__author__ = 'odrulea'

from cloudbrain.apps.AnalysisModules import ModuleAbstract
from cloudbrain.apps.AnalysisModules.utils import MatrixToBuffer, BufferToMatrix
import numpy as np

class ModuleTest(ModuleAbstract.ModuleAbstract):

    MODULE_NAME = "Test Module"

    # __init__ is handled by parent ModuleAbstract

    def setup(self):
        ModuleAbstract.ModuleAbstract.setup(self)
        # print self.MODULE_NAME+": setup"

    def consume(self, ch, method, properties, body):

        buffer_content = BufferToMatrix(body)

        if self.debug:
            print buffer_content.shape
            print buffer_content
            print
            print




