# Wall Ball Tracking App

Based on this: https://pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/



```
python3 ball_tracking.py --video ball_tracking_example.mp4
```

if you want to execute the script using your webcam rather than the supplied video file, simply omit the --video
switch:
```
python3 ball_tracking.py
```


# RGB Ball color range detector

https://github.com/PyImageSearch/imutils/blob/master/bin/range-detector


# Virtual Env

```
python3 -m venv myenv
source myenv/bin/activate
```

Deactivate:
```
deactivate
```

## Install modules

```
pip3 install imutils
pip3 install numpy
pip3 install opencv-python
```

## Run
```
python3 ball_tracking.py
```
Normal

```
python3 ball_tracking.py --camera 1 --frame-size 1200
```
* Using a USB camera
* Chaning the frame size to 1200


# Ball Detection

When the ball is moving fast, it looses tracking of it

Suggestions:

* Increase the frame rate.  If your camera or video source supports it, increase the frame rate
  can help capture more frames per second, which can improve tracking of fast-moving objects

* Adjust the color range: if the ball is not being detected in some frames because of changes in
  lighting or color, you can adjust the lower and uppoer boundaries of the color range used 
  to detect the green ball.

* I think we need to adjust the lower and upper bounds of the ball color.
* Could try out the range-detector script to see if that gets us the RGBs

* I think in some spots where the ball is too fast it is not detecting it b/c the ball
  is so faint in the video/picture.  

* You can only see a faint yellow blur going through

* Maybe we can set the sensitivity to something lower for the yellow?

* Try the better camera?

* Find an HSV thing that will look at an image and give it the blur ball?

* This guy says that the huff transform isnt so greate at tracking a fast ball but that can
  be fixed with an eliptical transform: https://www.youtube.com/watch?v=RaCwLrKuS1w


  I think it has something to do with when we blur and put it to grey scale and the ball
  is far away, it doesnt see it?
    * But it tracks it when it is slow....


* Another idea is to try to just track the ball color and not the ball itself?