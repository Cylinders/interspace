import win32api
import serial.tools.list_ports
import serial
import time
import tkinter as tk
from tkinter import ttk

def driveLetterLoad():
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print(f"Checking drive {letter}:\\")
        try:
            if(win32api.GetVolumeInformation(letter + ":\\")[0] == "INTERSPACE"):
                print(f"Found INTERSPACE drive at {letter}:\\")
                return letter
        except Exception as e:
            pass
    print("INTERSPACE drive not found")
    return -1

def findPort():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No ports found!")
        return -1

    # Filter only "good" ports
    good_ports = []
    for p in ports:
        if p.description and "USB Serial" in p.description:
            good_ports.append(p)
        elif p.manufacturer and "Raspberry" in p.manufacturer:
            good_ports.append(p)

    if len(good_ports) == 0:
        print("No matching device found.")
        return -1

    if len(good_ports) == 1:
        print(f"Automatically selected {good_ports[0].device}")
        return good_ports[0].device

    # If multiple good ports found, pop up a selector window
    def select_port():
        selected = combo.get()
        if selected:
            nonlocal selected_port
            selected_port = selected.split(' ')[0]  # Get COMx part
            window.destroy()

    selected_port = None
    window = tk.Tk()
    window.title("Select Your Device")
    window.geometry("500x200")
    label = tk.Label(window, text="Select the Interspace Device:", font=('Arial', 14))
    label.pack(pady=10)

    port_list = []
    for p in good_ports:
        desc = f"{p.device} - {p.description} - {p.manufacturer}"
        port_list.append(desc)

    combo = ttk.Combobox(window, values=port_list, font=('Arial', 12), width=60)
    combo.pack(pady=10)
    if port_list:
        combo.current(0)

    select_button = tk.Button(window, text="Select", command=select_port, font=('Arial', 12))
    select_button.pack(pady=10)

    window.mainloop()
    return selected_port if selected_port else -1

class Interspace():
    def __init__(self):
        self.driveLetter = driveLetterLoad()
        self.port = findPort()
        self.LP = -1
        self.ser = None

        if self.port == -1:
            print("ERROR: Could not find a suitable serial port!")
        else:
            try:
                # Set timeout to prevent blocking forever
                self.ser = serial.Serial(self.port, 115200, timeout=1)
                print(f"Successfully opened serial port {self.port}")
                # Flush any existing data
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()
            except Exception as e:
                print(f"ERROR opening serial port: {e}")
                self.port = -1

        if self.driveLetter == -1:
            print("ERROR: Could not find INTERSPACE drive!")
        else:
            try:
                with open(f"{self.driveLetter}:\\self.txt", "r") as f:
                    self.LP = f.read().strip().split("\n")[0]
                    print(f"Loaded LP: {self.LP}")
            except Exception as e:
                print(f"ERROR reading self.txt: {e}")
                self.driveLetter = -1

    def is_connected(self):
        return self.port != -1 and self.driveLetter != -1 and self.ser is not None

    def sendMessage(self, target: str, cont: str):
        if not self.is_connected():
            print("ERROR: Device not properly connected")
            return False

        try:
            with open(f"{self.driveLetter}:\\comms.txt", "w") as f:
                f.write(f"m\n{target}\n{self.LP}\n{cont}")
            return True
        except Exception as e:
            print(f"ERROR sending message: {e}")
            return False

    def sendGps(self):
        if not self.is_connected():
            print("ERROR: Device not properly connected")
            return False

        try:
            with open(f"{self.driveLetter}:\\comms.txt", "w") as f:
                f.write("g")
            return True
        except Exception as e:
            print(f"ERROR sending GPS request: {e}")
            return False

    def readMessage(self, timeout=100):
        """
        Read a message from the serial port.

        Args:
            timeout: Number of iterations to try reading (not seconds)

        Returns:
            The message string if successful, -1 otherwise
        """
        if not self.is_connected():
            print("ERROR: Device not properly connected")
            return -1

        print("Beginning read loop")
        for i in range(timeout):
            print(f"Loop iteration: {i}")

            try:
                # Check if data is available before attempting to read
                if self.ser.in_waiting > 0:
                    serIn = self.ser.readline().strip().decode("utf8")
                    print(f"Received: {serIn}")
                    if serIn.startswith("interspace1.0"):
                        return serIn[13:]
                    elif serIn.startswith("interspaceg1.0"):
                        try:
                            return float(serIn[14:])
                        except:
                            pass
                else:

                    # Small pause to prevent CPU maxing out
                    time.sleep(0.1)

                    # Every 10 iterations, print status
                    if i % 10 == 0 and i > 0:
                        print(f"Waiting for data... ({i}/{timeout})")

            except Exception as e:
                print(f"ERROR reading from serial: {e}")

        print(f"Timeout after {timeout} iterations without receiving proper message")
        return -1

    def close(self):
        """Close serial connection and clean up"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial connection closed")

if __name__ == "__main__":
    api = Interspace()

    if api.is_connected():
        print("Interspace initialized successfully")
        print("Waiting for message...")
        result = api.readMessage(timeout=50)
        print(f"Read result: {result}")
    else:
        print("Failed to initialize Interspace properly")

    # Always close properly
    api.close()
