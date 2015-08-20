=============
big_file_sort
=============
Description
-----------
Python library to sort large files by breaking them into smaller chunks, writing those to temporary files, and merging.

NAME
    big_file_sort

FUNCTIONS
    break_into_temp_files(input_file, key, temp_file_location, temp_file_size)
        Given input_filename which indicates a file of arbitrary size
        Write the same data to output_file with lines sorted by key_function
        Contents of output_file should be exactly the same size and the same number of lines

        - **parameters**, **types**, **return** and **return types**::

            :param input_filename: Filename pointing to file with line-delimited data you want to sort

            :type input_filename: str

            :param output_filename: Filename pointing to destination where sorted content will be written

            :type output_filename: str

            :param key: Optional key function to be passed to the sort algorithm

            :type key: Lambda or function to get access to comparable object

            :param temp_file_location: Optional location for temporary files - Default '/tmp/large_sorted_fragments'

            :type temp_file_location: str

            :param temp_file_size: Optional number of bytes for each chunk to break data into

            :type temp_file_size: int

            :param buffer_size: Optional number of bytes for I/O buffering

            :type buffer_size: int

            :return: None
            :rtype: None