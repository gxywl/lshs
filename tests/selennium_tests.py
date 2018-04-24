# _*_ encoding: utf-8 _*_
from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser=webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.close()
        pass

    def test_can_start_a_list(self):

        self.browser.get('http://localhost:5000')

        self.assertIn('To-Do',self.browser.title)
        #self.fail('Finish the test!')

# if __name__=='__main__':
#     unittest.main(warnings='ignore')
