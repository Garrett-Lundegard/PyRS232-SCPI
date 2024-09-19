import serial
import serial.tools.list_ports

def scan_serial_ports():
    # List all available ports
    ports = serial.tools.list_ports.comports()
    
    rs232_ports = []
    for port in ports:
        # Check if the port is an RS232 device based on description or other attributes
        if "RS232" in port.description or "Serial" in port.description:
            rs232_ports.append({
                "device": port.device,
                "description": port.description,
                "hwid": port.hwid
            })
    
    return rs232_ports

def query_device_identity(port_name):
    try:
        # Open the serial connection
        with serial.Serial(port=port_name, baudrate=9600, timeout=2) as ser:
            # Send the *IDN? query to get device identity
            ser.write(b'*IDN?\n')
            
            # Wait for and read the response
            response = ser.readline().decode().strip()
            return response
    except Exception as e:
        return f"Error querying device: {e}"

def measure_voltage(port_name):
    try:
        # Open the serial connection
        with serial.Serial(port=port_name, baudrate=9600, timeout=2) as ser:
            # Send the command to measure output voltage
            ser.write(b'MEAS:VOLT?\n')  # Corrected SCPI command for voltage measurement
            
            # Wait for and read the response
            response = ser.readline().decode().strip()
            return response
    except Exception as e:
        return f"Error measuring voltage: {e}"

def measure_current(port_name):
    try:
        # Open the serial connection
        with serial.Serial(port=port_name, baudrate=9600, timeout=2) as ser:
            # Send the command to measure output current
            ser.write(b'MEAS:CURR?\n')  # Corrected SCPI command for current measurement
            
            # Wait for and read the response
            response = ser.readline().decode().strip()
            return response
    except Exception as e:
        return f"Error measuring current: {e}"

def print_rs232_ports(rs232_ports):
    if rs232_ports:
        print("RS232/Serial devices found:")
        for idx, port in enumerate(rs232_ports):
            print(f"{idx + 1}. Device: {port['device']}, Description: {port['description']}, HWID: {port['hwid']}")
    else:
        print("No RS232 devices found.")

if __name__ == "__main__":
    rs232_ports = scan_serial_ports()
    print_rs232_ports(rs232_ports)
    
    if rs232_ports:
        # Ask user to choose a port if multiple are available
        selected_port = rs232_ports[0]['device']  # You can update this to prompt for a specific port
        
        # Query the identity of the connected device
        device_info = query_device_identity(selected_port)
        
        # Check if the device matches the 9115 Power Supply
        if "9115" in device_info:
            print(f"9115 Power Supply detected: {device_info}")
            
            # Measure and print the output voltage
            voltage = measure_voltage(selected_port)
            print(f"Output Voltage: {voltage} V")
            
            # Measure and print the output current
            current = measure_current(selected_port)
            print(f"Output Current: {current} A")
        else:
            print(f"Non-9115 device detected: {device_info}")
