import logging, struct, fcntl, termios, shutil, sys, pty, os, select, errno
from subprocess import Popen
from time import sleep
from select import select
from signal import SIGTERM, SIGKILL
from itertools import chain
from threading import Thread, Event, current_thread

class Phone():
    def __init__(self):
        self._logger = logging.getLogger("Phone Manager")
        self._tjoin_timeout = 5
        self._play_thread = None
        self._rcrd_thread = None
        self._play_cmd_pfx = "aplay --device=plughw:1,0 "
        self._rcrd_cmd_pfx = "arecord --device=plughw:1,0 --format=S24_LE --rate=48000 "
        self._stop = Event()

    # Do some magic fnctl stuff to set the virtual terminal window size of a PTY in order to match the current terminal size.
    def _set_pty_terminal_size(self, fd):
        columns, rows = shutil.get_terminal_size(fallback=(80, 24))
        size = struct.pack("HHHH", rows, columns, 0, 0)
        fcntl.ioctl(fd, termios.TIOCSWINSZ, size)

    def _cmd_runner(self, cmd, stop):
        thread_name = current_thread().name
        logger = logging.getLogger(thread_name)
        logger.debug("%s thread started" % thread_name)

        try:
            # Open PTYs (pseudoterminals) to use for the stdout and stderr streams. This is required because some executables will detect if they
            # are not connected to terminals and will enable block buffering of the streams, which may not get flushed regularly with the net effect
            # being that Python won't get the stdout/stderr messages as they are produced. The nanocom/nanokdp tools are good examples of this. Using
            # a PTY fools the child program into thinking its being run in a terminal. We set the PTY terminal window size to match the current one
            # trigger is being run from.
            masters, slaves = zip(pty.openpty(), pty.openpty())
            for fd in chain(masters, slaves): self._set_pty_terminal_size(fd)

            # Start the child process, using the select module to allow for non-blocking reads of the stdout and stderr streams. Note that the order
            # of messages between these streams cannot be guaranteed but in practice this doesn't seem to be an issue.
            logger.info("Spawning process using command '%s'" % (cmd))
            with Popen(args=cmd, stdin=sys.stdin, stdout=slaves[0], stderr=slaves[1], shell=True, preexec_fn=os.setsid) as proc:
                # Close the slave file descriptors here as we won't reference them past this point.
                for fd in slaves: os.close(fd)

                # Enter a select() loop to receive stdout and stderr stream data in a non-blocking manner
                readable = {
                    masters[0]: sys.stdout.buffer,
                    masters[1]: sys.stderr.buffer,
                }
                while readable:
                    if stop.isSet():
                        logger.info("Received stop event")
                        break
                    for fd in select(readable, [], [], 0)[0]:
                        try:
                            data = os.read(fd, 1024)
                        except OSError as e:
                            if (e.errno != errno.EIO): # EIO is an I/O Error
                                raise
                            del readable[fd]
                        else:
                            # If an empty bytes object is returned it means the EOF has been reached which indicates the process has terminated.
                            if not data:
                                del readable[fd]
                            else:
                                # Write the data to the corresponding sys stream so that it looks transparent to the user
                                readable[fd].write(data)
                                readable[fd].flush()

                if stop.isSet() and proc.poll() == None:
                    logger.debug("Sending SIGTERM to subprocess")
                    os.killpg(os.getpgid(proc.pid), SIGTERM)
                    sleep(0.5)
                    if proc.poll() == None:
                        logger.warning("Process is still alive after sending SIGTERM. Sending SIGKILL")
                        os.killpg(os.getpgid(proc.pid, SIGKILL))

            # If we've reached here, the child process has terminated
            for fd in masters: os.close(fd)
            ret_code = proc.returncode
            logger.info("Process finished with return code %d" % (ret_code))

        except Exception as err:
            ret_code = -2
            logger.error("A %s exception was raised while trying to execute command '%s'" % (type(err).__name__, cmd))
            logger.error("Exception: %s" % (err))

        logger.debug("%s thread finished" % thread_name)
        return ret_code

    def play(self, audio_file):
        if not self._play_thread or self._play_thread.is_alive() == False:
            cmd = self._play_cmd_pfx + str(audio_file)
            self._play_thread = Thread(target=self._cmd_runner, args=(cmd, self._stop, ), name="Player", daemon=True)
            self._play_thread.start()
        else:
            self._logger.warning("Attempted to call play() while play is in progress")

    def record(self, audio_file):
        if not self._rcrd_thread or self._rcrd_thread.is_alive() == False:
            cmd = self._rcrd_cmd_pfx + audio_file
            self._rcrd_thread = Thread(target=self._cmd_runner, args=(cmd, self._stop, ), name="Recorder", daemon=True)
            self._rcrd_thread.start()
        else:
            self._logger.warning("Attempted to call record() while recording is in progress")

    def stop(self):
        self._logger.info("Stopping play and record threads")
        self._stop.set()
        self._play_thread.join(timeout=self._tjoin_timeout)
        if self._play_thread.is_alive():
            raise Exception("Play thread didn't terminate after %ds" % self._tjoin_timeout)
        self._rcrd_thread.join(timeout=self._tjoin_timeout)
        if self._rcrd_thread.is_alive():
            raise Exception("Record thread didn't terminate after %ds" % self._tjoin_timeout)
        self._stop.clear()
