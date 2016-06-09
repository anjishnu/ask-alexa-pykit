from unittest import skip

from nose.tools import *

from .context import ask
from .fixtures.requests import TEST_FULL_REQUEST_DICT, TEST_SPARSE_REQUEST_DICT



class TestStandardRequest(object):

    def setUp(self):
        self.example = ask.Request(TEST_FULL_REQUEST_DICT)

    def tearDown(self):
        self.example = None

    def test_request_stores_request_dict(self):
        assert_equal(self.example.request, TEST_FULL_REQUEST_DICT)

    def test_request_stores_metadata(self):
        metadata = {'cute': 'puppy'}
        r = ask.Request(TEST_FULL_REQUEST_DICT, metadata=metadata)

        assert_equal(r.metadata, metadata)

    def test_request_metadata_is_blank_if_not_provided(self):
        assert_equal(self.example.metadata, {})

    def test_request_returns_request_type(self):
        req_type = self.example.request_type()

        assert_equal(req_type, 'IntentRequest')

    def test_request_returns_intent_name(self):
        intent_name = self.example.intent_name()

        assert_equal(intent_name, 'YesIntent')

    def test_request_is_intent(self):
        res = self.example.is_intent()

        assert_true(res)

    def test_request_returns_user_id(self):
        user_id = self.example.user_id()

        assert_equal(user_id, "amzn1.account.AGBATYSC32Y2QVDQKOWJUUJNEYFA")

    def test_request_returns_access_token(self):
        token = self.example.access_token()

        assert_equal(token, "fillertoken-fix-later")

    def test_request_returns_session_id(self):
        session_id = self.example.session_id()

        assert_equal(session_id, "SessionId.d461672c-2997-4d9d-9a8c-a67834acb9aa")

    def test_request_returns_slot_value(self):
        val1 = self.example.get_slot_value("example1")
        val2 = self.example.get_slot_value("example2")

        assert_equal(val1, "value1")
        assert_equal(val2, "value2")

    def test_request_returns_slot_names(self):
        names = self.example.get_slot_names()

        assert_items_equal(names, ["example1", "example2"])

    def test_request_returns_slot_map(self):
        slot_map = self.example.get_slot_map()
        expected = {'example1': 'value1', 'example2': 'value2'}

        assert_equal(slot_map, expected)

    def test_request_slots_property_assigned_on_init(self):
        slot_map = self.example.get_slot_map()
        slots = self.example.slots

        assert_equal(slots, slot_map)
        assert_is_not_none(slots)


class TestSparseRequest(object):
    def setUp(self):
        self.example = ask.Request(TEST_SPARSE_REQUEST_DICT)

    def tearDown(self):
        self.example = None

    def test_intent_name_with_no_intent(self):
        assert_is_none(self.example.intent_name())

    def test_is_intent_returns_False_with_no_intent(self):
        assert_false(self.example.is_intent())

    def test_access_token_returns_None(self):
        assert_is_none(self.example.access_token())

    def test_slot_value_returns_None(self):
        assert_is_none(self.example.access_token())

    def test_slot_names_returns_empty_list(self):
        assert_equal(self.example.get_slot_names(), [])

    def test_slot_map_returns_empty_dict(self):
        assert_equal(self.example.get_slot_map(), {})


class TestEmptyRequest(object):

    #@raises(KeyError)
    @skip('Unsure proper functionality.  Pass or raise better error?')
    def test_empty_request(self):
        ask.Request({})
