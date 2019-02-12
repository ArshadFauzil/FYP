from __future__ import absolute_import
from detect_intent_texts import detect_intent_texts
import os


PROJECT_ID = os.getenv('GCLOUD_PROJECT')
SESSION_ID = 'fake_session_for_testing'
TEXTS = ["hello", "book a meeting room", "Mountain View",
         "tomorrow", "10 AM", "2 hours", "10 people", "A", "name please"]


def test_detect_intent_texts():
    detect_intent_texts(PROJECT_ID, SESSION_ID, TEXTS, 'en-US')


if __name__ == '__main__':
    test_detect_intent_texts()
