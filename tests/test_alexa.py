from nose.tools import assert_equal, assert_dict_equal, assert_true

from .context import ask
from .fixtures.requests import (TEST_SESSION_ENDED_REQUEST, TEST_LAUNCH_REQUEST,
                                TEST_INTENT_REQUEST, UNRECOGNIZED_INTENT_REQUEST)


class TestVoiceHandler(object):

    def teardown(self):
        reload(ask)

    def test_defaults_on_init(self):
        assert_equal(ask.alexa._default, '_default_')
        assert_dict_equal(ask.alexa._handlers, {"IntentRequest": {}})

    def test_default_handler_decorator(self):

        @ask.alexa.default
        def some_logic():
            pass

        stored_function = ask.alexa._handlers[ask.alexa._default]
        assert_equal(stored_function, some_logic)

    def test_request_handler_decorator(self):
        request_type = "bar"

        @ask.alexa.request(request_type)
        def request_logic():
            pass

        stored_function = ask.alexa._handlers[request_type]
        assert_equal(stored_function, request_logic)

    def test_intent_handler_decorator(self):
        intent_type = "baz"

        @ask.alexa.intent(intent_type)
        def intent_logic():
            pass

        stored_function = ask.alexa._handlers['IntentRequest'][intent_type]
        assert_equal(stored_function, intent_logic)


class TestVoiceHandlerRouteRequest(object):

    @classmethod
    def setUpClass(cls):

        @ask.alexa.intent('GetZodiacHoroscopeIntent')
        def intent_logic(request):
            return ask.Response({'intent_handler_called': True})

        @ask.alexa.default
        def default_logic(request):
            return ask.Response({'default_handler_called': True})

        @ask.alexa.request('SessionEndedRequest')
        def request_logic(request):
            return ask.Response({'request_handler_called': True})


    @classmethod
    def tearDownClass(cls):
        reload(ask)  # in case these tests get run before TestVoiceHandler

    def test_routes_to_default_handler(self):
        req_json = UNRECOGNIZED_INTENT_REQUEST

        response = ask.alexa.route_request(req_json)
        assert_true(response['default_handler_called'])

    def test_routes_to_intent_handler(self):
        req_json = TEST_INTENT_REQUEST

        response = ask.alexa.route_request(req_json)
        assert_true(response['intent_handler_called'])

    def test_routes_to_request_handler(self):
        req_json = TEST_SESSION_ENDED_REQUEST

        response = ask.alexa.route_request(req_json)
        assert_true(response['request_handler_called'])
