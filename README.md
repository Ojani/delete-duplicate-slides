# delete-duplicate-slides
CLI for removing pages in a PDF file with identical text content to the on

## Usage:
The output will have the input file's name with "-no-duplicates" appended to it

`./main.py [input_file]`

when inputting a directory or using a wildcard that matches multiple files, the output_file parameter will be appended to the original name of the file to avoid naming conflicts. If only one file is matched, it's name will be whatever the parameter was set to

`./main.py [input_file] -o [output_file]`

Replacing original file (keeping the sname name)

`./main.py [input_file] -r`
