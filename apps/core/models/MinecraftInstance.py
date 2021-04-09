import io
import os
import sys
from shutil import rmtree
from socket import AF_UNIX, SOCK_DGRAM, socket
from subprocess import PIPE, Popen, TimeoutExpired
from threading import Thread
from time import sleep

import mcdwld
from core.network import get_first_open_port
from django.conf import settings

SOCKFILE_NAME = 'application.socket'


class MinecraftInstance(Thread):
    """
    A class that allow to handle minecraft server instances.

    Three states are availables :

    * stopped
    * starting
    * running

    When running, object can be use to send command to the instance.
    """

    TIMEOUT_STOP = 30
    DEFAULT_PORT = 25565

    def __init__(self, id: int, version: str):
        """
        Instanciate the server.

        If it is the first execution, the program create :

        * execution directory
        * eula.txt and accept it
        """
        Thread.__init__(self)
        self.setName('Server#%d' % id)

        self.id = id
        self.running = False
        self.processus = None
        self.port = None

        self.executable = mcdwld.get_server_file(
            directory=settings.MINECRAFT_DOWNLOAD_ROOT,
            version=version,
        )
        self.directory = settings.MINECRAFT_DATA_ROOT % self.id
        self.eula_file = os.path.join(self.directory, 'eula.txt')
        self.properties_file = os.path.join(
            self.directory, 'server.properties')

        self.sockfile = os.path.join(self.directory, SOCKFILE_NAME)
        self.socket = socket(AF_UNIX, SOCK_DGRAM)
        self.socket.setblocking(False)

    def run(self):
        """Execute the Minecraft server."""
        if not os.path.exists(self.executable):
            raise FileNotFoundError(
                'Server executable not found (%s)' % self.executable)
        if os.path.isfile(self.directory):
            raise FileExistsError('Directory is a file (%s)' % self.directory)
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        if os.path.exists(self.sockfile):
            os.remove(self.sockfile)

        with open(self.eula_file, 'wt+') as eula:
            eula.write('eula=true')

        self.socket.bind(self.sockfile)
        self.port = get_first_open_port(self.DEFAULT_PORT)

        arguments = [
            'java',
            '-server',
            '-Xms%s' % settings.MINECRAFT_MCMINMEM,
            '-Xmx%s' % settings.MINECRAFT_MCMAXMEM,
            # Tuning garbage collector
            '-XX:+UseG1GC',
            # '-XX:+CMSClassUnloadingEnabled',
            '-XX:ParallelGCThreads=2',
            # '-XX:MinHeapFreeRatio=5',
            # '-XX:MaxHeapFreeRatio=',
            # Launch jar file
            '-jar',
            self.executable,
            # '--port %d' % self.port,
            '--nogui',  # desactive server gui
        ]
        self.processus = Popen(
            args=arguments,
            cwd=self.directory,
            universal_newlines=True,
            stdin=PIPE,
            stdout=PIPE
        )

        self.running = True
        while self.processus.poll() is None and self.running:
            sleep(0.1)
            try:
                data = self.socket.recv(2048)
            except IOError:
                data = None
            if data:
                message = data.decode('utf-8')
                msg_type, msg_data = message.split(':')
                if msg_type == 'action' and msg_data == 'close':
                    self.stop()
                    self.processus.wait()
                    return
                elif msg_type == 'command':
                    self.exec_command(msg_data)
        self.stop()

    def exec_command(self, command: str):
        """Give a command to the server."""
        if not command.endswith('\n'):
            command += '\n'
        if self.processus is not None:
            try:
                self.processus.stdin.write(command)
                self.processus.stdin.flush()
            except IOError:
                pass

    def stop(self, force=False):
        """
        Stop the Minecraft server.
        Wait the server stop.
        """
        if not self.running:
            return

        self.running = False
        self.socket.close()
        os.remove(self.sockfile)
        if force:
            try:
                self.processus.communicate(
                    input='stop\n',
                    timeout=self.TIMEOUT_STOP
                )
            except TimeoutExpired:
                self.processus.kill()
        else:
            self.exec_command('save-all')
            self.exec_command('stop')
            self.processus.wait()

    def delete_data(self):
        """Delete all data about this minecraft server instance."""
        self.stop()
        rmtree(self.directory)
