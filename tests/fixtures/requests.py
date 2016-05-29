# -*- coding: utf-8 -*-

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
        },
        "new": True
    },
    "request": {
        "type": "IntentRequest",
        "requestId": "EdwRequestId.b22db637-b8f9-43c0-ae0c-1a9b35a02610",
        "timestamp": 1447911387582,
    }
}

TEST_SESSION_ENDED_REQUEST = {
    "version": "1.0",
    "session": {
        "new": False,
        "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
        "application": {
            "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
        },
        "attributes": {
            "supportedHoroscopePeriods": {
                "daily": True,
                "weekly": False,
                "monthly": False
            }
        },
        "user": {
            "userId": "amzn1.account.AM3B00000000000000000000000"
        }
    },
    "request": {
        "type": "SessionEndedRequest",
        "requestId": "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
        "timestamp": "2015-05-13T12:34:56Z",
        "reason": "USER_INITIATED"
    }
}

TEST_LAUNCH_REQUEST = {
    "version": "1.0",
    "session": {
        "new": True,
        "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
        "application": {
            "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
        },
        "attributes": {},
        "user": {
            "userId": "amzn1.account.AM3B00000000000000000000000"
        }
    },
    "request": {
        "type": "LaunchRequest",
        "requestId": "amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
        "timestamp": "2015-05-13T12:34:56Z"
    }
}


TEST_INTENT_REQUEST = {
  "version": "1.0",
  "session": {
    "new": False,
    "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
    },
    "attributes": {
      "supportedHoroscopePeriods": {
        "daily": True,
        "weekly": False,
        "monthly": False
      }
    },
    "user": {
      "userId": "amzn1.account.AM3B00000000000000000000000"
    }
  },
  "request": {
    "type": "IntentRequest",
    "requestId": " amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
    "timestamp": "2015-05-13T12:34:56Z",
    "intent": {
      "name": "GetZodiacHoroscopeIntent",
      "slots": {
        "ZodiacSign": {
          "name": "ZodiacSign",
          "value": "virgo"
        }
      }
    }
  }
}

UNRECOGNIZED_INTENT_REQUEST = {
  "version": "1.0",
  "session": {
    "new": False,
    "sessionId": "amzn1.echo-api.session.0000000-0000-0000-0000-00000000000",
    "application": {
      "applicationId": "amzn1.echo-sdk-ams.app.000000-d0ed-0000-ad00-000000d00ebe"
    },
    "attributes": {
      "supportedHoroscopePeriods": {
        "daily": True,
        "weekly": False,
        "monthly": False
      }
    },
    "user": {
      "userId": "amzn1.account.AM3B00000000000000000000000"
    }
  },
  "request": {
    "type": "IntentRequest",
    "requestId": " amzn1.echo-api.request.0000000-0000-0000-0000-00000000000",
    "timestamp": "2015-05-13T12:34:56Z",
    "intent": {
      "name": "thisisnottheintentyouarelookingfor",
      "slots": {
        "ZodiacSign": {
          "name": "ZodiacSign",
          "value": "virgo"
        }
      }
    }
  }
}
