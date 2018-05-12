from threading import Thread

import qi

from follow_person import FollowPersonModule
from speech_recognition import SpeechModule

if __name__ == "__main__":
    connection_url = "amber.local:9559"
    app = qi.Application(["--qi-url=" + connection_url])
    app.start()
    session = app.session

    FollowPersonModule = FollowPersonModule(session)
    SpeechEventListener = SpeechModule(session, "SpeechEventListener")

    follow_thread = Thread(target=FollowPersonModule.follow, args=[])

    speech_thread = Thread(target=SpeechEventListener.subscribe_to_words, args=[FollowPersonModule.change_mode])

    speech_thread.start()
    follow_thread.start()
    speech_thread.join()
    follow_thread.join()
