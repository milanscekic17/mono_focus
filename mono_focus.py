from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume #type: ignore
from win32gui import GetWindowText, GetForegroundWindow
import time
import psutil
import win32process
import keyboard #type: ignore


def unmute():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            volume.SetMasterVolume(1, None)

def main():
    hotkey = input("Type the hotkey that you wish to use to toggle the program (e.g., 'ctrl+m' 'ctrl+shift+l' 'h' etc.) and press Enter: ")
    print(f"Press {hotkey} to toggle the program.")
    keyboard.wait(hotkey)
    print("Program started, all applications muted.")
    time.sleep(0.5)
    active = ''
    try: 
        while True:
            if keyboard.is_pressed(hotkey):
                unmute()
                print(f"Paused the program, all applications unmuted. Press {hotkey} to resume. Press Ctrl+C to exit.")
                time.sleep(0.5)
                keyboard.wait(hotkey)
                print("Resumed the program.")
                time.sleep(0.5)
            hwnd = GetForegroundWindow()
            if hwnd == 0:
                time.sleep(0.1)
                continue
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            try:
                process = psutil.Process(pid)
                if active != str(process.name()):
                    print(f"Active process: " + str(process.name()))
                active = str(process.name())
            except psutil.NoSuchProcess:
                print("Process no longer exists.")
                time.sleep(1)
                continue
            
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                if session.Process:
                    if session.Process.name() == active:
                        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                        volume.SetMasterVolume(1, None)
                        continue

                    else:
                        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                        volume.SetMasterVolume(0, None)

    except KeyboardInterrupt:
         unmute()
         raise SystemExit("Exiting the program.")
    
main()




