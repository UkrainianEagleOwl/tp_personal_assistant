from memory_tests import*
from save_load_tests import *
from notes_core_tests import *

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()

    # Add test cases from each test file to the suite
    # notes tests
    suite.addTest(unittest.makeSuite(NotebookTestCase))
    suite.addTest(unittest.makeSuite(NoteTestCase))
    suite.addTest(unittest.makeSuite(TagTestCase))
    #save load tests
    suite.addTest(unittest.makeSuite(BooksSaveLoadTests))
    #memory tests
    suite.addTest(unittest.makeSuite(AddressBookTest))
    suite.addTest(unittest.makeSuite(NameTest))
    suite.addTest(unittest.makeSuite(PhoneTest))
    suite.addTest(unittest.makeSuite(BirthdayTestCase))
    suite.addTest(unittest.makeSuite(RecordTestCase))

    # Create a test runner and run the suite
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
