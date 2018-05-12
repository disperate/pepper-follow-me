from time import sleep

import qi

from follow_me import FollowMe

if __name__ == "__main__":

    connection_url = "amber.local:9559"
    app = qi.Application(["--qi-url=" + connection_url])
    app.start()

    session = app.session

    follow_me_module = FollowMe(session)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        follow_me_module.stop()
        print "Stopping..."
