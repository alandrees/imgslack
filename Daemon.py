import daemonize

import ProcessImageQueue

daemon = daemonize.Daemonize(app="ImgSlackProcessor",
                             pid="/tmp/imgslack",
                             action=ProcessImageQueue.process_image_queue)

daemon.start()
