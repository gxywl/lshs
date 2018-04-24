# _*_ encoding: utf-8 _*_
import unittest

from flask import url_for

from app import create_app, db


class TestURLs(unittest.TestCase):

    def setUp(self):
        self.app=create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # db.create_all()
        self.client=self.app.test_client(use_cookies=True)


    def tearDown(self):
        db.session.remove()
        #db.drop_all()
        self.app_context.pop()

    def test_root_redirect(self):
        #result=self.client.get('/')
        result = self.client.get(url_for('main.index'))  #SERVER_NAME ='localhost'
        #self.assertEqual(result.status_code,302)
        #self.assertIn('/blog/',result.headers['Location'])
        self.assertTrue('Stranger' in result.get_data(as_text=True))

# if __name__=='__main__':
#     unittest.main()