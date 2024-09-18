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
