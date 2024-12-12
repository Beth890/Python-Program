import datetime #Option 1 (show date/time)
import socket #Option 2/5 (IP addresses/socket connections)
from netmiko import ConnectHandler #Option 3/4(remote devices) 
import os #Option 5 (current working directory)


#Option 1, show local date and time
def show_local_datetime():
    print ("Local date and time is", datetime.datetime.now())

#Option 2, show local IP address
def show_local_ip():
    #Use socket to initially get host name and then the IP address
    print ("Local IP Address is", socket.gethostbyname(socket.gethostname()))

#Option 3, Show remote home directory
def show_remote_home_directory(ip, username, password):
    #remote home directory information
    device = {
        "device_type": "linux",
        "ip": "*****",#Input relevant remote device information
        "port": "*****",
        "username": "*****",
        "password":"******",
        "secret":"*****", #enable password (Privileged EXEC mode)
    }
    
    #enable connection to remote device
    ConnectHandler(**device).enable()

    try:
        #Establish SSH connection to remote device (make sure device is on) and input command 'dir' to show directory
        with ConnectHandler(**device) as ssh_conn:
            result = ssh_conn.send_command("dir")
            #Print results of using 'dir' command
            print("Remote Home Directory Listing include \n", result)

    #Exemption handling, using variable 'e' to give addition details of error to user
    except Exception as e:
        print(f"Error connecting to remote server: {e}")

#Option 4, Backup remote file
def backup_remote_file(ip, username, password):
    #Allow user to input path of file they wish to backup and use as remote_path variable
    remote_path= input("Enter the full path of the file on the remote computer: ")

    device = {
        "device_type": "linux",
        "ip": "*****", #Input relevant remote device information
        "port":"*****",
        "username": "******",
        "password": "******",
        "secret":"*******", #enable password (Privileged EXEC mode)
    }
#enable connection to remote device
    ConnectHandler(**device).enable()
    
    #print directory of remote device
    result = ConnectHandler(**device).send_command("dir")
    print("\n Remote Home Directory Listing include \n", result)

    try:
        with ConnectHandler(**device) as ssh_conn:
#Use connectHandler and command cp to copy required file
            result = ssh_conn.send_command(f"cp {remote_path} {remote_path}.old")
#Print successful and use exemption handling for errors
            print("\n Backup completed successfully." , result)
    except Exception as e:
        print(f"Error backing up remote file: {e}")
#print directory again to show copied file
    result = ConnectHandler(**device).send_command("dir")
    print("\n Remote Home Directory Listing include \n", result)

#Option 5, Save web page
def save_web_page():
# Ask for user input of url and name for saved file
    url = input("Enter the full URL of the web page: ")
    file_name = input("What do you want to name the saved file? ")

    try:
        # Resolve the domain name to an IP address to try avoid errors
        ip_address = socket.gethostbyname(url)

        # Create a socket and connect to the server using the resolved IP address
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip_address, 80))  # Connect to the server using IP address and port 80
        
            # Construct the HTTP GET request to fetch the page
            request = f"GET / HTTP/1.1\r\nHost: {url}\r\nConnection: close\r\n\r\n"
            s.send(request.encode())  # Send the HTTP GET request
        
            # Open the file for writing once, before the loop
            with open(file_name, "w") as file:
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
                
                    file.write(data.decode())#Write the HTML to file   
            

    except socket.gaierror:
        # Handle errors related to invalid URL
        print("Error: The URL could not be resolved. Please check the URL and try again.")

    except socket.error as e:
        # Handle socket-related errors
        print(f"Socket error: {e}")

    except FileExistsError:
        # Handle errors if file already exists
        print(f"Error: The path '{file_name}' is invalid or the file cannot be created.")

    except Exception as e:
        # To cover other errors
        print(f"An unexpected error occurred: {e}")

    else:
        # If the file is successfully saved, print confirmation
        print(f"\nWeb page saved successfully to {file_name}.\n Preview some contents below. \n")
        readfile = open(file_name)
        content = readfile.readlines()
        print(content[25:35])

    finally:
        # Finally, to show if file was or wasn't saved
            current_directory = os.getcwd()
            files_and_directories = os.listdir(current_directory)
            print("\nSee file saved/not saved in current directory:\n", files_and_directories, "\n")

    


#variables for remote server
remote_ip = "remote_server_ip"
remote_username = "remote_username"
remote_password = "remote_password"
    
#Print menu to show options
while True:
    print("\nMenu:")
    print("1 - Show date and time (local computer)")
    print("2 - Show IP address (local computer)")
    print("3 - Show Remote home directory listing")
    print("4 - Backup remote file")
    print("5 - Save web page")
    print("Q - Quit")

    choice = input("Enter your choice: ").upper() #using upper to change q to Q if user uses lowercase so it still runs
        
#Set actions for chosen choice and break if invaild choice chosen to keep programme running
    if choice == "1":
        show_local_datetime()
    elif choice == "2":
        show_local_ip()
    elif choice == "3":
        show_remote_home_directory(remote_ip, remote_username, remote_password)
    elif choice == "4":
        backup_remote_file(remote_ip, remote_username, remote_password)
    elif choice == "5":
        save_web_page()
    elif choice == "Q":
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
    




    
    
   

        
        
        





