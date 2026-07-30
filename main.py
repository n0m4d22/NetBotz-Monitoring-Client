"""CLI menu, thread orchestration, and user input."""

import threading
from lib import daemon

NETBOTZ_NODES = []
NETBOTZ_CREDENTIALS = None

# setup a thread locking mechanism to avoid the creation of multiple threads
global thread_running
thread_running = False

def show_menu():
    print("\n")
    print("+-----------------------+------------------------+")
    print("| == NetBotz Monitoring Client v0.1.0-beta.2 === |")
    print("+-----------------------+------------------------+")
    print("|           Authored by Fokos Nikolaos           |")
    print("+-----------------------+------------------------+")
    print("| 1. Start              | Starts the daemon      |")
    print("+-----------------------+------------------------+")
    print("| 2. Stop               | Stops the daemon       |")
    print("+-----------------------+------------------------+")
    print("| 3. Setup              | NetBotz Setup          |")
    print("+-----------------------+------------------------+") 
    print("| 0. Exit               |            -           |")
    print("+-----------------------+------------------------+")

def show_setup():
    print("\n")
    print("+-----------------------+------------------------+")
    print("| =============== NetBotz Setup ================ |")
    print("+-----------------------+------------------------+")
    print("| 1. Nodes              | Add nodes              |")
    print("+-----------------------+------------------------+")
    print("| 2. Credentials        | Set login credentials  |")
    print("+-------------------------------------------------")
    print("| 3. Overview           | View the configuration |")
    print("+-----------------------+------------------------+")
    print("| 0. Previous           |            -           |")
    print("+-----------------------+------------------------+")

def setup_node(label, ip):
    node = label, ip
    NETBOTZ_NODES.append(node)
    print(f"Added Node: {label}@{ip}")

def setup_credentials(username, password):
    global NETBOTZ_CREDENTIALS
    NETBOTZ_CREDENTIALS = (username, password)
    print(f"Credentials set: {username}:{password}")

def main():
    menu_choice = None 
    setup_choice = None 
    thread = None
    global thread_running

    while (menu_choice != 0):
        show_menu()
        # checks for valid input
        try:  
            menu_choice = int(input("> "))
        except ValueError:
            print("Invalid Value.")
 
        if (menu_choice == 1):
            if (thread_running == False):
                thread = threading.Thread(target=daemon.start, args=(NETBOTZ_NODES, NETBOTZ_CREDENTIALS), daemon=True)
                print(f"Thread created: {thread.name}")
                thread.start()
                thread_running = True
                print(f"Thread: {thread.name} started.")
            else: 
                print("A daemon is already running...")
        elif (menu_choice == 2):
            daemon.stop()
            thread_running = False
            
        elif (menu_choice == 3):
            show_setup()
            while (setup_choice != 0):
                # checks for valid input
                try:
                    setup_choice = int(input("> "))
                except ValueError:
                    print("Invalid Value.")

                if (setup_choice == 1):
                    label = str(input("Label: "))
                    ip = str(input("IP: "))
                    setup_node(label, ip)
                elif (setup_choice == 2):
                    username = str(input("Username: "))
                    password = str(input("Password: "))
                    setup_credentials(username, password)
                elif (setup_choice == 3):
                    print("Nodes: ", NETBOTZ_NODES)
                    print("Credentials: ", NETBOTZ_CREDENTIALS)
            
            menu_choice = None
            setup_choice = None
        
    print("Exiting...")
    return 0

# main execution
if __name__ == "__main__":
    # upon termination shows proper exit code
    try:
        status = main()
    except KeyboardInterrupt:
        status = -1

    print("Exit Code: ", status)
    