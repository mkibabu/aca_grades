import logging
import math
import pathlib
from typing import List

import pandas

import config

FILES = []
GRADES = {}
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
            class_name = file.name[:file.name.index(".csv")]
            logger.info("Processing data for class %s", class_name)
            try:
                df = pandas.read_csv(
                    file,
                    converters={"Grade": lambda g: int(float(g))},
                    names=['student', 'grade'],
                    header=0
                    )
                excluded_students, mean_grade = calculate_average(df)
                this_class = {
                    mean_grade: [class_name, len(df), len(df) - len(excluded_students), excluded_students]
                }
                GRADES.update(this_class)
            except Exception:
                logger.exception("Error reading input file %s", file.name)


def calculate_average(df: pandas.DataFrame) -> (List[str], int):
    """
    Calculate the average grade from a dataframe of grades, excluding grades
    less than 1.

    params:
    df (pandas.DataFrame): A dataframe of grades, with each row representing a
        student name and grade.

    returns:
    List[str]: List of students excluded from the average grade calculation.
    int: the average grade from this dataframe of grades.
    """
    # Get the list of students that we'll exclude
    zero_grades = df[df['grade'] == 0]
    excluded = zero_grades['student'].to_list()

    # Calculate average grade using non-zero-grade students
    non_zero_df = df[df['grade'] > 0]
    avg_grade = round(non_zero_df['grade'].mean(), 2)

    return excluded, avg_grade


if __name__ == "__main__":
    populate_input_files_list()
    read_all_files()
    print(GRADES)
