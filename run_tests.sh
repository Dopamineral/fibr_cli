#!/bin/sh
#defining datetime variables
today=$(date +"%Y-%m-%d") # 2020-10-08
mkdir -p test_res/${today}/

now=$(date +"%H:%M:%S") #10:12:05
output_file=test_res/${today}/${now}_test_suite.txt

#header of file
cat > $output_file << EOL
Testing Suite

Runs the following tests for your code given they are in src and test dirs.
- black: automatic formatting
- flake8: PEP8 syntax checking in case black misses anything
- pytest: general tests
- bandit: checking for security vulnerabilities
- line_profiler: line per line time benchmarking of selected code in src/bench_main.py
- memory_profiler: line per line memroy benchmarking of selected code
-----------------------------
Date: ${today} - ${now}

EOL


cat >> $output_file << EOL
---------------
     BLACK
---------------

EOL

cat >> $output_file << EOL
| folder --> src/
| (blank if no suggestion)

EOL


black src --diff >> $output_file
black src


cat >> $output_file << EOL
| folder --> test/
| (blank if no suggestion)

EOL
black test --diff >> $output_file
black test


# Running flake8 (checking PEP8 syntax)
cat >> $output_file << EOL
---------------
     FLAKE8
---------------

EOL
# setting max-line-length to 88 as per documentation of black
cat >> $output_file << EOL
| folder --> src/
| (blank if no suggestion)

EOL
flake8 src --count --max-line-lengt=88 >> $output_file

cat >> $output_file << EOL
| folder --> test/
| (blank if no suggestion)

EOL
flake8 test --count --max-line-lengt=88 >> $output_file

# Running pytest (general testing)
cat >> $output_file << EOL
---------------
     PYTEST
---------------

EOL
pytest test/ --showlocals --tb=long --pastebin=all  >> $output_file

# Running bandit (security checker)
cat >> $output_file << EOL
---------------
     BANDIT
---------------

EOL
cat >> $output_file << EOL
| folder --> src/
| (blank if no suggestion)

EOL
bandit -r src/ -v -f txt >> $output_file
cat >> $output_file << EOL
| folder --> test/
| (blank if no suggestion)

EOL
bandit -r test/ -v -f txt >> $output_file


cat >> $output_file << EOL
--------------------------
     TIME BENCH
--------------------------

EOL

kernprof -l -v src/bench.py >> $output_file


cat >> $output_file << EOL
--------------------------
     MEMORY BENCH
--------------------------

EOL

python -m memory_profiler src/bench.py -o test.txt >> $output_file

#footer
cat >> $output_file << EOL
------------------------
© Robert Pretorius 2022

EOL

#Convert to pdf
cp $output_file recent_report.txt
libreoffice --convert-to "pdf" recent_report.txt
rm recent_report.txt
