import osascript
target_volume = 50
vol = "set volume output volume " + str(50)
osascript.osascript(vol)

# or
target_volume = 20
osascript.osascript("set volume output volume {}".format(target_volume))

