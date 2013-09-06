# ExRelease Export v0.2
# Author: Southrop
# This macro is designed to be used with AVS scripts generated by ExRelease for quick and easy exporting of bookmarked frames.

import os.path
import pyavs

tabcount = avsp.GetTabCount()
count = 0

for n in range(0,tabcount):
	# Sets output directory to the current working directory (where the main video file is stored)
	vidpath = avsp.GetVar('vidfile', index=n)
	dirname = os.path.dirname(vidpath)
	
	# Sets filenames to #####_Group.png format, where ##### is the frame number
	basename = ur'%06d_' + avsp.GetVar('group', index=n) + '.png'
	
	filename = os.path.join(dirname, basename)
	
	# ------------------------------------------------------------------------------
	
	self = avsp.GetWindow()
	
	AVS = pyavs.AvsClip(avsp.GetText(clean=True), matrix=self.matrix, interlaced=self.interlaced, swapuv=self.swapuv)
	if AVS.IsErrorClip():
		avsp.MsgBox(AVS.error_message, 'Error')
		return
	
	# Get list of frames
	frame_count = avsp.GetVideoFramecount()
	bookmarks = avsp.GetBookmarkList()
	if bookmarks:
		frames = sorted(filter(lambda x: x < frame_count, set(bookmarks))),
	else:
		avsp.MsgBox('There are no bookmarks set.', 'Error')
		return
	
	# Save the images
	paths = []
	for i, frame_range in enumerate(frames):
		frame_index = len(paths) + 1
		for j, frame in enumerate(frame_range):
			ret = self.SaveImage(filename % (frame), frame=frame, avs_clip=AVS, quality=100, depth=8)
			if not ret:
				break
			paths.append(ret)
	
	count += len(paths)

avsp.MsgBox(str(count)+' images ('+str(count/tabcount)+' for each of '+str(tabcount)+' releases) created.', 'Information')
return 0