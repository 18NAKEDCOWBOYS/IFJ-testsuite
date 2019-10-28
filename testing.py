# Testing framework for IFJ 2019 projects

import pytest
import subprocess
import logging
import os
import shutil

# Error constants for compiler
ERR_COMP_OK = 0
ERR_COMP_LEX = 1
ERR_COMP_SYN = 2
ERR_COMP_SEM_DEF = 3
ERR_COMP_SEM_TYPE = 4
ERR_COMP_SEM_PAR = 5
ERR_COMP_SEM_OTHER = 6
# Error constants for interpreter
ERR_INT_OK = 0
ERR_INT_PARAM = 50
ERR_INT_ANALYZE = 51
ERR_INT_SEM = 52
ERR_INT_RUN_OPER = 53
ERR_INT_RUN_VAR = 54
ERR_INT_RUN_FRAME = 55
ERR_INT_RUN_NOVAL = 56
ERR_INT_RUN_BADVAL = 57
ERR_INT_RUN_STRING = 58

"""
START OF CONFIGURATION
"""

# Testing configuration
# MUST CONFIGURE !!!
# Path to IFJ19 compiler executable file
IFJCOMP_EXECUTABLE = "../IFJ-pytest-old/comp"
# If True, only compile the test program and check return code
COMPILE_ONLY = False
# If True, only compile and interpret the test program, but do not compare it with python interpretation
COMPILE_AND_INTERPRET_ONLY = False

#MAY CONFIGURE
# Path to template file to enable IFJ19 code to be run by python
IFJ_19_TEMPLATE_FILE ="./ifj19.py"
# Path to temporaly file to store compiler output 
TMP_FILE = "./tmp_file"
# Python interpreter for output comparison
PYTHON_INTERPRETER = "python3"
# Path to ic19 interpreter
ICL_INTERPRETTER = "./ic19int"
# Path to folder for incorrect outputs from IFJ 19 compiler
OUTPUT_FOLDER = "./outputs"
# Folder with test source files
TESTS_FOLDER = "./tests"
# Timeout for each test to cmplete
SINGLE_TEST_TIMEOUT = 10

# Tests
# (source_file, compiler_exit_code, interpret_exit_code, program_input)
tests = [
    # Basic tests from assignmnet
    ("factorial.py", ERR_COMP_OK, ERR_INT_OK, "5"),
    ("factorial.py", ERR_COMP_OK, ERR_INT_OK, "2"),
    ("factorial.py", ERR_COMP_OK, ERR_INT_OK, "a"),
    ("factorial.py", ERR_COMP_OK, ERR_INT_OK, None),
    ("factorial2.py", ERR_COMP_OK, ERR_INT_OK, "5"),
    ("factorial2.py", ERR_COMP_OK, ERR_INT_OK, "2"),
    ("factorial2.py", ERR_COMP_OK, ERR_INT_OK, "a"),
    ("factorial2.py", ERR_COMP_OK, ERR_INT_OK, None),
    ("buildin.py", ERR_COMP_OK, ERR_INT_OK, "abcdefgh\nabcdefgh"),
    ("buildin.py", ERR_COMP_OK, ERR_INT_OK, "abcdefgh"),
    # Lexical analysis tests
    ("badcomment.py", ERR_COMP_LEX, None, None),
    ("baddot.py", ERR_COMP_LEX, None, None),
    ("badchars.py", ERR_COMP_LEX, None, None),
    ("badcomment2.py", ERR_COMP_LEX, None, None),
    ("badexponent.py", ERR_COMP_LEX, None, None),
    ("badindent.py", ERR_COMP_LEX, None, None),
    ("badindent2.py", ERR_COMP_LEX, None, None),
    ("badstring.py", ERR_COMP_LEX, None, None),
    ("emptyexponent.py", ERR_COMP_LEX, None, None),
    ("morezeroes.py", ERR_COMP_LEX, None, None),
    ("nonasci.py", ERR_COMP_LEX, None, None),
    ("specstring.py", ERR_COMP_OK, ERR_INT_OK, None),
    # Syntax analysis tests
    ("badfunction.py", ERR_COMP_SYN, None, None),
    ("badfunction2.py", ERR_COMP_SYN, None, None),
    ("badfunction3.py", ERR_COMP_SYN, None, None),
    ("badfunction4.py", ERR_COMP_SYN, None, None),
    ("badfunction5.py", ERR_COMP_SYN, None, None),
    ("badfunction6.py", ERR_COMP_SYN, None, None),
    ("badfunction7.py", ERR_COMP_SYN, None, None),
    ("badindent3.py", ERR_COMP_SYN, None, None),
    ("badwhile.py", ERR_COMP_SYN, None, None),
    ("badwhile2.py", ERR_COMP_SYN, None, None),
    ("badwhile3.py", ERR_COMP_SYN, None, None),
    ("badif.py", ERR_COMP_SYN, None, None),
    ("badif2.py", ERR_COMP_SYN, None, None),
    ("badif3.py", ERR_COMP_SYN, None, None),
    ("badreturn.py", ERR_COMP_SYN, None, None),
    ("badcall.py", ERR_COMP_SYN, None, None),
    ("badcall2.py", ERR_COMP_SYN, None, None),
    ("badcall3.py", ERR_COMP_SYN, None, None),
    ("emptyprogram.py", ERR_COMP_OK, ERR_INT_OK, None),
    ("badexpr.py", ERR_COMP_SYN, None, None),
    ("badexpr2.py", ERR_COMP_SYN, None, None),
    ("badexpr3.py", ERR_COMP_SYN, None, None),
    ("badexpr4.py", ERR_COMP_SYN, None, None),
    ("badexpr5.py", ERR_COMP_SYN, None, None),
    # Semantics analysis tests
    ("badvar.py", ERR_COMP_SEM_DEF, None, None),
    ("badvar2.py", ERR_COMP_SEM_DEF, None, None),
    ("badvar3.py", ERR_COMP_SEM_DEF, None, None),
    ("badfunction8.py", ERR_COMP_SEM_DEF, None, None),
    ("badfunction9.py", ERR_COMP_SEM_DEF, None, None),
    ("badfunction10.py", ERR_COMP_SEM_DEF, None, None),
    ("badcall4.py", ERR_COMP_SEM_DEF, None, None),
    ("badcall5.py", ERR_COMP_SEM_DEF, None, None),
    # Interpret error tests
    ("badtype.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badtype2.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badtype3.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badtype4.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badtype5.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badtype6.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badtype7.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badtype8.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badtype9.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("zerodiv.py", ERR_COMP_OK, ERR_INT_RUN_BADVAL, None),
    ("zerodiv2.py", ERR_COMP_OK, ERR_INT_RUN_BADVAL, None),
    # Buildin functions tests
    ("badbuildin.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badbuildin2.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badbuildin3.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badbuildin4.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badbuildin5.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badbuildin6.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badbuildin7.py", ERR_COMP_OK, ERR_INT_RUN_OPER, None),
    ("badbuildin8.py", ERR_COMP_OK, ERR_INT_RUN_STRING, None)
    # TODO correct programs
]

"""
END OF CONFIGURATION
"""

test_index = 0
test_id = ""

def run_python(test_source, program_input):
    f = open(IFJ_19_TEMPLATE_FILE, "r")
    template_content = f.read()
    f.close()
    f = open(test_source, "r")
    program_content = f.read()
    f.close()
    f = open(TMP_FILE, "w")
    f.write(template_content + program_content)
    f.close()
    cmd = [PYTHON_INTERPRETER, TMP_FILE]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    capture_out, capture_err = process.communicate(input=program_input)
    return {"exit_code" : process.returncode,
            "stdout" : capture_out,
            "stderr" : capture_err}

def run_ifjcomp(test_source):
    f = open(test_source, 'rb')
    cmd = IFJCOMP_EXECUTABLE
    process = subprocess.Popen(cmd, stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    capture_out, capture_err = process.communicate()
    f.close()
    return {"exit_code" : process.returncode,
            "stdout" : capture_out,
            "stderr" : capture_err}

def run_iclint(input_data, program_input):
    f = open(TMP_FILE, "w")
    f.write(input_data)
    f.close()
    cmd = [ICL_INTERPRETTER, TMP_FILE]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    capture_out, capture_err = process.communicate(input=program_input)
    return {"exit_code" : process.returncode,
            "stdout" : capture_out,
            "stderr" : capture_err}

def check_compiler_error(process_info, error_code):
    if process_info["exit_code"] != error_code:
        logging.info("Compiler error output:\n" + (process_info["stderr"] or "<empty>"))
        logging.info("----")
        error = "Unexpected exit code of IFJ compiler. Actual:" + str(process_info["exit_code"]) + " Expected: " + str(error_code) + "."
        logging.error("ERROR:" + error)
        raise RuntimeError(test_id + " - " + error)

def check_interpret_error(process_info, error_code):
    if process_info["exit_code"] != error_code:
        logging.info("Interpret error output:\n" + (process_info["stderr"] or "<empty>"))
        logging.info("----")
        error = "Unexpected exit code of IFJ interpreter. Actual:" + str(process_info["exit_code"]) + " Expected: " + str(error_code) + "."
        logging.error("ERROR:" + error)
        raise RuntimeError(test_id + " - " + error)

def check_same_output(interpret_info, python_info):
    if interpret_info["exit_code"] != python_info["exit_code"]:
        logging.info("Python error output:\n" + (python_info["stderr"] or "<empty>"))
        logging.info("----")
        logging.info("Interpret error output:\n" + (interpret_info["stderr"] or "<empty>"))
        logging.info("--------")
        error = "Python and IFJ interprets have different exit codes. Python: " + str(python_info["exit_code"]) + " IFJ: " + str(interpret_info["exit_code"]) + "."
        logging.error("ERROR:" + error)
        raise RuntimeError(test_id + " - " + error)
    if interpret_info["stdout"] != python_info["stdout"]:
        logging.info("Python error output:\n" + (python_info["stderr"] or "<empty>"))
        logging.info("----")
        logging.info("Interpret error output:\n" + (interpret_info["stderr"] or "<empty>"))
        logging.info("--------")
        logging.info("Python output:\n" + (python_info["stdout"] or "<empty>"))
        logging.info("----")
        logging.info("Interpret output:\n" + (interpret_info["stdout"] or "<empty>"))
        logging.info("--------")
        error = "Python and IFJ interprets have different outputs."
        logging.error("ERROR:" + error)
        raise RuntimeError(test_id + " - " + error)

def setup_module():
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    os.mkdir(OUTPUT_FOLDER)

def teardown_module():
    if os.path.exists(TMP_FILE):
        os.remove(TMP_FILE)

def pytest_addoption(parser):
    parser.addoption("--mode", action="store_true", help="run all combinations")

@pytest.mark.timeout(SINGLE_TEST_TIMEOUT)
@pytest.mark.parametrize("test_file,comp_code,int_code,program_input", tests)
def test_IFJ_project(test_file, comp_code, int_code, program_input):
    global test_index
    global test_id
    test_index = test_index + 1
    test_id = test_file
    logging.info("\n********************\nTEST " + str(test_index) + ": " + test_id + "\n********************\n")
    test_file_path = TESTS_FOLDER + "/" + test_file
    compiler_info = run_ifjcomp(test_file_path)
    check_compiler_error(compiler_info, comp_code)
    if COMPILE_ONLY or (comp_code != 0):
        return

    try:
        interpret_info = run_iclint(compiler_info["stdout"], program_input)
        check_interpret_error(interpret_info, int_code)
        if COMPILE_AND_INTERPRET_ONLY or (int_code != 0):
            return

        python_info = run_python(test_file_path, program_input)
        check_same_output(interpret_info, python_info)
    except:
        f = open(OUTPUT_FOLDER + "/" + test_file + ".ifj19code", "w")
        f.write(compiler_info["stdout"])
        f.close()
        raise
