import socket
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

HOST = '0.0.0.0'
PORT = 26754      # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen()


intProgram = -1

possibleprograms = ["Spotify.exe",
                    "firefox.exe"]

programdisplaynames = {
    "Spotify.exe": "Spotify",
    "firefox.exe": "Firefox"
}

presets = [[["Spotify.exe", 0.00], ["firefox.exe", 0.50]],
           [["Spotify.exe", 0.50], ["firefox.exe", 0.00]]]

try:  # adds data from datafile
    from dataforstart import programdisplaynames as dict, possibleprograms as list, prelist
    presets += prelist
    possibleprograms += list
    programdisplaynames.update(dict)
except ModuleNotFoundError:
    print("Didn't find datafile 'dataforstart.py'")


programdisplayname = ""
programs = []
program = None
programsession = None
programsessionvol = None


class SkipError(Exception):
    pass


def getprogramdisplayname():
    global programdisplayname, program, programdisplayname
    try:
        programdisplayname = programdisplaynames[program]
    except KeyError:
        programdisplayname = program


def clearout():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"*3)


def terminate(_):
    exit()


def listprograms(_):
    global programs, possibleprograms, intProgram
    tempprograms = []
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() in possibleprograms:
            tempprograms.append(session.Process.name())

    if len(tempprograms) == 0:
        raise SkipError()

    if programs == tempprograms:
        updatestatus(str(tempprograms) + str(intProgram))
        return str(programs)
    programs = tempprograms[:]
    intProgram = -1
    nextprogram(None)
    return str(programs)


#  preset dummy [["firefox.exe", 0.5], ["Spotify.exe", 0.0],
#                ["firefox.exe", 0.0], ["Spotify.exe", 0.5]]

preset = -1
presetnext = []


def loadpreset():
    global preset, presets, presetnext

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() in possibleprograms:
            name = session.Process.name()
            for loading in presets[preset]:
                if name == loading[0]:
                    session._ctl.QueryInterface(ISimpleAudioVolume).SetMasterVolume(loading[1], None)
                    
    if preset == len(presets)-1:
        presetnext = presets[0]
    else:
        presetnext = presets[preset+1]

    return ""


def presetup(_):
    global preset, presets
    if len(presets) < 1:
        return "Not enough presets to change"

    preset += 1

    if preset >= len(presets):
        preset = 0

    return loadpreset()


def presetdown(_):
    global preset, presets
    if len(presets) < 1:
        return "Not enough presets to change"

    preset -= 1

    if preset < 0:
        preset = len(presets)-1

    return loadpreset()


def savepreset(_):
    global programs, presets, preset, presetnext
    sessions = AudioUtilities.GetAllSessions()
    temppresets = []
    for session in sessions:
        if session.Process and session.Process.name() in programs:
            vol = session._ctl.QueryInterface(ISimpleAudioVolume).GetMasterVolume()
            temppresets.append([session.Process.name(), vol])

    presets.append(temppresets)
    
    preset = len(presets)-1
    
    presetnext = presets[0]

    return presets


def clearallpresets(_):
    global preset, presets
    preset = -1
    presets = []
    return "presets deleted"


def setpresetprogram(_):
    global preset, presets, program, programsessionvol
    if len(presets) == 0:
        preset = 0
        presets.append([[program, programsessionvol.GetMasterVolume()]])
        return f"Made preset with {program}"
    for integer, loading in enumerate(presets[preset]):
        if loading[0] == program:
            presets[preset][integer][1] = programsessionvol.GetMasterVolume()
            return f"Redefined {program} in current preset"

    presets[preset].append([program, programsessionvol.GetMasterVolume()])
    return f"Added {program} to current preset"



def removepresetprogram(_):
    global preset, presets, program
    if len(presets) == 0:
        pass
    for integer, loading in enumerate(presets[preset]):
        if loading[0] == program:
            presets[preset].pop(integer)


def nextprogram(_):
    global intProgram, programs, program, programsession, programsessionvol
    intProgram += 1
    if intProgram >= len(programs):
        intProgram = 0
    program = programs[intProgram]
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == program:
            programsession = session
            programsessionvol = programsession._ctl.QueryInterface(ISimpleAudioVolume)
            getprogramdisplayname()
            return ""
    listprograms(None)
    return ""


def prevprogram(_):
    global intProgram, programs, program, programsession, programsessionvol
    intProgram -= 1
    if intProgram < 0:
        intProgram = len(programs)-1
    program = programs[intProgram]
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == program:
            programsession = session
            programsessionvol = programsession._ctl.QueryInterface(ISimpleAudioVolume)
            getprogramdisplayname()
            return ""
    listprograms(None)
    return ""


def getallsoundsources(_):
    all = ""

    sess = AudioUtilities.GetAllSessions()
    for currsess in sess:
        try:
            currsess
            all += f" - {currsess.Process.name()} - "
        except:
            all += " - UNKNOWN - "

    return all


def decsound(vol):
    global programsession, programsessionvol
    x = programsessionvol.GetMasterVolume() - vol
    if x < 0:
        x = 0
    programsessionvol.SetMasterVolume(x, None)
    return "VOL:" + str(int(x*100+0.5))


def incsound(vol):
    global programsession, programsessionvol
    x = programsessionvol.GetMasterVolume() + vol
    if x > 1:
        x = 1
    programsessionvol.SetMasterVolume(x, None)
    return "VOL:" + str(int(x*100+0.5))
    

def setsound(vol):
    global programsession, programsessionvol
    programsessionvol.SetMasterVolume(vol, None)
    return "VOL:" + str(int(vol*100+0.5))


def updatestatus(preline):
    global intProgram, programs, program, programsessionvol, presets, preset, presetnext
    clearout()
    if intProgram+1 >= len(programs):
        programnext = programs[0]
    else:
        programnext = programs[intProgram+1]

    try:
        programnext = programdisplaynames[programnext]
    except KeyError:
        pass
    
    presetline = ""

    if len(presets) > 0:
        tempfirst = ""
        tempsecond = ""
        for thing in presets[preset]:
            tempfirst += f"({thing[0]}, {thing[1]:.2f})"

        for thing in presetnext:
            tempsecond += f"({thing[0]}, {thing[1]:.2f})"

        presetline = f"Preset: {tempfirst}   -->-->-->-->   {tempsecond}"

    print(f"{preline}\n"
          f"\n"
          f" - Process: {programdisplayname}   -->-->-->-->   {programnext}\n"
          f"        - VOL: {int(programsessionvol.GetMasterVolume()*100+0.5)}\n"
          f"\n"
          f"\n"
          f"\n"
          f"{presetline}\n",
          end="\n")


funcdict = {
    "ArrLeft": (prevprogram, None),
    "ArrRight": (nextprogram, None),
    "NumPad3": (decsound, 0.25),
    "NumPad2": (decsound, 0.05),
    "NumPad1": (decsound, 0.01),
    "NumPad9": (incsound, 0.25),
    "NumPad8": (incsound, 0.05),
    "NumPad7": (incsound, 0.01),
    "NumPad4": (setsound, 0),
    "NumPad6": (setsound, 1),
    "NumPad5": (setsound, 0.5),
    "Backspace": (terminate, None),
    "UpdateSS": (listprograms, None),
    "ArrUp": (presetup, None),
    "ArrDown": (presetdown, None),
    "SavePreset": (savepreset, None),
    "ClearAllPresets": (clearallpresets, None),
    "RemovePresetProgram": (removepresetprogram, None),
    "SetPresetProgram": (setpresetprogram, None),
    "GetAllSoundSources": (getallsoundsources, None)
}

errormessage = "An error has occurred, plausible causes:\n" \
               "  Received key is unknown.\n" \
               "  Program couldn't recognize any programs.\n" \
               "\n" \
               "\n" \
               "Hopefully the idiot creator of this can help -theinsignificantdoll\n"

try:
    listprograms(None)
    nextprogram(None)
    updatestatus("Started")
except SkipError:
    pass

conn = False
previouscommands = []

while True:
    try:
        while True:
            if conn:
                conn.close()

            s.listen()
            conn, addr = s.accept()
            data = conn.recv(1024).decode("utf-8", "ignore")

            try:
                print(data)
                if program is None:

                    try:
                        listprograms(None)
                        nextprogram(None)
                    finally:
                        raise SkipError

                returned = funcdict[data][0](funcdict[data][1])
                updatestatus(f"{data}        {returned}")
                conn.close()

            except ModuleNotFoundError:  #(KeyError, SkipError):
                print(errormessage)
                print(data)

    except (ConnectionResetError): # OSError):
        print("DISCONNECTED / ERROR")
