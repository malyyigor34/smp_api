import unittest

from smp_api.tests.data_extractor_test import DataExtractorTest
from smp_api.tests.page_getter_test import PageGetterTest

calcTestSuite = unittest.TestSuite()
calcTestSuite.addTest(unittest.makeSuite(PageGetterTest))
calcTestSuite.addTest(unittest.makeSuite(DataExtractorTest))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(calcTestSuite)
