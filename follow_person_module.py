import threading
from time import sleep


class FollowPersonModule:
    def __init__(self, session):
        self.do_run = True

        self.motion_service = session.service("ALMotion")
        self.posture_service = session.service("ALRobotPosture")
        self.people_service = session.service("ALPeoplePerception")
        self.tracker_service = session.service("ALTracker")

        self.tts = session.service("ALTextToSpeech")
        self.tts.setLanguage("English")
        self.tts.setParameter("speed", 90)

        self.people_service.setFastModeEnabled(True)
        self.running = False
        self.no_person_warning = True

        # First, wake up.
        self.motion_service.wakeUp()

        # Set Stiffness
        names = "Body"
        stiffness_lists = 1.0
        time_lists = 1.0
        self.motion_service.stiffnessInterpolation(names, stiffness_lists, time_lists)

        # Go to posture stand
        fraction_max_speed = 1.0
        self.posture_service.goToPosture("Standing", fraction_max_speed)

        # Set target to track.
        self.event_name = "People"

        # set mode
        mode = "Navigate"
        self.tracker_service.setMode(mode)
        self.tracker_service.trackEvent(self.event_name)

        # minimize Security Distance
        self.motion_service.setTangentialSecurityDistance(0.05)
        self.motion_service.setOrthogonalSecurityDistance(0.10)


        # Set the robot relative position to target
        # The robot stays a 50 centimeters of target with 10 cm precision
        self.tracker_service.setRelativePosition([-0.5, 0.0, 0.0, 0.1, 0.1, 0.3])

        print "FollowPersonModule successfully initiated."

    def follow(self):

        t = threading.currentThread()
        while getattr(t, "do_run", True):

            if self.running:

                self.tracker_service.trackEvent(self.event_name)
                    # print(self.motion_service.getOrthogonalSecurityDistance())
                    # print(self.motion_service.getTangentialSecurityDistance())

                position = self.tracker_service.getTargetPosition(0)
                if not position:
                    print("No person in sight")
                    if self.no_person_warning:
                        self.no_person_warning = False
                        self.tts.say("I cant see you. Please get in front of me.")

                print(position)

                self.tracker_service.setRelativePosition([-0.5, 0.0, 0.0, 0.1, 0.1, 0.3])
                #else:
                    #if self.tracker_service.isActive():
                    #    self.tracker_service.stopTracker()
                    #    print("tracker deactivated")
                sleep(1)
        print "FollowPersonModule stopped."

    def change_mode(self, text):
        if text == 'stop':
            self.running = False
        if text == 'follow':
            self.running = True
        print(text)

    def __del__(self):
        self.tracker_service.stopTracker()
        self.tracker_service.unregisterAllTargets()
