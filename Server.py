import requests
import os
import base64
import glob
import time
import subprocess  # Importing subprocess for better command execution

# Constants
ARCLIGHT_JAR_NAME = "arclight-fabric-1.21-1.0.0-SNAPSHOT.jar"  # Update this as needed
ARCLIGHT_URL = "https://github.com/IzzelAliz/Arclight/releases/download/FeudalKings%2F1.0.0-SNAPSHOT/arclight-fabric-1.21-1.0.0-SNAPSHOT.jar"  # Replace with the actual URL for the Arclight JAR
MIN_RAM = "4G"  # Adjust memory allocation as needed

# Remove "server.py" if it exists
if os.path.exists("server.py"):
    os.remove("server.py")

# Create .gitignore if it doesn't already exist
if not os.path.exists("./.gitignore"):
    big = "L1B5dGhvbioNCi93b3JrX2FyZWEqDQovc2Vydmlkb3JfbWluZWNyYWZ0DQovbWluZWNyYWZ0X3NlcnZlcg0KL3NlcnZpZG9yX21pbmVjcmFmdF9vbGQNCi90YWlsc2NhbGUtY3MNCi90aGFub3MNCi9zZXJ2ZXJzDQovYmtkaXINCi92ZW5kb3INCmNvbXBvc2VyLioNCmNvbmZpZ3VyYXRpb24uanNvbg0KY29uZmlndXJhY2lvbi5qc29uDQoqLnR4dA0KKi5weWMNCioubXNwDQoqLm91dHB1dA=="
    decoded_content = base64.standard_b64decode(big).decode()
    with open(".gitignore", 'w') as gitignore:
        gitignore.write(decoded_content)

# Function to download the latest release (MSP)
def download_latest_release(download_path='.'):
    mirror = "https://elyxdev.github.io/latest"
    response = requests.get(mirror)
    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError:
            print("Error: Received an invalid JSON response.")
            return None
        url = data.get('latest')
        version = url.split("/")[-1]
        if version in glob.glob("*.msp"):
            return version
        else:
            os.system("rm *.msp")
            print("Updating your MSP version...")
            time.sleep(1.5)
        path_to_file = os.path.join(download_path, version)
        with open(path_to_file, 'wb') as file:
            file.write(requests.get(url).content)
        return version
    else:
        print(f"Error: Unable to access {mirror}. Status code: {response.status_code}")
        return None

# Function to download the Arclight JAR if it doesn't exist
def download_arclight():
    if not os.path.exists(ARCLIGHT_JAR_NAME):
        print("Arclight JAR not found, downloading...")
        try:
            with open(ARCLIGHT_JAR_NAME, 'wb') as file:
                file.write(requests.get(ARCLIGHT_URL).content)
            print("Arclight JAR downloaded successfully.")
        except requests.RequestException:
            print("Error: Failed to download Arclight JAR.")

# Setup required directories for Arclight
def setup_arclight_directories():
    os.makedirs("mods", exist_ok=True)
    os.makedirs("plugins", exist_ok=True)
    print("Arclight directories 'mods' and 'plugins' are set up.")

# Execute the server (Arclight or MSP file)
filename = download_latest_release()
if filename and filename.split(".")[-1] == "msp":
    os.system(f"chmod +x {filename} && ./{filename}")
elif filename:
    os.system(f"python3 {filename}")
else:
    download_arclight()  # Ensure Arclight JAR is downloaded
    setup_arclight_directories()  # Ensure directories are set up
    # Launch the Arclight server using subprocess
    print("Starting Arclight server with 4GB of RAM...")
    subprocess.run(["java", "-Xms" + MIN_RAM, "-Xmx" + MIN_RAM, "-jar", ARCLIGHT_JAR_NAME, "nogui"])
