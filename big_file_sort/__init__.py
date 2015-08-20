__author__ = 'larry'

import heapq
import os
import tempfile


def file_chunk_lines(f, chunk_size=65536):
    """Read chunks of lines and yield them one by one
    We default to a smaller chunk than the buffer size because we will be reading this from many files at the same time

    - **parameters**, **types**, **return** and **return types**::

        :param f: A file that has already been opened for read.
        :type f: FileIO
        :param chunk_size: Optional int to specify the maximum size of the chunks to break the input into
        :type chunk_size: int

        :return: yields one line at a time from the input file
        :rtype: unicode
    """
    while f:
        lines = f.readlines(chunk_size)
        if not lines:
            break
        for line in lines:
            yield line


def break_into_temp_files(input_file, key, temp_file_location, temp_file_size):
    """
    Given an input file
    1. Break it into parts of size indicated by temp_file_size
    2. Sort each of those parts
    3. Write each of those parts to disk in a temp file
    4. Return the list of temp filenames

    - **parameters**, **types**, **return** and **return types**::

        :param input_file: Input file
        :type input_file: FileIO
        :param key: Key function to be passed to the sort algorithm
        :type key: Lambda or function to get access to comparable object
        :param temp_file_location: Location to store temporary files
        :type temp_file_location: str
        :param temp_file_size: Size of each temporary file
        :type temp_file_size: int

        :return: List of all temporary filenames created by this method
        :rtype: list
    """
    temp_filenames = []
    while input_file:
        lines = input_file.readlines(int(0.95 * temp_file_size))

        if not lines:
            input_file.close()
            input_file = None

        lines.sort(key=key)

        fd, filename = tempfile.mkstemp(dir=temp_file_location)
        tf = os.fdopen(fd, 'w')
        tf.writelines(lines)
        tf.close()
        temp_filenames.append(filename)

    return temp_filenames


def sort_file(input_filename, output_filename, key=None, temp_file_location='/tmp/large_sorted_fragments',
                 temp_file_size=1048576, buffer_size=1048576):
    """
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
    """
    with open(input_filename, 'r', buffer_size) as input_file:
        try:
            os.mkdir(temp_file_location)
        except OSError:
            # If the directory already exists, we don't need to panic
            # If this is another exception, we will fail very soon.
            pass

        temp_filenames = break_into_temp_files(input_file, key, temp_file_location, temp_file_size)

        with open(output_filename, 'w', buffer_size) as out_file:
            temp_files = [open(filename) for filename in temp_filenames]
            temp_files_iterators = [file_chunk_lines(f) for f in temp_files]
            out_file.writelines(heapq.merge(*temp_files_iterators))
            map(lambda x: x.close(), temp_files)
            map(os.remove, temp_filenames)