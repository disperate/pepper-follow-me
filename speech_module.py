from time import sleep


class SpeechModule:
    def __init__(self, session, name):
        self.name = name
        self.asr_service = session.service("ALSpeechRecognition")
        self.memory = session.service("ALMemory")

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

    def follow(self):
        print("starting to follow in speech")

    def subscribe_to_words(self, callback):
        print("starting to wait for words")
        last_word = ''
        threshold = 0.3

        while True:
            data = self.memory.getData("WordRecognized")
            word = data[0]
            certainty = data[1]
            # print(data)
            if word != last_word and certainty > threshold:
                last_word = word

                if last_word == 'follow':
                    print("follow")
                    callback("follow")

                if last_word == 'stay' or last_word == 'stop':
                    print("stop")
                    callback("stop")

            sleep(0.1)
