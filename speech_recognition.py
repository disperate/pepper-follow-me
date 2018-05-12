import argparse
import sys
from time import sleep

import qi


class SpeechEventModule:
    def __init__(self, session, name):
        self.name = name
        self.asr_service = session.service("ALSpeechRecognition")
        memory = session.service("ALMemory")
        global memory

        self.asr_service.pause(True)
        self.asr_service.setLanguage("English")
        self.asr_service.setLanguage("German")
        self.asr_service.setLanguage("English")

        vocabulary = ["follow", "stop", "stay"]

        self.asr_service.setVocabulary(vocabulary, False)
        self.asr_service.pause(False)
        self.asr_service.subscribe(name)

    def __del__(self):
        self.asr_service.pause(True)
        self.asr_service.unsubscribe(self.name)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="amber.local",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
                                                                                              "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    SpeechEventListener = SpeechEventModule(session, "SpeechEventListener")

    last_word = ''
    threshold = 0.3

    while True:
        data = memory.getData("WordRecognized")
        word = data[0]
        certainty = data[1]

        if word != last_word and certainty > threshold:
            last_word = word

            if last_word == 'follow':
                print("follow")
            if last_word == 'stay' or last_word == 'stop':
                print("stop")

        sleep(0.2)
