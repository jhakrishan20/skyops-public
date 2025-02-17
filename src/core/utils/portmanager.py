import os
import signal
import platform
import subprocess

class PortManager:
    @staticmethod
    def free_port(port):
       
        try:
            system = platform.system()

            if system == "Windows":
                # Find process using the port
                result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
                for line in result.stdout.splitlines():
                    if f":{port}" in line:
                        parts = line.split()
                        pid = parts[-1]  # PID is the last column
                        if pid.isdigit():
                            os.system(f"taskkill /F /PID {pid}")
                            print(f"✅ Process {pid} using port {port} has been killed.")

            else:  # Linux / macOS
                # Find process using the port
                result = subprocess.run(["lsof", "-i", f":{port}"], capture_output=True, text=True)
                for line in result.stdout.splitlines()[1:]:  # Skip the header
                    parts = line.split()
                    pid = parts[1]  # PID is in the second column
                    os.kill(int(pid), signal.SIGKILL)
                    print(f"✅ Process {pid} using port {port} has been killed.")

            print(f"Port is now free.")
            return True
        
        except Exception as e:
            print(f"❌ Error freeing port {port}: {e}")
            return False
