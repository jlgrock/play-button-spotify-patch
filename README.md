Play Button Spotify patch
========================


Overview
--------
This is a patch for removing the default OS X behavior of _always_ starting
iTunes when the play button on the keyboard is pressed.  This feature can be
useful for a lot of users, but it can also be annoying if iTunes isn't your _"go to"_ application.

The Patch script will patch the Remote Control Daemon to replace the starting of
iTunes whenever you press the play button to starting Spotify on the keyboard or an external remote control. This will only prevent iTunes from starting, all other functions (like play/pause while iTunes is _running_) will continue to work as before.

Lastly, this program will backup the original file in case if you would like to
restore the original functionality.


General Information
-------------------
This is a fork from a project from [Farhan Ahmad](https://github.com/thebitguru/play-button-itunes-patch), which disabled the play button until an application had started up.

To run the patch (which does the backup automatically), clone this repository and double click on the file **Patch.command**.
