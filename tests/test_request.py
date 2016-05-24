import unittest

from .context import ask

TEST_FULL_REQUEST_DICT = {
    "session": {
        "sessionId": "SessionId.d461672c-2997-4d9d-9a8c-a67834acb9aa",
        "application": {
            "applicationId": "amzn1.echo-sdk-ams.app.a306b3a3-3331-43c1-87bd-87d29d16fac8"
        },
        "user": {
            "userId": "amzn1.account.AGBATYSC32Y2QVDQKOWJUUJNEYFA",
            "accessToken": "fillertoken-fix-later"
        },
        "new": True
    },
    "request": {
        "type": "IntentRequest",
        "requestId": "EdwRequestId.b22db637-b8f9-43c0-ae0c-1a9b35a02610",
        "timestamp": 1447911387582,
        "intent": {
            "name": "YesIntent",
            "slots": {
                "example1": {
                    "value": "value1"
                },
                "example2": {
                    "value": "value2"
                }
            }
        }
    }
}

TEST_SPARSE_REQUEST_DICT = {
    "session": {
        "sessionId": "SessionId.d461672c-2997-4d9d-9a8c-a67834acb9aa",
        "application": {
            "applicationId": "amzn1.echo-sdk-ams.app.a306b3a3-3331-43c1-87bd-87d29d16fac8"
        },
        "user": {
            "userId": "amzn1.account.AGBATYSC32Y2QVDQKOWJUUJNEYFA",
#            "accessToken": "fillertoken-fix-later"
        },
        "new": True
    },
    "request": {
        "type": "IntentRequest",
        "requestId": "EdwRequestId.b22db637-b8f9-43c0-ae0c-1a9b35a02610",
        "timestamp": 1447911387582,
        #"intent": {
        #    "name": "YesIntent",
        #    "slots": {}
        #}
    }
}


class TestStandardRequest(unittest.TestCase):

    def setUp(self):
        self.example = ask.Request(TEST_FULL_REQUEST_DICT)

    def tearDown(self):
        self.example = None

    def test_request_stores_request_dict(self):
        self.assertEqual(self.example.request, TEST_FULL_REQUEST_DICT)

    def test_request_stores_metadata(self):
        metadata = {'cute': 'puppy'}
        r = ask.Request(TEST_FULL_REQUEST_DICT, metadata=metadata)

        self.assertEqual(r.metadata, metadata)

    def test_request_metadata_is_blank_if_not_provided(self):
        self.assertEqual(self.example.metadata, {})

    def test_request_returns_request_type(self):
        req_type = self.example.request_type()

        self.assertEqual(req_type, 'IntentRequest')

    def test_request_returns_intent_name(self):
        intent_name = self.example.intent_name()

        self.assertEqual(intent_name, 'YesIntent')

    def test_request_is_intent(self):
        res = self.example.is_intent()

        self.assertTrue(res)

    def test_request_returns_user_id(self):
        user_id = self.example.user_id()

        self.assertEqual(user_id, "amzn1.account.AGBATYSC32Y2QVDQKOWJUUJNEYFA")

    def test_request_returns_access_token(self):
        token = self.example.access_token()

        self.assertEqual(token, "fillertoken-fix-later")

    def test_request_returns_session_id(self):
        session_id = self.example.session_id()

        self.assertEqual(session_id, "SessionId.d461672c-2997-4d9d-9a8c-a67834acb9aa")

    def test_request_returns_slot_value(self):
        val1 = self.example.get_slot_value("example1")
        val2 = self.example.get_slot_value("example2")

        self.assertEquals(val1, "value1")
        self.assertEquals(val2, "value2")

    def test_request_returns_slot_names(self):
        names = self.example.get_slot_names()

        self.assertItemsEqual(names, ["example1", "example2"])

    def test_request_returns_slot_map(self):
        slot_map = self.example.get_slot_map()
        expected = {'example1': 'value1', 'example2': 'value2'}

        self.assertEqual(slot_map, expected)

    def test_request_slots_property_assigned_on_init(self):
        slot_map = self.example.get_slot_map()
        slots = self.example.slots

        self.assertEqual(slots, slot_map)
        self.assertIsNotNone(slots)


class TestSparseRequest(unittest.TestCase):

    def setUp(self):
        self.example = ask.Request(TEST_SPARSE_REQUEST_DICT)

    def tearDown(self):
        self.example = None

    def test_intent_name_with_no_intent(self):
        self.assertIsNone(self.example.intent_name())

    def test_is_intent_returns_False_with_no_intent(self):
        self.assertFalse(self.example.is_intent())

    def test_access_token_returns_None(self):
        self.assertIsNone(self.example.access_token())

    def test_slot_value_returns_None(self):
        self.assertIsNone(self.example.access_token())

    def test_slot_names_returns_empty_list(self):
        self.assertEqual(self.example.get_slot_names(), [])

    def test_slot_map_returns_empty_dict(self):
        self.assertEqual(self.example.get_slot_map(), {})


@unittest.skip('Unsure proper functionality.  Pass or raise better error?')
class TestEmptyRequest(unittest.TestCase):

    def test_empty_request(self):
        try:
            empty = Request({}) # fails on keyerror:
        except:
            self.fail('Failed to create Request with empty request_dict')


if __name__ == '__main__':
    unittest.main()
