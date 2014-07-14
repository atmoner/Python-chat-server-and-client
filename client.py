# telnet program example
# https://pypi.python.org/pypi/simple-crypt
import socket, select, string, sys
from simplecrypt import encrypt, decrypt

def prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()
 
#main function
if __name__ == "__main__":
     
    if(len(sys.argv) < 4) :
        print 'Usage : python telnet.py hostname port debug(true,false)'
        sys.exit()
     
    host = sys.argv[1]
    port = int(sys.argv[2])
    debug = sys.argv[3]
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    print 'Connected to remote host. Start sending messages ' + debug
    prompt()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    if(debug == 'true') :
                        plaintext = data
                    else :
                        plaintext = decrypt('password', data)

                    sys.stdout.write(plaintext)
                    prompt()
             
            #user entered a message
            else :
                msg = sys.stdin.readline()
                ciphertext = encrypt('password', msg)
                s.send(msg)
                prompt()
                
