from websockets.sync.client import connect

def request():
    with connect("ws://localhost:8283?username=Abiel") as websocket:
        _input= input("Enter Prompt: ")
        websocket.send(_input)
        #websocket.send('List their names')
        response=''
        while True:
            received = websocket.recv()
            if received == "<<Response Finished>>":
                break
            response+= received
            print(received, end="", flush=True)
        print("\n")
        return response

if __name__ =='__main__':
    request()