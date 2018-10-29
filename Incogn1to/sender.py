import socket
import time
import blinder_send
import threading
import interface


def sel_username():
        global username, host, port
        username = input("Choose your username for this chat > ")
        while len(username) > 20:
            print("Username should contains max 20 character!")
            username = input("Choose your username for this chat > ")
        host = input("Insert the IP of your friend: ")
        port = int(input("Insert the port number: "))


def connect_to():

    try:
        global s, username_recv

        s = socket.socket()
        s.connect((host, port))
        s.send(str.encode(username))
        username_recv = str(s.recv(1024), 'utf-8')
        print("[*] Connected with", username_recv)
        public_key_list = s.recv(4096)
        enc_key = blinder_send.rsa_encryption(public_key_list)
        s.send(enc_key)
        # Starting thread for receive message
        t_recv = threading.Thread(target=receive)
        t_recv.start()

    except ConnectionRefusedError:
            print("[*] Your friend is offline...retrying")
            time.sleep(10)
            connect_to()

    except (ConnectionResetError, ConnectionAbortedError):
            print("\n[*] Closing Incogn1to")
            time.sleep(1)
            s.close()
            interface.on_closing_sender()
    except (socket.gaierror, OverflowError):
            print('[*] Bad IP or PORT')
            sel_username()


def send_mess(event=None):

        try:
            send_message = interface.get_my_msg().get()
            interface.get_my_msg().set('')
            if len(send_message) > 0:
                base64text = blinder_send.aes_encryption_sender(send_message)
                s.send(base64text)
                interface.get_msg_list().insert('end', 'You: ' + send_message[:160])
                interface.get_msg_list().yview('end')
                if len(send_message) > 160:
                    interface.get_msg_list().insert('end', send_message[160:320])
                    interface.get_msg_list().yview('end')
        except ConnectionAbortedError:
            print("[*] Connection Aborted Error!")
            print("[*] Closing chat ")
        except OSError:
            err_msg = '[ERROR] --> Check the terminal for more info'
            print("[*] Unable to send the message...maybe your friend has left the chat")
            interface.get_msg_list().insert('end', err_msg)
            interface.get_msg_list().yview('end')


def receive():

    try:
        while True:
                rec_mess = s.recv(4096)
                if not rec_mess:
                    err_msg = '[ERROR] --> Check the terminal for more info'
                    print("[*] Your friend has left the chat :(")
                    print("[*] Trying to reconnect...")
                    interface.get_msg_list().insert('end', err_msg)
                    interface.get_msg_list().yview('end')
                    time.sleep(5)
                    connect_to()
                dec_mess = blinder_send.decrypt_message(rec_mess)
                if dec_mess != '':
                    interface.get_msg_list().insert('end', username_recv + ': ' + dec_mess[:160])
                    interface.get_msg_list().yview('end')
                    if len(dec_mess) > 160:
                        interface.get_msg_list().insert('end', dec_mess[160:320])
                        interface.get_msg_list().yview('end')

    except ConnectionResetError:
        err_msg = '[ERROR] --> Check the terminal for more info'
        print("[*] Your friend has left the chat :(")
        print("[*] Trying to reconnect...")
        interface.get_msg_list().insert('end', err_msg)
        time.sleep(5)
        connect_to()

    except ConnectionAbortedError:
        print("\n[*] Closing Incogn1to")
        time.sleep(1)
        s.close()
        interface.on_closing_sender()


def get_socket():
    return s


if __name__ == "__main__":
    print("[*] Run incogn1to.py!")
