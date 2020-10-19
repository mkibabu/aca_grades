import logging
import math
import pathlib

import pandas

import config
from grade_calculator import calculate_average


FILES = []
logger = logging.getLogger("get_files")


def populate_input_files_list():
    """
    Populate the list of files to read from. This assumes that the files
    are in the directory defined by the INPUT_DIR config value.
    """

    input_dir = pathlib.Path(config.INPUT_DIR)
    logger.info("Reading inut files from location %s", input_dir.resolve())
    for item in input_dir.iterdir():
        if item.is_file():
            FILES.append(item.resolve())

    logger.info("Found %s files in input location %s", len(FILES), input_dir.resolve())


def read_all_files():
    # Since we have to keep track of individual class values, fileinput doesn't
    # work out very well here. Loop over the filenames instead.
    for file in FILES:
        with open(file, 'r') as grades:
            logger.info("Processing data for class %s", file.name[:file.name.index(".csv")])
            try:
                df = pandas.read_csv(file, index_col="Student Name", converters={"Grade": lambda g: int(float(g))})
                calculate_average(df)
            except Exception:
                logger.exception("Error reading input file %s", file.name)


if __name__ == "__main__":
    populate_input_files_list()
    read_all_files()
