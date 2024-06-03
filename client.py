import socket
import sys
from os import path as os_path, listdir as os_listdir, makedirs as os_makedirs
import getopt
import shutil
from time import sleep, time


def send_string(sock, string):
    sock.sendall(string.encode() + b'\n')


def send_int(sock, integer):
    sock.sendall(str(integer).encode() + b'\n')


def create_backup_file(src_dir, _fn, backup_dir):
    path = os_path.join(src_dir, _fn)
    try:
        shutil.move(path, backup_dir)
    except shutil.Error:
        print("File exists and it will not be overridden...")
        bk_fn, ext = _fn.split(".")
        epoch = str(int(time()))
        bk_fn = "_".join([bk_fn, epoch])
        bk_fn = ".".join([bk_fn, ext])
        print("New backup file:", bk_fn)
        backup_dir = os_path.join(backup_dir, bk_fn)
        create_backup_file(src_dir, _fn, backup_dir)


def send_files(sock, src_dir, backup_dir):
    send_string(sock, src_dir)
    files = os_listdir(src_dir)
    n_files = len(files)
    send_int(sock, n_files)

    for _file in files:
        fpath = os_path.join(src_dir, _file)
        fsize = os_path.getsize(fpath)
        send_string(sock, _file)
        send_int(sock, fsize)
        with open(fpath, 'rb') as f:
            sock.sendall(f.read())


def transmit_files(host, port, src_dir, backup_dir, task_period):
    print(f'Task repeated every {task_period} minutes...')
    current_task_mins = 1
    while True:
        current_task_mins -= 1
        if current_task_mins == 0:
            print('\nStarting new socket instance...')
            sock = socket.socket()
            print('Connecting socket...')
            sock.connect((host, port))
            print(f'Sending files from folder: {src_dir}')
            send_files(sock, src_dir, backup_dir)
            sock.close()
            print(f'Moving files to backup folder...')
            os_makedirs(backup_dir, exist_ok=True)
            for _fn in os_listdir(src_dir):
                create_backup_file(src_dir, _fn, backup_dir)
            current_task_mins = task_period
        print(f"The next call will be made in {current_task_mins} minutes...")
        sleep(60)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "t:hi:p:s:b:", ["taskperiod", "help", "host=", "port=", "source=", "backup="])
    except getopt.GetoptError:
        print('Invalid option. Usage: client.py -t <taskperiod> -i <host> -p <port> -s <source> -b <backup>')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-t", "--taskperiod"):
            task_period = int(arg)
        elif opt in ("-i", "--host"):
            host = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-s", "--source"):
            src_dir = arg
        elif opt in ("-b", "--backup"):
            backup_dir = arg

    transmit_files(host, port, src_dir, backup_dir, task_period)


if __name__ == '__main__':
    main(sys.argv[1:])
