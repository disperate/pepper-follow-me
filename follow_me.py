#! /usr/bin/env python
# -- encoding: UTF-8 --

"""Example: Use Tracking Module to Track an Object"""

import time

import qi


def main(session):
    """
    This example shows how to use ALTracker to track an object with trackEvent api.
    This example is only a subscriber. You need to create another script to raise the tracked event.
    Your events should follow this structure :
        EventNameInfo {
          TargetPositionInFrameWorld,
          TimeStamp,
          EffectorId,
          HeadThreshold (optional)
          }
    All details are available in ALTracker API Documentation.
    """
    # Get the services ALTracker, ALMotion and ALRobotPosture.

    motion_service = session.service("ALMotion")
    memory_service = session.service("ALMemory")
    posture_service = session.service("ALRobotPosture")
    people_service = session.service("ALPeoplePerception")
    tracker_service = session.service("ALTracker")
    engagement_service = session.service("ALEngagementZones")
    asr_service = session.service("ALSpeechRecognition")

    people_service.setFastModeEnabled(True)

    # First, wake up.
    motion_service.wakeUp()

    # Set Stiffness
    names = "Body"
    stiffnessLists = 1.0
    timeLists = 1.0
    motion_service.stiffnessInterpolation(names, stiffnessLists, timeLists)

    # Go to posture stand
    fractionMaxSpeed = 1.0
    posture_service.goToPosture("Standing", fractionMaxSpeed)

    # Set target to track.
    eventName = "People"

    # set mode
    mode = "Navigate"
    tracker_service.setMode(mode)

    # Disable Security Distance
    motion_service.setTangentialSecurityDistance(0.05)
    motion_service.setOrthogonalSecurityDistance(0.10)

    # Set the robot relative position to target
    # The robot stays a 50 centimeters of target with 10 cm precision
    tracker_service.setRelativePosition([-0.5, 0.0, 0.0, 0.1, 0.1, 0.3])

    # Then, start tracker.
    tracker_service.trackEvent(eventName)

    # Speech Recognition
    # Example: Adds "yes", "no" and "please" to the vocabulary (without wordspotting)
    # vocabulary = ["follow", "stop"]
    # asr_service.pause(True)
    # asr_service.setVocabulary(vocabulary, True)
    # asr_service.pause(False)

    # Start the speech recognition engine with user Test_ASR
    # asr_service.subscribe("Test_ASR")
    # print 'Speech recognition engine started'


    print "ALTracker successfully started."
    print "Use Ctrl+c to stop this script."

    try:
        while True:
            time.sleep(1)
            print(motion_service.getOrthogonalSecurityDistance())
            print(motion_service.getTangentialSecurityDistance())
            position = tracker_service.getTargetPosition(0)
            print(position)
            tracker_service.setRelativePosition([-0.5, 0.0, 0.0, 0.1, 0.1, 0.3])


    except KeyboardInterrupt:
        print
        print "Interrupted by user"
        print "Stopping..."

    # Stop tracker, go to posture Sit.
    tracker_service.stopTracker()
    tracker_service.unregisterAllTargets()
    # posture_service.goToPosture("Sit", fractionMaxSpeed)
    # motion_service.rest()

    print "ALTracker stopped."


if __name__ == "__main__":
    connection_url = "amber.local:9559"
    app = qi.Application(["--qi-url=" + connection_url])
    app.start()
    session = app.session
    main(session)
