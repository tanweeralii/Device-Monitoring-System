#!/usr/bin/python3

import subprocess
import websocket
import time
try:
    import thread
except ImportError:
    import _thread as thread


def run_command(command_to_run):
    try:
        command_list = command_to_run.split(" ")
        res = subprocess.run(
            command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ws.send(res.stdout.decode()+res.stderr.decode()+"+browser")
    except:
        ws.send("Got Error. Retry+browser")


def on_message(ws, message):
    '''
        This method is invoked when ever the client
        receives any message from server
    '''
    x = format(message).split("+", 1)
    print(x[1])
    if x[1] == 'linux':
        run_command(format(x[0]))


def on_error(ws, error):
    '''
        This method is invoked when there is an error in connectivity
    '''
    print("received error as {}".format(error))


def on_close(ws):
    '''
        This method is invoked when the connection between the 
        client and server is closed
    '''
    print("Connection closed")


def on_open(ws):
    '''
        This method is invoked as soon as the connection between 
                client and server is opened and only for the first time
    '''
    print("Connected")

    def run(*args):
        while True:
            time.sleep(20)
            ws.send("Hello")
        time.sleep(20)
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    while True:
        try:
            ws = websocket.WebSocketApp("wss://",
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
            ws.on_open = on_open
            ws.run_forever()
        except:
            print("Cannot Connect")
