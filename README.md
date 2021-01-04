# SoundControl
A program i made so that i could control sound levels on my pc. (Switch to spotfiy when ads appear)

WINDOWS ONLY

Once the Macroserver.py is ran it will create a socket, wait for a client to
connect, receive data from client, and then close the connection.

HOW TO CONFIGURE Macroserver.py
    You can either configure the file dataforstart.py or MacroServer.py itself.
    
    the list "possibleprograms" is a list of recognized sound sources that will be recognized and show up.
    
    sometimes process names are not the most user friendly, therefore if there is an entry for a 
    process in "programdisplaynames" it will change the displayed string to its output.

    "presets" is a list that contains a list of presets that you can move through (I am not good at explaining this)

    IN MACROSERVER.py:
        towards the end of the macroserver.py file there should be a dict, within this dict you will find
        the Commands that the server can be given, it will then execute the corresponding function with parameter.

charSend.pyc:
    charSend takes a string as a parameter, opens a clients connection to the server and sends it.
    therefore this command would send the GetAllSoundSources command "pythonw directory/charSend.pyc GetAllSoundSessions"


HOW I USE IT
    By using HIDMacros i am executing the charSend.pyc file with a specific parameter thus sending it to the
    macroserver.py

    I use HIDMacros because it was the easiest keyboard HOOK to setup on windows 10(to my knowledge) and because it
    is capable of recognizing multiple devices, thus allowing me to have a Normal and a Macro keyboard.

    HIDMacros config:
	in the scripts tab:
		Dim wsh
                Set wsh = CreateObject("Wscript.Shell")
	
        keyconfigurations:
		wsh.Run "pythonw ""directory\charSend.pyc"" {COMMAND}"
	



LIST OF ALL FUNCTIONS THAT CAN DO STUFF
    funcname,  argument
    prevprogram, None
    nextprogram, None
    decsound, INT (Amount to decrease sound 0.0-1.0)
    incsound, INT
    setsound, INT (Amount to set time to, 0.0-1.0)
    terminate, None
    listprograms, None
    presetup. None
    presetdown, None
    savepreset, None
    clearallpresets, None
    removepresetprogram, None
    setpresetprogram, None
    getallsoundsources, None



Good luck, Youll need it.