import threading
from time import sleep


class SpeechModule:
    def __init__(self, session, name):
        self.do_run = True
        self.name = name
        self.asr_service = session.service("ALSpeechRecognition")
        self.memory = session.service("ALMemory")

        self.tts = session.service("ALTextToSpeech")
        self.tts.setLanguage("English")
        self.tts.setParameter("speed", 90)

        self.asr_service.pause(True)

        # hack to prevent dictionary already set error
        self.asr_service.setLanguage("English")
        self.asr_service.setLanguage("German")
        self.asr_service.setLanguage("English")

        vocabulary = ["follow", "stop", "stay"]

        self.asr_service.setVocabulary(vocabulary, False)
        self.asr_service.pause(False)
        self.asr_service.subscribe(name)

        print "SpeechEventModule successfully initiated."

    def __del__(self):
        self.asr_service.pause(True)
        self.asr_service.unsubscribe(self.name)

    def subscribe_to_words(self, callback):

        try:
            self.memory.removeData("WordRecognized")
        except RuntimeError:
            print("failed to remove WordRecognized")
        last_word = ''
        threshold = 0.30

        t = threading.currentThread()
        while getattr(t, "do_run", True):
            try:
                data = self.memory.getData("WordRecognized")
                word = data[0]
                certainty = data[1]

                if word != last_word and certainty > threshold:
                    last_word = word

                    if last_word == 'follow':
                        callback("follow")
                        self.tts.say("Let's go")

                    if last_word == 'stay' or last_word == 'stop':
                        callback("stop")
                        self.tts.say("I will stay here. Bye.")

            except RuntimeError:
                print("getData WordRecognized is empty")

            sleep(0.1)

        print "SpeechModule stopped."
