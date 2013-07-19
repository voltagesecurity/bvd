#!/bin/bash
# Applescript for reloading Chrome upon deploy
osascript - <<!
tell application "Google Chrome" to activate
tell application "System Events"
    keystroke "r" using {command down, shift down}
    end tell
!
