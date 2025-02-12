import keyboard

def system(command):
    # Nested function to mute the system volume.
    def mute():
        keyboard.press_and_release("volume mute")  # Simulate the mute key press.

    # Nested function to unmute the system volume.
    def unmute():
        keyboard.press_and_release("volume mute")  # Simulate the unmute key press.

    # Nested function to increase the system volume.
    def volume_up():
        keyboard.press_and_release("volume up")  # Simulate the volume up key press.

    # Nested function to decrease the system volume.
    def volume_down():
        keyboard.press_and_release("volume down")  # Simulate the volume down key press.

    # Execute the appropriate command.
    if command == "mute":
        mute()
        return "Muted the system volume."
    elif command == "unmute":
        unmute()
        return "Unmute"
    elif command == "volume up":
        volume_up()
        return "Volume up"
    elif command == "volume down":
        volume_down()
        return "Volume down"
    return "Sorry I don't know how to do that"