from time import sleep


class FollowPersonModule:
    def __init__(self, session):

        self.motion_service = session.service("ALMotion")
        self.posture_service = session.service("ALRobotPosture")
        self.people_service = session.service("ALPeoplePerception")
        self.tracker_service = session.service("ALTracker")

        self.people_service.setFastModeEnabled(True)
        self.running = False

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

        # minimize Security Distance
        self.motion_service.setTangentialSecurityDistance(0.05)
        self.motion_service.setOrthogonalSecurityDistance(0.10)

        # Set the robot relative position to target
        # The robot stays a 50 centimeters of target with 10 cm precision
        self.tracker_service.setRelativePosition([-0.5, 0.0, 0.0, 0.1, 0.1, 0.3])

        print "FollowPersonModule successfully initiated."

    def follow(self):
        print("starting to follow")

        while True:
            sleep(1)
            if self.running:
                if not self.tracker_service.isActive():
                    print("tracker activated")
                    self.tracker_service.trackEvent(self.event_name)
                # print(self.motion_service.getOrthogonalSecurityDistance())
                # print(self.motion_service.getTangentialSecurityDistance())

                position = self.tracker_service.getTargetPosition(0)
                print(position)
                self.tracker_service.setRelativePosition([-0.5, 0.0, 0.0, 0.1, 0.1, 0.3])
            else:
                self.tracker_service.stopTracker()
                print("tracker deactivated")

        print "ALTracker stopped."

    def change_mode(self, text):
        if text == 'stop':
            self.running = False
        if text == 'follow':
            self.running = True
        print("callback, param was " + text)

    def __del__(self):
        self.tracker_service.stopTracker()
        self.tracker_service.unregisterAllTargets()
