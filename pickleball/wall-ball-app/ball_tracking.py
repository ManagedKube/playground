# import the necessary packages


# Lines 2-8 handle importing our necessary packages. We’ll be using deque
# , a list-like data structure with super fast appends and pops to maintain a list of the past N (x, y)-locations of the ball in our video stream. Maintaining such a queue allows us to draw the “contrail” of the ball as its being tracked.

# We’ll also be using imutils
# , my collection of OpenCV convenience functions to make a few basic tasks (like resizing) much easier. If you don’t already have imutils
# installed on your system, you can grab the source from GitHub or just use pip
# to install it:

# pip3 install --upgrade imutils

# From there, Lines 11-16 handle parsing our command line arguments. The first switch, --video
# is the (optional) path to our example video file. If this switch is supplied, then OpenCV will grab a pointer to the video file and read frames from it. Otherwise, if this switch is not supplied, then OpenCV will try to access our webcam.

# If this your first time running this script, I suggest using the --video
# switch to start: this will demonstrate the functionality of the Python script to you, then you can modify the script, video file, and webcam access to your liking.

# A second optional argument, --buffer
# is the maximum size of our deque
# , which maintains a list of the previous (x, y)-coordinates of the ball we are tracking. This deque
# allows us to draw the “contrail” of the ball, detailing its past locations. A smaller queue will lead to a shorter tail whereas a larger queue will create a longer tail (since more points are being tracked):

from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
ap.add_argument("-c", "--camera", type=int, default=0,
    help="camera to use (default=0)")
ap.add_argument("-f", "--frame-size", type=int, default=600,
    help="frame size (default=600)")
args = vars(ap.parse_args())





# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# https://github.com/PyImageSearch/imutils/blob/master/bin/range-detector
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
# greenLower = (120, 100, 50) # green
# greenUpper = (60, 100, 100) # yellow
pts = deque(maxlen=args["buffer"])
# if a video path was not supplied, grab the reference
# to the webcam
## src=0 is the default camera (the webcam in the monitor)
## src=1 is the second camera (could be plugged into the USB)
if not args.get("video", False):
	vs = VideoStream(src=args["camera"]).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)


# Lines 50 and 51 define the lower and upper boundaries of the color green in the HSV color space (which I determined using the range-detector script in the imutils
# library). These color boundaries will allow us to detect the green ball in our video file. Line 23 then initializes our deque
# of pts
# using the supplied maximum buffer size (which defaults to 64
# ).

# From there, we need to grab access to our vs
# pointer. If a --video
# switch was not supplied, then we grab reference to our webcam (Lines 27 and 28) — we use the imutils.video
# VideoStream
# threaded class for efficiency. Otherwise, if a video file path was supplied, then we open it for reading and grab a reference pointer on Lines 31 and 32 (using the built in cv2.VideoCapture
# ).




# Define the has_reversed_trajectory function
def has_reversed_trajectory(coords):
    if len(coords) < 3:
        return False

    # Filter out None values and non-tuple values
    coords = [coord for coord in coords if coord is not None and isinstance(coord, tuple)]

    dx = [(x2[0] - x1[0]) for (x1, y1), (x2, y2) in zip(coords, coords[1:])]
    dy = [(y2[0] - y1[0]) for (x1, y1), (x2, y2) in zip(coords, coords[1:])]

    reversed_x = dx[-1] * dx[-2] < 0 if len(dx) >= 2 else False
    reversed_y = dy[-1] * dy[-2] < 0 if len(dy) >= 2 else False

    return reversed_x or reversed_y




# keep looping
while True:
	# grab the current frame
	frame = vs.read()
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=args["frame_size"])
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)


    # Line 83 starts a loop that will continue until (1) we press the q
    # key, indicating that we want to terminate the script or (2) our video file reaches its end and runs out of frames.

    # Line 85 makes a call to the read
    # method of our camera
    # pointer which returns a 2-tuple. The first entry in the tuple, grabbed
    # is a boolean indicating whether the frame
    # was successfully read or not. The frame
    # is the video frame itself. Line 87 handles VideoStream
    # vs VideoCapture
    # implementations.

    # In the case we are reading from a video file and the frame is not successfully read, then we know we are at the end of the video and can break from the while
    # loop (Lines 90 and 91).

    # Lines 94-56 preprocess our frame
    # a bit. First, we resize the frame to have a width of 600px. Downsizing the frame
    # allows us to process the frame faster, leading to an increase in FPS (since we have less image data to process). We’ll then blur the frame
    # to reduce high frequency noise and allow us to focus on the structural objects inside the frame
    # , such as the ball. Finally, we’ll convert the frame
    # to the HSV color space.

    # Lines 100 handles the actual localization of the green ball in the frame by making a call to cv2.inRange
    # . We first supply the lower HSV color boundaries for the color green, followed by the upper HSV boundaries. The output of cv2.inRange
    # is a binary mask
    # , like this one:
    # Figure 2: Generating a mask for the green ball using the cv2.inRange function.
    # Figure 2: Generating a mask for the green ball using the cv2.inRange function.

    # As we can see, we have successfully detected the green ball in the image. A series of erosions and dilations (Lines 101 and 102) remove any small blobs that may be left on the mask.

    # Alright, time to perform compute the contour (i.e. outline) of the green ball and draw it on our frame
    # :






	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
	# update the points queue
	pts.appendleft(center)


        # We start by computing the contours of the object(s) in the image on Line 146 and `147`. On the subsequent line, make the function compatible with all versions of OpenCV. You can read more about why this change to cv2.findContours
        # is necessary in this blog post. We’ll also initialize the center
        # (x, y)-coordinates of the ball to None
        # on Line 149.

        # Line 151 makes a check to ensure at least one contour was found in the mask
        # . Provided that at least one contour was found, we find the largest contour in the cnts
        # list on Line 155, compute the minimum enclosing circle of the blob, and then compute the center (x, y)-coordinates (i.e. the “centroids) on Lines 157 and 158.

        # Line 160 makes a quick check to ensure that the radius
        # of the minimum enclosing circle is sufficiently large. Provided that the radius
        # passes the test, we then draw two circles: one surrounding the ball itself and another to indicate the centroid of the ball.

        # Finally, Line 167 appends the centroid to the pts
        # list.

        # The last step is to draw the contrail of the ball, or simply the past N (x, y)-coordinates the ball has been detected at. This is also a straightforward process:

    # Initialize a list to store the last 10 points
	last_10_pts = [None] * 10

    # Capture the original frame before making any changes to it
	original_frame = frame.copy()

	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

        ################################
        ## Adds the list of the last 10 points x, y to the frame with a black background

        # Update the list of the last 10 points
		last_10_pts.pop(0)
		last_10_pts.append((pts[i - 1], pts[i]))

        # Check if the trajectory has reversed
		reversed_trajectory = has_reversed_trajectory(last_10_pts)

        # To revert the frame back to its original state, restore the original frame
		frame = original_frame

        # If the trajectory has reversed, make the screen flash yellow
		# if reversed_trajectory:
		# 	frame[:] = [0, 255, 255]  # BGR color for yellow

        # Print the trajectory reversal information
		reversal_str = "Reversed trajectory" if reversed_trajectory else "Not reversed trajectory"

        # Add the reversal message to the list of points
		last_10_pts.append(reversal_str)

        # Make sure the list of points does not exceed 10 elements
		if len(last_10_pts) > 10:
			last_10_pts.pop(0)

        # Set the initial position for the text
		text_position = (10, frame.shape[0] - 10)

        # Draw a filled rectangle over the area where the text is drawn
		cv2.rectangle(frame, (0, frame.shape[0] - 200), (400, frame.shape[0]), (0, 0, 0), -1)

		# # Move the position up for the next point
		# text_position = (text_position[0], text_position[1] - 15)

        # Loop over the last 10 points and draw them on the frame
		for j, point in enumerate(reversed(last_10_pts)):
			if point is not None:
                 # Format the point as a string
				point_str = f"Point {j + 1}: {point}" if isinstance(point, tuple) else point

				# Draw the text on the frame
				cv2.putText(frame, point_str, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

				# Move the position up for the next point
				text_position = (text_position[0], text_position[1] - 15)

        ################################




        
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

    # Display the frame after applying GaussianBlur
	cv2.imshow("Blurred", blurred)

    # Display the HSV frame
	cv2.imshow("HSV", hsv)


# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
# otherwise, release the camera
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()


# We start looping over each of the pts
# on Line 190. If either the current point or the previous point is None
# (indicating that the ball was not successfully detected in that given frame), then we ignore the current index continue looping over the pts
# (Lines 193 and 194).

# Provided that both points are valid, we compute the thickness
# of the contrail and then draw it on the frame
# (Lines 197 and 198).

# The remainder of our ball_tracking.py
# script simply performs some basic housekeeping by displaying the frame
# to our screen, detecting any key presses, and then releasing the vs
# pointer.