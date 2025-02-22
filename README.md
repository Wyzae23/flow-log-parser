# Flow Log Parser

## Overview

The script performs the following tasks:
- Reads a plain text file containing log flow records
- Reads a CSV lookup table mapping `(dsport, protocol)` combinations to tags
- Processes each flow log entry and determines the destination port and protocol, matching it to a tag
- Outputs two CSV files:
    - One with counts for each tag
    - One with counts for each `(port, protocol)` combination

## Assumptions
- The input file is a plain text file that is a (`.txt`) file
- The lookup table is given as a (`.csv`) file
- The output files are outputted as (`.csv`) files
- Any row in the input flow logs file that doesn't contain all 14 fields are skipped and viewed as invalid rows
- Only rows with protocol numbers from 0-19 inclusive are considered valid rows
- The `.csv` file that holds the tag counts will have a tag called `Untagged`. This tag is for any valid row that did not contain a (port, protocol) mapping in the lookup table
- the `.csv` file that holds the (port, protocol) combination counts will only hold a count for valid rows.


## Requirements
- Python 3.x
- No external libraries are needed, only the Python standard library

## How to Run
- Terminal Command: `python script.py /path/to/input.txt /path/to/lookupTable.csv`
- Example with input file and lookup table file in the same directory:
    `python script.py exampleInput.txt exampleLookupTable.csv`


## Input Files
- *Flow Log File:*
    A plain text file (`.txt`) where each line represents a flow log record with space-separated fields (expected 14 fields per line)

- *Lookup Table:*
    A CSV file (`.csv`) with a header and three columns:
    `dstport, protocol, tag`
    Each row maps a destination port and protocol combination to a tag

## Output Files
The script generates two CSV output files:
- `tag_counts_for<lookup_table_filename>_and_<input_file_filename>.csv`: Contains tag counts with columns `Tag, Count`
- `port_protocol_counts_for<lookup_table_filename>_and_<input_file_filename>.csv`: Contains counts for port, protocol combination with columns `Port, Protocol, Count`

## Tests
- Input file with rows that don't have exactly 14 fields should not consider those rows
- No matter what dstPort and protocol numbers are given, the sum of both output count files should sum up to be the same (the number of valid rows)
- Multiple occurences of the same (dstPort, protocol) should be accounted for
- Rows with invalid protocol numbers are skipped
- Empty input file
- Example Input Files Used for Testing:
    - exampleInput.txt
    - exampleInput2.txt
    - exampleInput3.txt
    - exampleInput4.txt
    - exmapleInput5.txt
- Example Lookup Tables Used for Testing:
    - exampleLookupTable.csv
    - exampleLookupTable2.csv
    - exampleLookupTable3.csv


