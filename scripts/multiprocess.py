from argparse import ArgumentParser
from multiprocessing import cpu_count, Pool
from datetime import datetime
from json import dumps, load
from glob import glob
from os import path

from logger import Logger

# define directories
root_dir = path.dirname(path.dirname(__file__))
files_dir = path.join(root_dir, "files")
source_dir = path.join(files_dir, "source")
target_dir = path.join(files_dir, "target")

# instantiate logger
log = Logger.get()


def worker(file):
    start_time = datetime.now()

    # open file
    with open(file, "r") as fhi:
        # load data to dictionary
        data = load(fhi)

        # add new items to dictionary
        data["System"] = "OldSystem"
        data["Currency"] = "USD"

    # write dictionary to new file
    filename = path.basename(file)
    new_file = path.join(target_dir, filename)
    with open(new_file, "w") as fho:
        fho.write(dumps(data, indent=4))

    run_time = datetime.min + (datetime.now() - start_time)
    log.info("completed {} in {}".format(filename, run_time.strftime("%H:%M:%S")))


def process(**kwargs):
    start_time = datetime.now()
    
    workers = kwargs.get("workers")
    
    log.info("start (workers={})".format(workers))

    # get files to process
    files = glob(path.join(source_dir, "*.json"))

    # sequential process
    # for file in files:
    #     worker(file)

    # multi process
    with Pool(processes=workers) as pool:
        result = pool.map_async(worker, files)
        result.wait()
    
    run_time = datetime.min + (datetime.now() - start_time)
    log.info("complete (run time: {})".format(run_time.strftime('%H:%M:%S')))


if __name__ == '__main__':
    # define script arguments..
    parser = ArgumentParser(description="multi processing script")
    parser.add_argument("-w", dest="workers", type=int, required=False, help="Workers.", default=int(cpu_count()/2))
    parser.add_argument("--debug", action="store_true", help="debug")
    
    # parse script arguments
    args = parser.parse_args()
    
    process(**vars(args))
