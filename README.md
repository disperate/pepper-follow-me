# FollowMe for Pepper
FollowMe is a python behaviour for letting Pepper follow you. Pepper is trying to stay about 0.5 m away from the person in his focus.
The behaviour is operated through voice commands.
## Oral Commands
Pepper listens to the following keywords:
* follow
* stop | stay

## API
To initialize the behaviour call
```python
follow_me_module = FollowMe(session)
```
The behaviour will listen to the oral commands as soon as the modul is initialized.  

You can stop the behaviour by calling:

```python
follow_me_module.stop()
```

## Limitations
* Pepper follows the first person found by the ALPeoplePerception service.
* ALPeoplePerception has troubles recognizing people in bright light.
* Pepper is slow (max. ~3 km/h)
* The security distances within the ALMotion services have been minimized to allow Pepper to walk through doors. We can't guarantee that the object avoidance will work properly. Take care. 

## Example usage
In [example.py](example.py) you can find a basic usage of the FollowMe modul.


```python
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
```

## Improvements
- [ ] Ask the person to slow down if Pepper can't follow.
- [ ] Ask person to get in front of Pepper if no one is recognized.
- [ ] Improve behaviour if pepper loses sight to person
