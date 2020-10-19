import math

import typing
import pandas


def calculate_average(df: pandas.DataFrame) -> int:
    """
    Calculate the average grade from a dataframe of grades, excluding grades
    less than 1.

    params:
    df (pandas.DataFrame): A dataframe of grades, with each row representing a
        student name and grade.

    returns:
    int: the average grade from this dataframe of grades.
    """
    non_zero_df = df[df['Grade'] > 0]
    avg_grade = round(non_zero_df['Grade'].mean(), 2)
    print(f"Mean: {avg_grade}")
