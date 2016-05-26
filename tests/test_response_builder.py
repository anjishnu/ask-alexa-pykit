from nose.tools import assert_equal, assert_dict_equal

from .context import ask

RAW_TEMPLATE = {
    "version": "1.0",
    "response": {
        "outputSpeech": {
            "type": "PlainText",
            "text": "Some default text goes here."
                },
        "shouldEndSession": False
    }
}


class TestResponeHandler(object):
    def setup(self):
        self.default_speech = {"outputSpeech": {"type": "PlainText",
                                                "text": None}
                               }

    def test_response_builder_stores_base_response(self):
        assert_equal(RAW_TEMPLATE, ask.ResponseBuilder.base_response)

    def test_speech_defaults(self):
        output = ask.ResponseBuilder.create_speech()

        assert_dict_equal(output, self.default_speech)

    def test_speech_takes_message(self):
        message = 'My New Message'
        output = ask.ResponseBuilder.create_speech(message=message)

        assert_equal(output['outputSpeech']['text'], message)

    def test_speech_can_return_ssml_message(self):
        message = 'Yet another message'

        output = ask.ResponseBuilder.create_speech(message=message, is_ssml=True)

        assert_equal(output['outputSpeech']['type'], 'SSML')
        assert_equal(output['outputSpeech']['ssml'], message)

    def test_create_card_defaults(self):
        card = ask.ResponseBuilder.create_card()

        assert_dict_equal(card, {'type': 'Simple'})

    def test_create_card_adds_kwargs_when_present(self):
        expected = {'type': 'Simple', 'title': 'Welcome'}
        output = ask.ResponseBuilder.create_card(title='Welcome')
        assert_dict_equal(output, expected)

        expected = {'type': 'Simple', 'subtitle': 'some words'}
        output = ask.ResponseBuilder.create_card(subtitle='some words')
        assert_dict_equal(output, expected)

        expected = {'type': 'Simple', 'content': 'interesting info'}
        output = ask.ResponseBuilder.create_card(content='interesting info')
        assert_dict_equal(output, expected)

        expected = {'type': 'Something else'}
        output = ask.ResponseBuilder.create_card(card_type='Something else')
        assert_dict_equal(output, expected)
