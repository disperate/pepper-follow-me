from threading import Thread

from follow_person_module import FollowPersonModule
from speech_module import SpeechModule


class FollowMe:
    def __init__(self, session):
        speech_event_listener = SpeechModule(session, "SpeechEventListener")
        follow_person_module = FollowPersonModule(session)

        self.follow_thread = Thread(target=follow_person_module.follow, args=[])
        self.speech_thread = Thread(target=speech_event_listener.subscribe_to_words,
                                    args=[follow_person_module.change_mode])

        self.speech_thread.start()
        self.follow_thread.start()

    def stop(self):
        self.speech_thread.do_run = False
        self.follow_thread.do_run = False

    def __del__(self):
        self.speech_thread.do_run = False
        self.follow_thread.do_run = False
