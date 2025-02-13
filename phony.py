#!/usr/bin/python
import logging, util, os, re, signal, code
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep
from pathlib import Path
from datetime import datetime
from phone import Phone
from gpiozero import Button

# Script constants
this_script_path          = Path(__file__).resolve()
this_script_dir           = this_script_path.parent.resolve()
this_script_filename      = this_script_path.name
output_path_root          = Path(this_script_dir, 'out').resolve()
greeting_msg_path         = Path(this_script_dir, 'greeting.wav').resolve()
handset_button_pin        = 14
handset_button_debounce_s = 0.2
secret_button_pin         = 12
secret_button_debounce_s  = 1

# Handle SIGINT signals (ex: user presses CTRL + C) to exit gracefully.
def sigint_handler(signum, frame):
    logger = logging.getLogger(name=this_script_filename)
    logger.critical("Received SIGINT. Exiting")
    logger.info("Program ended at %s" % (start_time.now().strftime("%H:%M:%S on %d %B %Y")))
    exit()
signal.signal(signal.SIGINT, sigint_handler)

# Parse script input arguments.
def parse_args():
    desc_str = ("Implements a telephone message recorder\n\n")
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter, description=desc_str)
    parser.add_argument("-o", "--output", type=str, default=output_path_root, help="The directory to output recorded audio files and the log (default=%(default)s)")
    parser.add_argument("--debug", action="store_true", help="If specified, log messages at DEBUG level and higher will be printed to the console")
    return parser.parse_args()

# Look through output_path_root to determine the number the last recording started with and generate a new filename
def get_new_filename(logger, out_dir):
    logger.debug("Determining next recording filename")
    try:
        outdir_contents = os.listdir(path=out_dir)
    except Exception as err:
        logger.error("A %s exception was raised while trying to list the contents of directory %s" % (type(err).__name__, outdir_contents))
        raise

    # Iterate through the list of outdir_contents to find the highest numbered directory
    last_dir_num = 0
    for obj in outdir_contents:
        matched = re.match(pattern="^([0-9]+)_", string=obj)

        # matched[1] corresponds to the first capture group
        if matched is not None and matched[1] is not None and int(matched[1]) > last_dir_num:
            last_dir_num = int(matched[1])

    new_file_name = "%d_Recording_%s.wav" % (last_dir_num + 1, datetime.now().strftime("%d%b%y-%H%M%S"))
    logger.debug("Last recording number was %d. Using new filename %s" % (last_dir_num, new_file_name))
    return str(Path(out_dir, new_file_name).resolve())

# This function gets called by the gpiozero library when the handset is lifted off the receiver. It simultaneously initiates playback
# of the greeting message from the handset speaker and starts recording from the handset microphone.
def handset_up(button, phone_manager, logger, out_dir):
    new_file_name = get_new_filename(logger=logger, out_dir=out_dir)
    phone_manager.play(audio_file=greeting_msg_path)
    phone_manager.record(audio_file=new_file_name)

# This function is called by the gpiozero library when the handset is placed down onto the receiver. It halts any ongoing playback and
# recording threads.
def handset_down(button, phone_manager):
    phone_manager.stop()

# This function is called by the gpiozero library when the special key chord combination is pressed on the phone receiver. It stops any
# ongoing threads and then initiates playback of the second-last recording (since the first-last will be the one that was just terminated).
def play_last_recording(button, phone_manager):
    phone_manager.stop()
    second_last_recording = phone_manager.getSecondLastRecording()
    phone_manager.play(audio_file=second_last_recording)

# Main program loop. It parses input arguments, initiates the logger, and registers callback functions in the gpiozero library to be called
# upon button activations.
if (__name__ == "__main__"):
    args = parse_args()
    util.init_logging(console_level=(logging.DEBUG if args.debug else logging.INFO), logfile=True, logfile_dir=output_path_root)
    logger = logging.getLogger(name=this_script_filename)

    start_time = datetime.now()
    logger.info("Program started at %s" % (start_time.now().strftime("%H:%M:%S on %d %B %Y")))

    phone_manager = Phone()
    handset_button = Button(pin=handset_button_pin, pull_up=True, bounce_time=handset_button_debounce_s)
    handset_button.when_activated = lambda: handset_up(button=handset_button, phone_manager=phone_manager, logger=logger, out_dir=args.output)
    handset_button.when_deactivated = lambda: handset_down(button=handset_button, phone_manager=phone_manager)
    secret_button = Button(pin=secret_button_pin, pull_up=True, bounce_time=secret_button_debounce_s)
    secret_button.when_activated = lambda: play_last_recording(button=secret_button, phone_manager=phone_manager)

    if args.debug:
        code.interact(banner="\n", local=locals()) # Enter interactive Python interpreter

    # Main thread loop. Nothing to do except wait for a the OS to eventually kill us
    while True:
        sleep(10)
