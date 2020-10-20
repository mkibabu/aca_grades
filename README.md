# ACA Candidate Test
Sample code to calculate the average grades of all classes.

## Requirements
- Python 3.7

## Structure:
```
├── calculate_grades
│   ├── config.py   - Configuration file
│   ├── main.py     - Main entry point
├── input
│   ├── ClassA.csv
│   ├── ClassB.csv
│   └── ClassC.csv
├── output.txt
└── README.md
```

## Execution
1. Create a Python virtual env
2. Install the dependencies
    ```
    pip install -r requirements.txt
    ```
3. Run the code:
    ```
    python calculate_grades/main.py
    ```

## Architectural Decisions
1. Used pandas to read and manipulate the csv files. Pandas make reading and
manipulating csv files easy and painless. An alternative would've been the
in-built `FileInput` module, which is made to read a lot of files passed as
an argument. However, looping over the input files list and using pandas made
it easier to keep track of each class' values.
2. Single script vs reusable module. It was easier (and faster) to create this
as a single script, because the calculations required are too small to be split
off into a separate module.
3. Synchronous file IO. Writing to a file is a blocking operation, and since
the number of files may grow, the writing operation may end up being the most
time-comsuming. However, the nature of this operation is such that we cannot
write to the output file until all calculations are done, since we first output
a summary of all the calculations. As such, I chose to use synchronous IO
rather than the `async` module and async file IO libraries like 
[aiofiles](https://pypi.org/project/aiofiles/).
4. How the input files are found. For quick scaffolding, I chose to assume that
the script would be run in the same location as the directory cntaining the
input files. A different implementation may use command-line inputs for the
files to read, or even upload hem via an API endpoint. Either way, by splitting
off how the fils are discovered from the processing, my implementation is able
to switch to whichever new way files can be discovered without changing the
way averages are calculated; only one function would need to be changed.
