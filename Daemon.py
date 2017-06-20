"""
Copyright 2017 Pirate Hour Productions

Author: Alan Drees

Purpose: Implement a daemon wrapper around the ProcessImageQueue module
"""
import daemonize
import argparse

import ProcessImageQueue

daemon = daemonize.Daemonize(app="ImgSlackProcessor",
                             pid="/tmp/imgslackprocessor.pid",
                             action=ProcessImageQueue.process_image_queue)

daemon.start()
