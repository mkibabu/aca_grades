import logging
import math
import pathlib
from typing import Dict, List

import pandas

import config

FILES = []
GRADES = {}
logger = logging.getLogger("get_files")


def populate_input_files_list() -> None:
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


def read_and_process_all_files() -> None:
    # Since we have to keep track of individual class values, FileInput doesn't
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
                excluded_students, mean_grade = _calculate_average(df)
                this_class = {
                    mean_grade: [class_name, len(df), len(df) - len(excluded_students), excluded_students]
                }
                GRADES.update(this_class)
            except Exception:
                logger.exception("Error reading input file %s", file.name)


def _calculate_average(df: pandas.DataFrame) -> (List[str], int):
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
    avg_grade = round(non_zero_df['grade'].mean(), 1)

    return excluded, avg_grade


def write_results_to_file() -> None:
    """
    Write the results of calculating the average to an output file.
    The file name is determined by the config value OUTPUT_FILE.
    """
    sorted_grades = sorted([grade for grade in GRADES], reverse=True)
    with open(config.OUTPUT_FILE, 'w') as outfile:
        # Write the highest class average.
        # Class details is a list, structure is:
        # [class name, total # of students, # of students used, list of excluded students]
        highest_score = sorted_grades[0]
        best_class_details = GRADES[highest_score]
        outfile.write(
            ("Congratulations, {0}!\n"
            "You're the highest-performing class, "
            "with an average score of {1}!\n\n").format(
                best_class_details[0],
                highest_score
            )
        )
        outfile.write("Full summary of scores for all classes:\n")

        # Calculate average for all classes.
        sum_of_all_grades = sum([grade * GRADES[grade][2] for grade in sorted_grades])
        sum_of_included_students = sum([GRADES[grade][2] for grade in sorted_grades])
        avg_of_all_students = round((sum_of_all_grades/sum_of_included_students), 1)

        outfile.write("Average score of al classes: {0}".format(avg_of_all_students))

        for grade in sorted_grades:
            class_details = GRADES[grade]
            output_str = (
                "\nClass: {0:<5}\n"
                "Mean score: {1}\n"
                "Total # of students: {2}\n"
                "Number of included students: {3}\n"
                "Students with 0 grade:\n"
                "- {4}\n\n".format(
                    class_details[0],
                    grade,
                    class_details[1],
                    class_details[2],
                    ", ".join(name for name in class_details[3])
                )
            )
            outfile.write(output_str)


if __name__ == "__main__":
    populate_input_files_list()
    read_and_process_all_files()
    write_results_to_file()

