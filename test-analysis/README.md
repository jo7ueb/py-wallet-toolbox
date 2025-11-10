# This README explains the project
We have a ts library and a py library
The py test cases were generated from the ts library tests
In order to ensure the tests are functionally similar enough to warrant marking as good enough we have written several scripts
The first script generate_matching_tests.py creates a matching_tests.md file
That file is parsed by parse_matching_tests.py which creates a test_ranges.json file
That file is then used by compare_test_implementations_hybrid.py and a test_comparison_detailed_report.md file is created
That file is then analyzed by auto_test_fixer.py and attempts are made to patch the FAIL-ed tests

