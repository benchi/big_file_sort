import os
import random
import unittest

import big_file_sort


class BigFileSort(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def verify_contents_same_length(self, input_lines, output_lines):
        input_len = sum([len(x) for x in input_lines])
        output_len = sum([len(x) for x in output_lines])
        self.assertEqual(input_len, output_len)

    def verify_files_same_size(self, input_file, output_file):
        self.assertEqual(os.stat(input_file).st_size, os.stat(output_file).st_size)

    def verify_contents_same_num_lines(self, input_lines, output_lines):
        self.assertEqual(len(input_lines), len(output_lines))

    def verify_contents_sorted(self, output_lines):
        for i, line in enumerate(output_lines[:-1]):
            self.assertGreaterEqual(output_lines[i + 1], line)

    def verify_good(self, input_filename, output_filename):
        self.verify_files_same_size(input_filename, output_filename)

        with open(input_filename, 'r') as input_file:
            with open(output_filename, 'r') as output_file:
                input_lines = input_file.readlines()
                output_lines = output_file.readlines()

                self.verify_contents_same_num_lines(input_lines, output_lines)
                self.verify_contents_same_length(input_lines, output_lines)
                self.verify_contents_sorted(output_lines)

    def helper_test_input_file(self, input_file):
        output_file = '/tmp/big_file_sort_test_%s' % (random.randint(0, 10000))
        big_file_sort.sort_file(input_file, output_file)
        self.verify_good(input_file, output_file)

        big_file_sort.sort_file(input_file, output_file, temp_file_size=1)
        self.verify_good(input_file, output_file)

        big_file_sort.sort_file(input_file, output_file, buffer_size=1)
        self.verify_good(input_file, output_file)

        big_file_sort.sort_file(input_file, output_file, temp_file_size=1, buffer_size=1)
        self.verify_good(input_file, output_file)

    def test_empty(self):
        self.helper_test_input_file('empty.txt')

    def test_normal(self):
        self.helper_test_input_file('100lines.txt')

    def test_one_line(self):
        self.helper_test_input_file('1line.txt')


suite = unittest.TestLoader().loadTestsFromTestCase(BigFileSort)
unittest.TextTestRunner(verbosity=2).run(suite)
