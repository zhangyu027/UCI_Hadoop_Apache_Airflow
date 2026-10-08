#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3 Hadoop MapReduce runner for VS Code / Jupyter.

FINAL PATHS USED:
    Codebook folder:
        /Users/yuzhang/projects/UCI_Hadoop_Apache_Airflow/Assignments/Codebook/

    Mapper:
        /Users/yuzhang/projects/UCI_Hadoop_Apache_Airflow/Assignments/Codebook/mapper2.py

    Reducer:
        /Users/yuzhang/projects/UCI_Hadoop_Apache_Airflow/Assignments/Codebook/reducer.py

    Outputs folder:
        /Users/yuzhang/projects/UCI_Hadoop_Apache_Airflow/Assignments/Outputs/
"""

from pathlib import Path
import subprocess
import shutil
import sys
import os

# ============================================================
# FINAL ABSOLUTE PATHS
# ============================================================
PROJECT_ROOT = Path("/Users/yuzhang/projects/UCI_Hadoop_Apache_Airflow")
ASSIGNMENTS_DIR = PROJECT_ROOT / "Assignments"
CODEBOOK_DIR = ASSIGNMENTS_DIR / "Codebook"
DATASET_DIR = ASSIGNMENTS_DIR / "Dataset"
OUTPUTS_DIR = ASSIGNMENTS_DIR / "Outputs"

MAPPER = CODEBOOK_DIR / "mapper2.py"
REDUCER = CODEBOOK_DIR / "reducer.py"

INPUT_FILE = DATASET_DIR / "input.txt"
LOCAL_OUTPUT_FILE = OUTPUTS_DIR / "m3_wordcount_output_local.txt"
HADOOP_OUTPUT_DIR = OUTPUTS_DIR / "m3_wordcount_hadoop_output"


# ============================================================
# SETUP
# ============================================================
def ensure_folders() -> None:
    CODEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Codebook folder: {CODEBOOK_DIR}")
    print(f"[INFO] Dataset folder:  {DATASET_DIR}")
    print(f"[INFO] Outputs folder:  {OUTPUTS_DIR}")


def ensure_sample_input() -> None:
    """Create a small sample input only if no input file exists."""
    if not INPUT_FILE.exists():
        INPUT_FILE.write_text(
            "Hadoop is useful for big data.\n"
            "Hadoop MapReduce uses mapper and reducer files.\n"
            "This assignment runs mapper2.py and reducer.py.\n",
            encoding="utf-8",
        )
        print(f"[INFO] Created sample input file: {INPUT_FILE}")
    else:
        print(f"[INFO] Using existing input file: {INPUT_FILE}")


def ensure_mapper_reducer_exist() -> None:
    """Check that mapper2.py and reducer.py are in the exact Codebook folder."""
    missing = []
    if not MAPPER.exists():
        missing.append(str(MAPPER))
    if not REDUCER.exists():
        missing.append(str(REDUCER))

    if missing:
        raise FileNotFoundError(
            "Missing required file(s):\n"
            + "\n".join(missing)
            + "\n\nPlease place mapper2.py and reducer.py in this folder:\n"
            + str(CODEBOOK_DIR)
        )

    print(f"[INFO] Mapper found:  {MAPPER}")
    print(f"[INFO] Reducer found: {REDUCER}")


def clean_output() -> None:
    """Remove old outputs before a new run."""
    if LOCAL_OUTPUT_FILE.exists():
        LOCAL_OUTPUT_FILE.unlink()
    if HADOOP_OUTPUT_DIR.exists():
        shutil.rmtree(HADOOP_OUTPUT_DIR)
    print("[INFO] Previous output removed.")


# ============================================================
# HADOOP HELPERS
# ============================================================
def find_hadoop_command():
    """Try to find Hadoop command on Mac or local project folders."""
    possible = [
        "hadoop",
        "/opt/homebrew/bin/hadoop",
        "/usr/local/bin/hadoop",
        str(PROJECT_ROOT / "hadoop-3.4.1/bin/hadoop"),
        str(Path.home() / "hadoop-3.4.1/bin/hadoop"),
    ]
    for cmd in possible:
        if shutil.which(cmd) or Path(cmd).exists():
            return cmd
    return None


def find_streaming_jar():
    """
    Try to find the Hadoop Streaming jar without scanning the entire Mac home folder.

    The previous version used Path.home().rglob(...), which can search thousands of
    files and make the script appear frozen. This version checks only common Hadoop
    locations and supports an optional HADOOP_STREAMING_JAR environment variable.
    """
    env_jar = os.environ.get("HADOOP_STREAMING_JAR")
    if env_jar and Path(env_jar).exists():
        return env_jar

    possible_files = [
        Path("/opt/homebrew/opt/hadoop/libexec/share/hadoop/tools/lib/hadoop-streaming.jar"),
        Path("/usr/local/opt/hadoop/libexec/share/hadoop/tools/lib/hadoop-streaming.jar"),
    ]

    for file_path in possible_files:
        if file_path.exists():
            return str(file_path)

    possible_dirs = [
        Path("/opt/homebrew/opt/hadoop/libexec/share/hadoop/tools/lib"),
        Path("/usr/local/opt/hadoop/libexec/share/hadoop/tools/lib"),
        Path("/opt/homebrew/Cellar/hadoop"),
        Path("/usr/local/Cellar/hadoop"),
        PROJECT_ROOT / "hadoop-3.4.1/share/hadoop/tools/lib",
        Path.home() / "hadoop-3.4.1/share/hadoop/tools/lib",
    ]

    candidates = []
    for folder in possible_dirs:
        if folder.exists():
            # Limit recursive searching to Hadoop installation folders only.
            candidates.extend(folder.glob("hadoop-streaming*.jar"))
            candidates.extend(folder.glob("**/hadoop-streaming*.jar"))

    candidates = sorted(set(candidates))
    return str(candidates[0]) if candidates else None


def run_command(command, input_text=None):
    return subprocess.run(
        command,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


# ============================================================
# LOCAL MAPREDUCE FALLBACK
# ============================================================
def run_local_mapreduce() -> None:
    """Run mapper2.py and reducer.py locally, so this works even without Hadoop."""
    print("[INFO] Running local MapReduce fallback...")
    input_text = INPUT_FILE.read_text(encoding="utf-8", errors="ignore")

    mapper_result = run_command([sys.executable, str(MAPPER)], input_text=input_text)
    if mapper_result.returncode != 0:
        raise RuntimeError(f"Mapper failed:\n{mapper_result.stderr}")

    # Hadoop sorts mapper output before reducer. We do the same locally.
    sorted_mapper_output = "\n".join(sorted(mapper_result.stdout.splitlines())) + "\n"

    reducer_result = run_command([sys.executable, str(REDUCER)], input_text=sorted_mapper_output)
    if reducer_result.returncode != 0:
        raise RuntimeError(f"Reducer failed:\n{reducer_result.stderr}")

    LOCAL_OUTPUT_FILE.write_text(reducer_result.stdout, encoding="utf-8")
    print(f"[SUCCESS] Local output saved to:\n{LOCAL_OUTPUT_FILE}")


# ============================================================
# HADOOP STREAMING RUN
# ============================================================
def run_hadoop_streaming(hadoop_cmd, streaming_jar) -> bool:
    """Run Hadoop Streaming if Hadoop is available."""
    print("[INFO] Trying Hadoop Streaming...")

    command = [
        hadoop_cmd,
        "jar",
        streaming_jar,
        "-files",
        f"{MAPPER},{REDUCER}",
        "-mapper",
        f"{sys.executable} mapper2.py",
        "-reducer",
        f"{sys.executable} reducer.py",
        "-input",
        str(INPUT_FILE),
        "-output",
        str(HADOOP_OUTPUT_DIR),
    ]

    print("[INFO] Running command:")
    print(" ".join(command))

    result = run_command(command)
    if result.returncode == 0:
        print("[SUCCESS] Hadoop Streaming completed.")
        print(result.stdout)
        return True

    print("[WARNING] Hadoop Streaming failed. Falling back to local MapReduce.")
    print(result.stderr)
    return False


# ============================================================
# DISPLAY OUTPUT
# ============================================================
def display_output() -> None:
    print("\n================ WORD COUNT OUTPUT ================\n")

    hadoop_parts = sorted(HADOOP_OUTPUT_DIR.glob("part-*")) if HADOOP_OUTPUT_DIR.exists() else []
    if hadoop_parts:
        for part in hadoop_parts:
            print(f"Output file: {part}")
            print(part.read_text(encoding="utf-8", errors="ignore"))
        return

    if LOCAL_OUTPUT_FILE.exists():
        print(f"Output file: {LOCAL_OUTPUT_FILE}")
        print(LOCAL_OUTPUT_FILE.read_text(encoding="utf-8", errors="ignore"))
        return

    print("No output file found.")


# ============================================================
# MAIN
# ============================================================
def main() -> None:
    ensure_folders()
    ensure_sample_input()
    ensure_mapper_reducer_exist()
    clean_output()

    hadoop_cmd = find_hadoop_command()
    streaming_jar = find_streaming_jar()

    if hadoop_cmd and streaming_jar:
        ok = run_hadoop_streaming(hadoop_cmd, streaming_jar)
        if not ok:
            clean_output()
            run_local_mapreduce()
    else:
        print("[INFO] Hadoop command or streaming jar not found.")
        print("[INFO] Using local MapReduce fallback.")
        run_local_mapreduce()

    display_output()


if __name__ == "__main__":
    main()
