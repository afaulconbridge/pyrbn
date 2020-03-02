# to profile:
# python -m cProfile -o perf.prof perf.py
# snakeviz perf.prof
# Then view :8080/snakeviz/perf.prof

# run once to generate data
# run again to analyze data

import argparse
import collections
import csv
import gc
import logging
import logging.config
import random
import sys
import time

# this is an extra dependency
import pandas as pd
from pyrbn import RBNBasic, RBNFast, RBNNumpy


def main():
    # measure performance of implementation
    fieldnames = ("cls", "n", "k", "i", "j", "steptime")
    timings = None

    # see if we can read data
    try:
        with open("perf.csv", "r") as csvfile:
            reader = csv.reader(csvfile)
            timings = pd.DataFrame.from_records(reader, columns=next(reader))
            print(timings.describe())

            # make sure things are the right type
            timings["n"] = timings["n"].astype("int64")
            timings["k"] = timings["k"].astype("int64")
            timings["i"] = timings["i"].astype("int64")
            timings["j"] = timings["j"].astype("int64")
            timings["steptime"] = timings["steptime"].astype("float64")
            # now that we have the data, analyze it
            print(timings.groupby(["cls", "n"]).mean()["steptime"])

    except FileNotFoundError:
        # no data, generate it
        writer = csv.writer(sys.stdout)
        writer.writerow(fieldnames)
        Timing = collections.namedtuple("Timing", fieldnames)
        timings = []
        clzzes = [RBNNumpy, RBNFast, RBNBasic]
        ns = (10, 100, 1000)
        ks = (2, 5)
        for clzz in clzzes:
            for n in ns:
                for k in ks:
                    for i in range(25):
                        for j in range(1):
                            # setup
                            rng = random.Random(i)
                            rbn = clzz.from_random(rng)
                            state = rbn.states

                            # prepare for timing
                            gc.disable()
                            starttime = time.time()
                            # timing
                            for l in range(10000):
                                state = rbn.next_state(state)
                            # cleanup after timing
                            endtime = time.time()
                            gc.enable()
                            gc.collect()

                            # store time result
                            interval = endtime - starttime
                            timing = Timing(clzz.__name__, n, k, i, j, interval)
                            timings.append(timing)
                            writer.writerow(timing)

        with open("perf.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fieldnames)
            writer.writerows(timings)


def main_setup():
    parser = argparse.ArgumentParser("pyrbnachem")
    parser.add_argument(
        "--log-config", type=str, default=None, help="log configuration file"
    )
    parser.add_argument(
        "--log-critical", action="store_const", const=logging.CRITICAL, dest="log_level"
    )
    parser.add_argument(
        "--log-error", action="store_const", const=logging.ERROR, dest="log_level"
    )
    parser.add_argument(
        "--log-warning", action="store_const", const=logging.WARNING, dest="log_level"
    )
    parser.add_argument(
        "--log-info",
        action="store_const",
        const=logging.INFO,
        dest="log_level",
        default=logging.INFO,
    )
    parser.add_argument(
        "--log-debug", action="store_const", const=logging.DEBUG, dest="log_level"
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)
    if args.log_config:
        logging.config.fileConfig(args.log_config)

    logger = logging.getLogger("pyrbnachem")

    if args.log_config:
        logger.debug("loaded log config from {}".format(args.log_config))

    main()


if __name__ == "__main__":
    main_setup()
