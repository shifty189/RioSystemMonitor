from icecream import ic
import ARPTools as arp
import tkinter as tk
versionNUM = '0.1'
CPUName = arp.systemStatus()['CPUName']
cpuRate = ''
drives = []
processes = []
processDict = {}
colors = {
    "CPU": "Red",
    "Drive": "Blue",
    "Process": "Green",
    "Network": "Teal"
}


def showAllProcess():
    global processDict

    processLabels = []
    processWindow = tk.Toplevel()
    for i, process in enumerate(processDict.keys()):
        if i < 30:
            processLabels.append(tk.Label(processWindow, text=process).grid(row=i, column=0))
        elif i < 60:
            processLabels.append(tk.Label(processWindow, text=process).grid(row=i-30, column=1))
        elif i < 90:
            processLabels.append(tk.Label(processWindow, text=process).grid(row=i-60, column=2))
        elif i < 120:
            processLabels.append(tk.Label(processWindow, text=process).grid(row=i-90, column=3))
        else:
            print('still need more room!')




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
            drives.append(disk)
    driveCount.set(count)
    for process in update['processes']:
        processDict[process] = True
    processCount.set(f"{str(update['processNum'])} processes running")
    cpuRate = update['cpuRate']
    main.after(1500, checkSystem)


main = tk.Tk()
main.title(f'Rio system monitor {versionNUM}')
processCount = tk.StringVar()
driveCount = tk.IntVar()
checkSystem()
cpuFrame = tk.Frame(main)
cpuFrame.pack()
cpuLabel = tk.Label(cpuFrame, text=CPUName, bg=colors['CPU'])
cpuLabel.pack()
cpuRateLabel = tk.Label(cpuFrame, text=f"CPU load: {cpuRate}")
cpuRateLabel.pack()

processFrame = tk.Frame(main)
processFrame.pack()
processLabel = tk.Label(processFrame, textvariable=processCount, bg=colors['Process'])
processLabel.pack()
processShowButton = tk.Button(processFrame, text='show all process', command=showAllProcess)
processShowButton.pack()

driveFrame = tk.Frame(main)
driveLabels = []
driveUsedSpace = []
for i, drive in enumerate(drives):
    driveLabels.append(tk.Label(main, text=drives[i], bg=colors['Drive']).pack())

main.mainloop()
