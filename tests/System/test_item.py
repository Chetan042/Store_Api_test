from models.item import ItemModel
from tests.base_test import BaseTest
from models.store import StoreModel
from models.user import UserModel
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                authreq = client.post('/auth', data=json.dumps({'username': 'test', 'password': '1234'}),
                                      headers={'Content-Type': 'application/json'})
                auth_token = json.loads(authreq.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                authreq = client.post('/auth', data =json.dumps({'username': 'test', 'password': '1234'}),
                                      headers={'Content-Type': 'application/json'})
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)


    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 149.99, 1)
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)


    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 149.99, 1)
                resp = client.delete('/item/test')
                self.assertEqual(resp.status_code, 200)

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/test', data={'price': 17.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.post('/item/test', data={'price': 17.99, 'store_id': 1})
                resp = client.post('/item/test', data={'price': 17.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 400)

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.put('/item/test', data={'price': 17.99, 'store_id': 1})
                self.assertEqual(ItemModel.find_by_name('test'))

    def test_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()
                self.assertEqual(ItemModel.find_by_name('test'))

                client.put('/item/test', data={'price': 7.99, 'store_id': 1})

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 5.99, 1).save_to_db()
                resp = client.get('/items')
                self.assertDictEqual({'items': [{'name': 'test', 'price': 7.99}]},
                                     json.loads(resp.data))
