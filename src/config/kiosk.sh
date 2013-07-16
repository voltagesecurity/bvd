#!/bin/bash
# Applescript for loading BVD in Chrome at login
open -a '/Applications/Google Chrome.app' --args http://localhost
sleep 5
osascript - <<!
tell application "Google Chrome" to activate
tell application "System Events"
    keystroke "f" using {command down, shift down}
    end tell
!
