import tkinter
import sender
import listener


def gui_sender():
    global my_msg
    global msg_list
    global top

    top = tkinter.Tk()
    top.title("Incogn1to")
    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  # For the messages to be sent.
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=25, width=150, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.configure(background='#000d1a')
    msg_list.configure(foreground='white')
    top.configure(background='#00264d')
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", sender.send_mess)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=sender.send_mess)
    send_button.configure(foreground='white')
    send_button.configure(background='#000d1a')
    send_button.pack()

    top.protocol("WM_DELETE_WINDOW", on_closing_sender)
    tkinter.mainloop()


def gui_listener():
    global my_msg
    global msg_list
    global top

    top = tkinter.Tk()
    top.title("Incogn1to")

    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  # For the messages to be sent.
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=25, width=150, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.configure(background='#000d1a')
    msg_list.configure(foreground='white')
    top.configure(background='#00264d')
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", listener.send_mess)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=listener.send_mess)
    send_button.configure(foreground='white')
    send_button.configure(background='#000d1a')
    send_button.pack()

    top.protocol("WM_DELETE_WINDOW", on_closing_listener)
    tkinter.mainloop()


def get_my_msg():
    return my_msg


def get_msg_list():
    return msg_list


def on_closing_sender(event=None):
    sender.get_socket().close()
    top.quit()


def on_closing_listener(event=None):
    listener.get_socket().close()
    top.quit()
