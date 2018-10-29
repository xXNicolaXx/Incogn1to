import socket
import threading
import blinder_list
import time
import sys
import interface


def sel_username():
    global username
    global port
    username = input("Choose your username for this chat > ")
    port = int(input("Insert the port for the listener: "))
    while len(username) > 20:
        print("[*] Username should contains max 20 character!")
        username = input("Choose your username for this chat > ")


def socket_create():

    global s, conn, address, dec_key, username_recv
    try:
        s = socket.socket()
        s.bind(("0.0.0.0", port))
        s.settimeout(120)
        s.listen(1)
        print("[*] Waiting for your friend...")
        conn, address = s.accept()
        conn.send(str.encode(username))
        username_recv = str(conn.recv(1024), 'utf-8')
        print("[*] Connected with", username_recv)
        conn.send(blinder_list.get_public_key())
        aes_key = conn.recv(4096)
        dec_key = blinder_list.decrypt_aes_key(aes_key)
        # Starting thread receive message
        t_recv = threading.Thread(target=receive)
        t_recv.start()

    except socket.timeout:
        print("[*] Socket timout...")
        sys.exit()

    except OverflowError:
        print("[*] Port must be 0-65535!")
        sel_username()


def send_mess(event=None):

        try:
            send_message = interface.get_my_msg().get()
            interface.get_my_msg().set('')
            if len(send_message) > 0:
                base64text = blinder_list.aes_encryption(send_message)
                conn.send(base64text)
                interface.get_msg_list().insert('end', 'You: ' + send_message[:160])
                interface.get_msg_list().yview('end')
                if len(send_message) > 160:
                    interface.get_msg_list().insert('end', send_message[160:320])
                    interface.get_msg_list().yview('end')


        except ConnectionAbortedError:
                conn.close()
                interface.on_closing_listener()
        except BrokenPipeError:
            err_msg = '[ERROR] --> Check the terminal for more info'
            interface.get_msg_list().insert('end', err_msg)
            interface.get_msg_list().yview('end')


def receive():
    try:
        while True:
            rec_mess = conn.recv(4096)
            dec_mess = blinder_list.decrypt_message(rec_mess)
            if dec_mess != '':
                interface.get_msg_list().insert('end', username_recv + ': ' + dec_mess[:160])
                interface.get_msg_list().yview('end')
                if len(dec_mess) > 160:
                    interface.get_msg_list().insert('end', dec_mess[160:320])
                    interface.get_msg_list().yview('end')

    except ConnectionRefusedError:
            print("\n[*] Your friend is offline...")
            time.sleep(1)
            socket_create()
    except ConnectionResetError:
            print("\n[*] Your friend has left the chat :(")
            time.sleep(1)
            print("[*] Trying to reconnect...")
            time.sleep(1)
            socket_create()

    except ConnectionAbortedError:
        print("\n[*] Closing Incogn1to...")
        conn.close()
        interface.on_closing_listener()


def get_dec_aes():
    return dec_key


def get_socket():
    return conn


if __name__ == "__main__":
    print("[*] Run incogn1to.py!")

