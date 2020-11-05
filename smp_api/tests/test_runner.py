import unittest

#from smp_api.tests.data_extractor_test import DataExtractorTest
#from smp_api.tests.page_getter_test import PageGetterTest
from smp_api.tests.browser_test import BrowserTest

calcTestSuite = unittest.TestSuite()
#calcTestSuite.addTest(unittest.makeSuite(PageGetterTest))
#calcTestSuite.addTest(unittest.makeSuite(DataExtractorTest))
calcTestSuite.addTest(unittest.makeSuite(BrowserTest))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(calcTestSuite)
