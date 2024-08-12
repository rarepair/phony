#!/usr/bin/env python
import logging, util, os, re, signal, code
from argparse import ArgumentParser, RawTextHelpFormatter
from time import sleep
from pathlib import Path
from datetime import datetime
from phone import Phone
from gpiozero import Button

this_script_path     = Path(__file__).resolve()
this_script_dir      = this_script_path.parent.resolve()
this_script_filename = this_script_path.name
output_path_root     = Path(this_script_dir,'out').resolve()

def sigint_handler(signum, frame):
    logger = logging.getLogger(name=this_script_filename)
    logger.critical("Received SIGINT. Exiting")
    exit()
signal.signal(signal.SIGINT, sigint_handler)

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

def handset_up(button, phone_manager, logger, out_dir):
    new_file_name = get_new_filename(logger=logger, out_dir=out_dir)
    phone_manager.play(audio_file="/home/wtk/Desktop/test.wav")
    phone_manager.record(audio_file=new_file_name)

def handset_down(button, phone_manager):
    phone_manager.stop()

if (__name__ == "__main__"):
    args = parse_args()
    util.init_logging(console_level=(logging.DEBUG if args.debug else logging.INFO))
    logger = logging.getLogger(name=this_script_filename)

    start_time = datetime.now()
    logger.info("Program started at %s" % (start_time.now().strftime("%H:%M:%S on %d %B %Y")))

    phone_manager = Phone()
    handset_button = Button(pin=14, pull_up=True, bounce_time=0.5)
    handset_button.when_activated = lambda: handset_up(button=handset_button, phone_manager=phone_manager, logger=logger, out_dir=args.output)
    handset_button.when_deactivated = lambda: handset_down(button=handset_button, phone_manager=phone_manager)

    # Main thread loop. Nothing to do except wait for a the OS to eventually kill us
    while True:
        sleep(10)

    if args.debug:
        code.interact(banner="\n", local=locals()) # Enter interactive Python interpreter
