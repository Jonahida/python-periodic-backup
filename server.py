import socket
import sys
from getopt import getopt
from os import path as os_path
import shutil


def receive_files(host, port, target_dir, n_clients):
    print('\nStarting socket instance...')
    s = socket.socket()
    print('Bind...')
    s.bind((host, port))
    print('Listen...')
    s.listen(n_clients)

    while True:
        client, address = s.accept()
        print(f'{address} connected')

        # client socket and makefile wrapper will be closed when with exits.
        with client, client.makefile('rb') as clientfile:
            while True:
                folder = clientfile.readline()
                if not folder:
                    # When client closes connection folder == b''
                    break
                folder = folder.strip().decode()
                no_files = int(clientfile.readline())
                print(f'Receiving folder: {folder} ({no_files} files)')

                for i in range(no_files):
                    filename = clientfile.readline().strip().decode()
                    filesize = int(clientfile.readline())
                    data = clientfile.read(filesize)
                    print(f'Receiving file: {filename} ({filesize} bytes)')
                    with open(os_path.join(target_dir, filename), 'wb') as f:
                        f.write(data)


def main(argv):
    try:
        opts, args = getopt(argv, "hi:p:t:c:", ["help", "host=", "port=", "target=", "clients="])
    except getopt.GetoptError:
        print('Invalid option. Usage: server.py -i <host> -p <port> -t <target> -c <clients>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--host"):
            host = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-t", "--target"):
            target_dir = arg
        elif opt in ("-c", "--clients"):
            n_clients = int(arg)

    receive_files(host, port, target_dir, n_clients)


if __name__ == '__main__':
    main(sys.argv[1:])
