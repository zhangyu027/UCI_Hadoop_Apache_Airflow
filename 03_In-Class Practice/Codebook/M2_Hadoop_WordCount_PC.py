#!/usr/bin/env python3
"""
M2 Hadoop WordCount Practice — PC / VS Code Runnable Python File

This file is designed for Windows PC + VS Code.

It does NOT use Google Colab-only syntax:
    - no google.colab
    - no ! shell commands
    - no %%bash

What this script does:
    1. Sets JAVA_HOME and HADOOP_HOME.
    2. Checks Java and Hadoop.
    3. Creates a clean input folder.
    4. Creates one small file: student_text.txt.
    5. Runs Hadoop WordCount ONLY on student_text.txt.
    6. Prints the WordCount output.
    7. Prints student practice instructions.

Before running:
    1. Install Java 8 or Java 11.
    2. Install Hadoop 3.4.1.
    3. Update JAVA_HOME and HADOOP_HOME below if your paths are different.
    4. Run in VS Code terminal:

        python M2_Hadoop_WordCount_PC_VSCode_Runnable.py
"""

import os
import shutil
import subprocess
from pathlib import Path


# ==================================================
# 1) USER CONFIGURATION
# ==================================================
# Update these two paths if your PC uses different folders.

JAVA_HOME = r"C:\Program Files\Java\jdk-11"
HADOOP_HOME = r"C:\hadoop-3.4.1"
HADOOP_VERSION = "3.4.1"


# ==================================================
# 2) PATH SETTINGS
# ==================================================
USER_HOME = Path.home()

INPUT_DIR = USER_HOME / "student_wordcount_input"
OUTPUT_DIR = USER_HOME / "student_wordcount_output"
STUDENT_FILE = INPUT_DIR / "student_text.txt"

HADOOP_CMD = Path(HADOOP_HOME) / "bin" / "hadoop.cmd"

MAPREDUCE_EXAMPLES_JAR = (
    Path(HADOOP_HOME)
    / "share"
    / "hadoop"
    / "mapreduce"
    / f"hadoop-mapreduce-examples-{HADOOP_VERSION}.jar"
)


# ==================================================
# 3) SET ENVIRONMENT VARIABLES
# ==================================================
def setup_environment():
    os.environ["JAVA_HOME"] = JAVA_HOME
    os.environ["HADOOP_HOME"] = HADOOP_HOME

    os.environ["PATH"] = (
        str(Path(HADOOP_HOME) / "bin")
        + os.pathsep
        + str(Path(HADOOP_HOME) / "sbin")
        + os.pathsep
        + os.environ.get("PATH", "")
    )

    print("=" * 70)
    print("Environment")
    print("=" * 70)
    print(f"JAVA_HOME   = {JAVA_HOME}")
    print(f"HADOOP_HOME = {HADOOP_HOME}")
    print()


# ==================================================
# 4) COMMAND HELPER
# ==================================================
def run_command(command, allow_fail=False):
    print("-" * 70)
    print("Running command:")
    print(" ".join(map(str, command)))
    print("-" * 70)

    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
        env=os.environ.copy()
    )

    if result.stdout:
        print("STDOUT:")
        print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    if result.returncode != 0 and not allow_fail:
        raise RuntimeError(
            f"Command failed with return code {result.returncode}"
        )

    return result


# ==================================================
# 5) CHECK JAVA AND HADOOP INSTALLATION
# ==================================================
def check_installation():
    print("=" * 70)
    print("Checking Java and Hadoop installation")
    print("=" * 70)

    if not Path(JAVA_HOME).exists():
        print(f"WARNING: JAVA_HOME path does not exist: {JAVA_HOME}")
        print("Please update JAVA_HOME near the top of this script.")
        print()

    if not Path(HADOOP_HOME).exists():
        raise FileNotFoundError(
            f"HADOOP_HOME does not exist: {HADOOP_HOME}\n"
            "Please install Hadoop or update HADOOP_HOME near the top of this script."
        )

    if not HADOOP_CMD.exists():
        raise FileNotFoundError(
            f"Hadoop command not found: {HADOOP_CMD}\n"
            "Please check your Hadoop installation."
        )

    if not MAPREDUCE_EXAMPLES_JAR.exists():
        raise FileNotFoundError(
            f"MapReduce examples jar not found:\n{MAPREDUCE_EXAMPLES_JAR}"
        )

    run_command(["java", "-version"])
    run_command([str(HADOOP_CMD), "version"])


# ==================================================
# 6) CREATE CLEAN STUDENT INPUT FILE
# ==================================================
def create_student_text_file():
    print("=" * 70)
    print("Creating clean student input file")
    print("=" * 70)

    if INPUT_DIR.exists():
        shutil.rmtree(INPUT_DIR)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    student_text = """Hadoop helps count words
Hadoop works with big data
Students practice Hadoop WordCount
Data data data is everywhere
WordCount counts each word
"""

    STUDENT_FILE.write_text(student_text, encoding="utf-8")

    print("Student file created:")
    print(STUDENT_FILE)
    print()
    print("Student file content:")
    print(STUDENT_FILE.read_text(encoding="utf-8"))


# ==================================================
# 7) RUN HADOOP WORDCOUNT ONLY ON student_text.txt
# ==================================================
def run_wordcount_on_student_file():
    print("=" * 70)
    print("Running Hadoop WordCount on student_text.txt only")
    print("=" * 70)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    wordcount_command = [
        str(HADOOP_CMD),
        "jar",
        str(MAPREDUCE_EXAMPLES_JAR),
        "wordcount",
        str(STUDENT_FILE),
        str(OUTPUT_DIR)
    ]

    run_command(wordcount_command)


# ==================================================
# 8) DISPLAY WORDCOUNT OUTPUT
# ==================================================
def display_wordcount_output():
    print("=" * 70)
    print("WordCount output")
    print("=" * 70)

    output_files = sorted(OUTPUT_DIR.glob("part-*"))

    if not output_files:
        print("No output file found.")
        return

    for output_file in output_files:
        print(f"Output file: {output_file}")
        print(output_file.read_text(encoding="utf-8", errors="ignore"))


# ==================================================
# 9) STUDENT PRACTICE INSTRUCTIONS
# ==================================================
def print_student_practice():
    print("""
======================================================================
STUDENT PRACTICE
======================================================================

Practice instructions:

1. Open this file on your PC:

   student_wordcount_input/student_text.txt

2. Replace the sample text with your own 5 or more lines.

Example idea:

   People in those industries often travel globally.
   They move between projects.
   They work with multiple contractors and business groups.
   Some periods are very intense.
   Other periods are quieter.

3. Rerun this Python file in VS Code:

   python M2_Hadoop_WordCount_PC_VSCode_Runnable.py

4. Answer:

   a. Which word appears most often?
   b. Did the WordCount output change?
   c. Why did the count change?
   d. What is the difference between running WordCount on one file versus an entire folder?

Important:

This script reads ONLY:

   student_text.txt

It does NOT read every file in the input folder.
======================================================================
""")


# ==================================================
# 10) MAIN
# ==================================================
def main():
    setup_environment()
    check_installation()
    create_student_text_file()
    run_wordcount_on_student_file()
    display_wordcount_output()
    print_student_practice()


if __name__ == "__main__":
    main()
