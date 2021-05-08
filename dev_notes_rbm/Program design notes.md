# Designing the interface
- Implement a CLI that takes some basic args, like, 
	- background arguments: 
		- -v --virtual
			Takes a path to a virtual background image to superimpose behind you
		- -c --color
			Color name (red, yellow, blue, etc.)
		- -b --blur
			Blur. Int input. Determines the strength of the gaussian blur
		- They should all be optional. 
			- If unspecified, default to blur. 
	- -t --time
		-	Print out time statistics per frame. 
		- optional. If unspecified, default to false. 
	- -d --debug
		- Debug mode. Print out statistics to image frames. 
		- optional. If unspecified, default to false.
	- -o --out
		- Out path for images. Directory. 
		- optional. If unspecified, default to writing to the system time or some rand seed. 
	- -i --in
		- In path for image, or directory of images. 
			- If directory, applies the specified effect across all images. 
		- optional. If unspecified, default to reading from the webcam. 
	- -v --video
		- If specified, stitch the images into a video. 
		- Optional. If unspecified, default to just writing images into a folder. 
- So a sample usage could be as simple as
	- python main.py 
	- in which case, we would read from the webcam, apply a standard blur, and write to 
		a randomly named output folder in the program directory. 