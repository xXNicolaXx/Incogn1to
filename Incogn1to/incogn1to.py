import blinder_send
import blinder_list
import sender
import listener
import interface


def start():

    print('''
ooooo                                                          .o      .             
`888'                                                        o888    .o8             
 888  ooo. .oo.    .ooooo.   .ooooo.   .oooooooo ooo. .oo.    888  .o888oo  .ooooo.  
 888  `888P"Y88b  d88' `"Y8 d88' `88b 888' `88b  `888P"Y88b   888    888   d88' `88b 
 888   888   888  888       888   888 888   888   888   888   888    888   888   888 
 888   888   888  888   .o8 888   888 `88bod8P'   888   888   888    888 . 888   888 
o888o o888o o888o `Y8bod8P' `Y8bod8P' `8oooooo.  o888o o888o o888o   "888" `Y8bod8P' 
                                      d"     YD                                      
                                      "Y88888P'            v2.0 (Made by xXNicolaXx)                         
    ''')
    print("Welcome to Incogn1to chat! Feel free to write whatever you want ;D\n")


def option():
    choice = ''
    print("\nSelect an option:")
    print("[1] Connect to your friend")
    print("[2] Waiting for your friend\n")
    while choice != '1' and choice != '2':
        choice = input("> ")
        if choice == '1':
            sender_loader()
        if choice == '2':
            list_loader()


def sender_loader():
    sender.sel_username()
    blinder_send.gen_key()
    sender.connect_to()
    interface.gui_sender()


def list_loader():

    listener.sel_username()
    print("\n[*] Generating RSA keys")
    blinder_list.rsa_key()
    listener.socket_create()
    interface.gui_listener()


if __name__ == "__main__":
    try:
        start()
        option()
    except KeyboardInterrupt:
        print("[Ctrl + C] detected! Closing Incogn1to...")
