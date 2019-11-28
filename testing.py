# Testing framework for IFJ 2019 projects

"""
SCRIPT FILE - DO NOT EDIT
"""

import pytest
import subprocess
import logging
import os
import shutil

from config import *

# Global variables
test_index = 0
test_id = ""

# Run test on native python interpreter
def run_python(test_source, program_input):
    # read template file to enable interpretation of ifj19 with native python
    f = open(IFJ_19_TEMPLATE_FILE, "r")
    template_content = f.read()
    f.close()
    # Read test source file
    f = open(test_source, "r")
    program_content = f.read()
    f.close()
    # Generate source file native python
    f = open(TMP_FILE, "w")
    f.write(template_content + program_content)
    f.close()
    # Execute test on native python
    cmd = [PYTHON_INTERPRETER, TMP_FILE]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    capture_out, capture_err = process.communicate(input=program_input)
    # Return info about the execution
    return {"exit_code" : process.returncode,
            "stdout" : capture_out,
            "stderr" : capture_err}

# Run test on ifj19 compiler
def run_ifjcomp(test_source):
    # Open test source
    f = open(test_source, 'rb')
    # Execute test on ifj19 compiler
    cmd = IFJCOMP_EXECUTABLE
    process = subprocess.Popen(cmd, stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    capture_out, capture_err = process.communicate()
    # Close test source
    f.close()
    # Return info about the execution
    return {"exit_code" : process.returncode,
            "stdout" : capture_out,
            "stderr" : capture_err}

# Run interpret witj intermediate code
def run_iclint(input_data, program_input):
    # Save intermediate code to file
    f = open(TMP_FILE, "w")
    f.write(input_data)
    f.close()
    # Execute code on interpreter
    cmd = [ICL_INTERPRETTER, TMP_FILE]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    capture_out, capture_err = process.communicate(input=program_input)
    # Return info about the execution
    return {"exit_code" : process.returncode,
            "stdout" : capture_out,
            "stderr" : capture_err}

# Check error code from ifj19 compiler
def check_compiler_error(process_info, error_code):
    # Check for correct error code
    if process_info["exit_code"] not in error_code:
	# Log error
        logging.info("Compiler error output:\n" + (process_info["stderr"] or "<empty>"))
        logging.info("----")
        error = "Unexpected exit code of IFJ compiler. Actual: " + str(process_info["exit_code"]) + " Expected: " + str(error_code) + "."
        logging.error("ERROR: " + error)
	# Fail test
        raise RuntimeError(test_id + " - " + error)

# Check error code from ifj19 interpreter
def check_interpret_error(process_info, error_code):
    if process_info["exit_code"] not in error_code:
	# Log error
        logging.info("Interpret error output:\n" + (process_info["stderr"] or "<empty>"))
        logging.info("----")
        error = "Unexpected exit code of IFJ interpreter. Actual: " + str(process_info["exit_code"]) + " Expected: " + str(error_code) + "."
        logging.error("ERROR: " + error)
	# Fail test
        raise RuntimeError(test_id + " - " + error)

# Check output from native python and ifj19 interpreter
def check_same_output(interpret_info, python_info):
    # Check if python and ifj19 have the save exit code
    if interpret_info["exit_code"] != python_info["exit_code"]:
	# Log error
        logging.info("Python error output:\n" + (python_info["stderr"] or "<empty>"))
        logging.info("----")
        logging.info("Interpret error output:\n" + (interpret_info["stderr"] or "<empty>"))
        logging.info("----")
        error = "Python and IFJ interprets have different exit codes. Python: " + str(python_info["exit_code"]) + " IFJ: " + str(interpret_info["exit_code"]) + "."
        logging.error("ERROR: " + error)
	# Fail test
        raise RuntimeError(test_id + " - " + error)

    # Check standart output of python and ifj19
    if interpret_info["stdout"] != python_info["stdout"]:
	# Log error
        logging.info("Python error output:\n" + (python_info["stderr"] or "<empty>"))
        logging.info("----")
        logging.info("Interpret error output:\n" + (interpret_info["stderr"] or "<empty>"))
        logging.info("----")
        logging.info("Python output:\n" + (python_info["stdout"] or "<empty>"))
        logging.info("----")
        logging.info("Interpret output:\n" + (interpret_info["stdout"] or "<empty>"))
        logging.info("----")
        error = "Python and IFJ interprets have different outputs."
        logging.error("ERROR: " + error)
	# Fail test
        raise RuntimeError(test_id + " - " + error)

# Check if test can be run according to implemented expansions
def check_extentions(must, cant):

    def get_extention_name(extend):
	if extend == EXTEND_BOOLOOP:
            return "BOOLOOP"
        elif extend == EXTEND_BASE:
            return "BASE"
        elif extend == EXTEND_CYCLES:
            return "CYCLES"
        elif extend == EXTEND_FUNEXP:
            return "FUNEX"
        elif extend == EXTEND_IFTHEN:
            return "IFTHEN"
        else:
            return "UNKNOWN"

    for extention in IMPLEMENTED_EXTENTIONS:
        if extention in cant:
            logging.info("Test skipped")
            logging.info("Reason: extention" + get_extention_name(extention) + " is implemented but not allowed.")
            pytest.skip("Extention mismatch")
    for extention in must:
        if extention in IMPLEMENTED_EXTENTIONS:
            logging.info("Test skipped")
            logging.info("Reason: extantion" + get_extention_name(extention) + " is not implemented but required.")
            pytest.skip("Extention mismatch")

# Setup before first test
def setup_module():
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    os.mkdir(OUTPUT_FOLDER)

# Clean up after last test
def teardown_module():
    if os.path.exists(TMP_FILE):
        os.remove(TMP_FILE)

# Execution of single test
@pytest.mark.timeout(SINGLE_TEST_TIMEOUT)
@pytest.mark.parametrize("test_file,comp_code,int_code,program_input,extention_must,extentions_cant", tests)
def test_IFJ_project(test_file, comp_code, int_code, program_input, extention_must, extentions_cant):
    # Global variables must be accessed here
    global test_index
    global test_id
    test_index = test_index + 1
    test_id = test_file
    # Log current test
    logging.info("\n********************\nTEST " + str(test_index) + ": " + test_id + "\n********************\n")
    if program_input is not None:
        logging.info("PROGRAM INPUT:")
        logging.info(program_input)
        logging.info("----")
    # Check extentions
    check_extentions(extention_must, extentions_cant)
    # Run ifj19 compiler
    test_file_path = TESTS_FOLDER + "/" + test_file
    compiler_info = run_ifjcomp(test_file_path)
    # Check compiler for error
    check_compiler_error(compiler_info, comp_code)
    # End execution if tests are compile only
    if TESTING_MODE == MODE_COMPILE or (compiler_info["exit_code"] != 0):
        if TESTING_MODE == MODE_COMPILE and (compiler_info["exit_code"] == 0):
	    # Log warning about incomplete testing
            logging.info("WARNING: This test was not entirely completed, because of the MODE_COMPILE testing mode.")
            logging.info("         Interpretation and output checks were not run.")
            logging.info("----")
        logging.info("SUCCESS")
        return

    # If this part failes, the intermedate code must be saved for further analysis
    try:
	# Run ifj19 interpret
        interpret_info = run_iclint(compiler_info["stdout"], program_input)
	# Check interpret for error
        check_interpret_error(interpret_info, int_code)
	# End execution if tests are compile and interpret only
        if TESTING_MODE == MODE_INTERPRET or (interpret_info["exit_code"] != 0):
            if TESTING_MODE == MODE_INTERPRET and (interpret_info["exit_code"] == 0):
		# Log warning about incomplete testing
                logging.info("WARNING: This test was not entirely completed, because of the MODE_INTERPRET testing mode.")
                logging.info("         Output checks were not run.")
                logging.info("----")
            logging.info("SUCCESS")
            return

	# Run test on native python and compare results with ifj19
        python_info = run_python(test_file_path, program_input)
        check_same_output(interpret_info, python_info)
    except:
	# Save intermetiate code
        f = open(OUTPUT_FOLDER + "/" + test_file + ".ifj19code", "w")
        f.write(compiler_info["stdout"])
        f.close()
        raise

    # Test successfull
    logging.info("SUCCESS")
