from icecream import ic
import ARPTools as arp
import tkinter as tk
from tkinter import messagebox
import psutil
from icecream import ic
versionNUM = '0.3'
CPUName = arp.systemStatus()['CPUName']
drives = []
processes = []
processDict = {}

#function to try to kill a running process, and always closes the process window
def killP(processToKill, processwindow):
    processes = psutil.process_iter()
    for process in processes:
        if process.name() == processToKill:
            try:
                process.kill()
            except psutil.AccessDenied:
                messagebox.showerror(title='Access Denied', message=f'Access Denied to {processToKill}')
    processwindow.destroy()


def killWindow(x):
    global processDict
    x.destroy()
    killProcesses = []
    killprocessWindow = tk.Toplevel()
    # processes = psutil.process_iter()

    for i, process in enumerate(processDict.keys()):
        if i < 30:
            killProcesses.append(tk.Button(killprocessWindow, text=process, font=("Arial", 8), command=lambda x = process:killP(x, killprocessWindow)).grid(row=i, column=0))
        elif i < 60:
            killProcesses.append(tk.Button(killprocessWindow, text=process, font=("Arial", 8), command=lambda x = process:killP(x, killprocessWindow)).grid(row=i - 30, column=1))
        elif i < 90:
            killProcesses.append(tk.Button(killprocessWindow, text=process, font=("Arial", 8), command=lambda x = process:killP(x, killprocessWindow)).grid(row=i - 60, column=2))
        elif i < 120:
            killProcesses.append(tk.Button(killprocessWindow, text=process, font=("Arial", 8), command=lambda x = process:killP(x, killprocessWindow)).grid(row=i - 90, column=3))
        else:
            print('still need more room!')


def showAllProcess():
    global processDict
    processLabels = []
    processWindow = tk.Toplevel()
    labelFrame = tk.Frame(processWindow)
    for i, process in enumerate(processDict.keys()):
        if i < 30:
            processLabels.append(tk.Label(labelFrame, text=process, font=("Arial", 8)).grid(row=i, column=0))
        elif i < 60:
            processLabels.append(tk.Label(labelFrame, text=process, font=("Arial", 8)).grid(row=i-30, column=1))
        elif i < 90:
            processLabels.append(tk.Label(labelFrame, text=process, font=("Arial", 8)).grid(row=i-60, column=2))
        elif i < 120:
            processLabels.append(tk.Label(labelFrame, text=process, font=("Arial", 8)).grid(row=i-90, column=3))
        else:
            print('still need more room!')
    labelFrame.pack()
    killProcess = tk.Button(processWindow,
                            text='Terminate Mode',
                            font=("Arial", 8),
                            command=lambda: killWindow(processWindow)
                            )
    killProcess.pack()




def checkSystem():
    global CPUName
    global cpuRate
    global processCount
    global processes
    global driveCount
    global drives
    global processDict

    update = arp.systemStatus()
    count = 0
    drives = []
    processDict = {}
    for disk in update['disks']:
        if update['disks'][disk] != 'Non readable drive':
            count += 1
            drives.append((disk, update['disks'][disk]))
    driveCount.set(count)
    for process in update['processes']:
        processDict[process] = True
    processCount.set(f"{str(update['processNum'])} processes running")
    cpuRate.set(f"CPU load: {update['CPUload']}")
    main.after(1000, checkSystem)


main = tk.Tk()
main.title(f'Rio system monitor {versionNUM}')
processCount = tk.StringVar()
driveCount = tk.IntVar()
cpuRate = tk.StringVar()
checkSystem()
cpuFrame = tk.Frame(main)
cpuFrame.pack()
cpuLabel = tk.Label(cpuFrame, text=CPUName)
cpuLabel.pack()
cpuRateLabel = tk.Label(cpuFrame, textvariable=cpuRate)
cpuRateLabel.pack()

processFrame = tk.Frame(main)
processFrame.pack()
processLabel = tk.Label(processFrame, textvariable=processCount)
processLabel.pack()
processShowButton = tk.Button(processFrame, text='show all process', command=showAllProcess)
processShowButton.pack()

driveFrame = tk.Frame(main)
driveLabels = []
driveUsedSpace = []
for i, drive in enumerate(drives):
    driveUsed = arp.convert_size(drives[i][1].used)
    driveTotal = arp.convert_size(drives[i][1].total)
    driveText = f"{drives[i][0]}: {drives[i][1].percent}% Used ({driveUsed}) of {driveTotal} total"
    driveLabels.append(tk.Label(main, text=driveText).pack())

main.mainloop()
