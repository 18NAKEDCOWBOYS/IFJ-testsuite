# Testing framework for IFJ 2020 projects

"""
USER TESTING SCRIPT - RUN BUT DO NOT EDIT
"""

# Imports
import argparse
import os
import json
import subprocess

# Default argument values
DEFAULT_COMPILER_PATH = './ifj20'
DEFAULT_LOG_FILE = './log.txt'
DEFAULT_TIMEOUT = 5
DEFAULT_OUTPUT_FOLDER = './outputs'
DEFAULT_TEST_DEFINITION = './tests.json'
DEFAULT_GO_INTERPRETER = 'go'
DEFAULT_IFJCODE_INTERPRETER = './ic20int'
DEFAULT_GO_INCLUDE = './ifj20.go'
DEFAULT_TMP_FILE = './tmp'

# configuration file constants
CONFIGURATION_OUTPUT = './config.py'

# List of extensions
EXTENSIONS = ['BOOLTHEN', 'BASE', 'FUNEXP', 'MULTIVAL', 'UNARY']

# Global variables
test_index = 0
test_id = ""




# Function to parse command line arguments
def ParseArgs ():
    # Define parser
    parser = argparse.ArgumentParser(description="run tests for IFJ20 project")

    # Define arguments for mode selection
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--mode-compile-only', '-mc', action='store_true', help='compile only mode runs only compiler for each test (no interpretation and no output checking)')
    group.add_argument('--mode-interpret-only', '-mi', action='store_true', help='interpret only mode runs only compiler and interpreter for each test (no output checking)')
    group.add_argument('--mode-all', '-ma', action='store_true', help='all mode runs compiler and interpreter for each test and then checks outputs with native go language interpreter. This option is default')
    group.add_argument('--mode-list', '-ml', action='store_true', help='list mode only lists avaiable tests and test groups (no compilation, interpretation or output checking)')

    # Define argument for test selection
    parser.add_argument('--select', '-s', default='', help='list of tests or test groups that should be run. example: "test1,test2,groupA". default: All defined tests are run')

    # Define commonly used arguments
    parser.add_argument('--compiler', '-c', default=DEFAULT_COMPILER_PATH, help='path to the IFJ20 language compiler (the IFJ project executable). default: ' + DEFAULT_COMPILER_PATH)
    parser.add_argument('--extensions', '-e', default='', help='list of implemented extensions. example: "BOOLTHEN,BASE". default: No extension implemented. options: ' + ', '.join(EXTENSIONS))
    parser.add_argument('--log-file', '-l', default=DEFAULT_LOG_FILE, help='path to the log file created by the testsuite (if file already exists, it will be deleted). default: ' + DEFAULT_LOG_FILE)
    parser.add_argument('--timeout', '-t', default=DEFAULT_TIMEOUT, type=int, help='specify maximum timeout for each test in seconds (required to detect infinite run errors). defult = ' + str(DEFAULT_TIMEOUT))
    parser.add_argument('--output-folder', '-o', default=DEFAULT_OUTPUT_FOLDER, help='path to the folder where compiler output (IFJ20code language programs) is stored for every test that fails on interpretation or checking (if folder already exists, it will be deleted). default: ' + DEFAULT_OUTPUT_FOLDER)

    # Define other arguments
    parser.add_argument('--tests-definition', default=DEFAULT_TEST_DEFINITION, help='path to the tests definition json file. default: ' + DEFAULT_TEST_DEFINITION)
    parser.add_argument('--go-interpreter', default=DEFAULT_GO_INTERPRETER, help='command to execute native go interpreter for output checking. default: ' + DEFAULT_GO_INTERPRETER)
    parser.add_argument('--ifjcode-interpreter', default=DEFAULT_IFJCODE_INTERPRETER, help='command to execute IFJ20code interpreter for compiler output interpretation. default: ' + DEFAULT_IFJCODE_INTERPRETER)
    parser.add_argument('--go-include-file', default=DEFAULT_GO_INCLUDE, help='path to the file that is required to be included in go programs to execute ifj language. default: ' + DEFAULT_GO_INCLUDE)
    parser.add_argument('--tmp-file', default=DEFAULT_TMP_FILE, help='path to a temp file that will be created for each test to store compiler output for interpretation. default: ' + DEFAULT_TMP_FILE)

    # Parse arguments from command line
    args = parser.parse_args()

    # Argument postprrocessing
    if not args.mode_compile_only and not args.mode_interpret_only and not args.mode_all and not args.mode_list:
        print('setting default mode --mode-all')
        args.mode_all = True

    if args.select != '':
        print('parsing tests selection')
        args.select = args.select.split(',')
    else:
        args.select = []

    if not os.path.isfile(args.compiler):
        raise Exception('The path \'' + args.compiler + '\' is not a valid compiler executable')

    if args.extensions != '':
        print('parsing extensions')
        args.extensions = args.extensions.split(',')
        for ext in args.extensions:
            if ext not in EXTENSIONS:
                raise Exception('Invalid extension \'' + ext + '\'')
    else:
        args.extensions = []

    if os.path.isfile(args.log_file):
        print('removing old log file \'' + args.log_file + '\'')
        os.remove(args.log_file)
    if os.path.isdir(args.log_file):
        raise Exception('There is a directory with the same name as specified log file \'' + args.log_file + '\'')

    if args.timeout <= 0:
        raise Exception('Value of timeout must be greater then zero, but is \'' + str(args.timeout) + '\'')

    if os.path.isfile(args.output_folder):
        raise Exception('There is a file with the same name as specified output folder \'' + args.output_folder + '\'')
    if os.path.isdir(args.output_folder):
        print('removing old output folder \'' + args.output_folder + '\'')
        shutil.rmtree(args.output_folder)

    if not os.path.isfile(args.tests_definition):
        raise Exception('The path \'' + args.tests_definition + '\' is not a valid tests definiton file')

    print('checking go interpreter')
    output = subprocess.check_output([args.go_interpreter, 'version'])
    if output[:11] != 'go version ':
        raise Exception('Go interpreter is not valid. Command: \'' + args.go_interpreter + ' version\' didn\'t produce correct output')
    print('go interpreter found in version \'' + output[11:-1] + '\'')

    print('checking ifjcode interpreter')
    output = subprocess.check_output([args.ifjcode_interpreter])
    if output[:7] != 'BUILD: '
        raise Exception('Ifjcode interpreter is not valid. Command: \'' + args.ifjcode_interpreter + '\' didn\'t produce correct output')
    print('ifjcode interpreter found')

    if not os.path.isfile(args.go_include_file):
        raise Exception('The path \'' + args.go_include_file + '\' is not a valid go include file')

    return args

# Function to load tests definition file
def LoadTests(args):

    def RecurseGroups(root, group, processedGroups, processedTests):
        for include in group['include']:
            if include['name'] in processedGroups:
                raise Exception('Group \'' + include['name'] + '\' is included multiple times in group \'' + root + '\'')
            processedGroups.append(include['name'])
            for test in include['tests']:
                if test['name'] in processedTests:
                    raise Exception('Test \'' + test['name'] + '\' is included multiple times in group \'' + root + '\'')
                processedTests.append(test['name'])
            RecurseGroups(root, include, processed)

    def ParseError():
        raise Exception('Test definition file has bad format')

    # Parse json
    print ('parsing tests definitions')
    try:
        with open(args.tests_definition, 'r') as f:
            definition = json.load(f)
    except:
        raise Exception('Test definition file \'' + args.tests_definition + '\' is not valid json file')

    # Check validity
    names = []
    if 'tests' not in definition or 'groups' not in definition or type(definition['tests']) != list or type(definition['groups']) != list:
        ParseError()
    for test in definition['tests']:
        if type(test) != dict:
            ParseError()
        if 'name' not in test or type(test['name']) != unicode:
            ParseError()
        if test['name'] in names:
            raise Exception('Duplicate names in tests definition file')
        names.append(test['name'])
        if 'description' in test:
            if type(test['description']) != unicode:
                ParseError()
        if 'file' not in test or type(test['file']) != unicode:
            ParseError()
        if 'input' in test and type(test['input']) != unicode:
            ParseError()
        if 'compiler-codes' in test:
            if type(test['compiler-codes']) != list:
                ParseError()
            for item in test['compiler-codes']:
                if type(item) != int:
                    ParseError()
        else:
            test['compiler-codes'] = [0]
        if 'interpret-codes' in test:
            if type(test['interpret-codes']) != list:
                ParseError()
            for item in test['interpret-codes']:
                if type(item) != int:
                    ParseError()
        else:
            test['interpret-codes'] = [0]
        if 'extensions-must' in test:
            if type(test['extensions-must']) != list:
                ParseError()
            for item in test['extensions-must']:
                if type(item) != unicode or item not in EXTENSIONS:
                    ParseError()
        else:
            test['extensions-must'] = []
        if 'extensions-cant' in test:
            if type(test['extensions-cant']) != list:
                ParseError()
            for item in test['extensions-cant']:
                if type(item) != unicode or item not in EXTENSIONS:
                    ParseError()
        else:
            test['extensions-cant'] = []
    for group in definition['groups']:
        if type(group) != dict:
            ParseError
        if 'name' not in group or type(group['name']) != unicode:
            ParseError()
        if group['name'] in names:
            raise Exception('Duplicate names in tests definition file')
        names.append(group['name'])
        if 'description' in group:
            if type(group['description']) != unicode:
                ParseError()
        if 'tests' in group:
            if type(group['tests']) != list:
                ParseError()
            for item in group['tests']:
                if type(item) != unicode:
                    ParseError()
        else:
            group['tests'] = []
        if 'include' in group:
            if type(group['include']) != list:
                ParseError()
            for item in group['include']:
                if type(item) != unicode:
                    ParseError()
        else:
            group['include'] = []

    # Process groups
    print('processing group definitions')
    for group in definition['groups']:
        tests = []
        for test in group['tests']:
            found = False
            for reference in definition['tests']:
                if reference['name'] == test:
                    tests.append(reference)
                    found = True
                    break
            if not found:
                raise Exception('Test \'' + test + '\' specified in group \'' + group['name'] + '\' is not present in definition file')
        group['tests'] = tests
        groups = []
        for include in group['include']:
            found = False
            for reference in definition['groups']:
                if (reference['name'] == include):
                    groups.append(reference)
                    found = True
                    break
            if not Found:
                raise Exception('Group \'' + include + '\' included from group \'' + group['name'] + '\' is not present in definition file')
    # Check for bad dependies
    for group in definition['groups']:
        processedGroups = [group['name']]
        processedTests = []
        for test in group['tests']:
            processedTests.append(test['name'])
        RecurseGroups(group['name'], group, processedGroups, processedTests)

    # Select needed tests and groups
    print('selecting relevant tests and groups')
    if args.select != []:
        tests = []
        for test in definition['tests']:
            if test['name'] in args.select:
                tests.append(test)
        groups = []
        for group in definition['groups']:
            if group['name'] in args.select:
                groups.append(group)
    else:
        tests = definition['tests']
        groups = definition['groups']

    # Returning results
    print('\'' + str(len(tests)) + '\' tests and \'' + str(len(groups)) + '\' groups were selected')
    return tests, groups

# Printer for tests and groups
def ListTests(tests, groups):

    def GetIndent(indent):
        return ' ' * indent * 4

    def PrintGroup(group, indent):
        print(GetIndent(indent) + 'GROUP: ' + group['name'])
        indent += 1
        if 'description' in group:
            print(GetIndent(indent) + group['description'])
        PrintTests(group['tests'], indent)
        for include in group['include']:
            PrintGroup(include, indent)
        indent -= 1
        print('\n')

    def PrintTests(tests, indent):
        for test in tests:
            print(GetIndent(indent) + 'TEST: ' + test['name'])
            indent += 1
            if 'description' in test:
                print(GetIndent(indent) + test['description'])
            print(GetIndent(indent) + 'FILE: ' + test['file'])
            print(GetIndent(indent) + 'COMPILER CODES: ' + str(test['compiler-codes']))
            print(GetIndent(indent) + 'INTERPRET CODES: ' + str(test['interpret-codes']))
            if 'input' in test:
                print(GetIndent(indent) + 'INPUT: ' + test['input'])
            if test['extensions-must'] != []:
                print(GetIndent(indent) + 'EXTENSION REQUIRED: ' + str(test['extensions-must']))
            if test['extensions-cant'] != []:
                print(GetIndent(indent) + 'EXTENSION FORBIDEN: ' + str(test['extensions-cant']))
            indent -= 1
            print('')

    print('\nLIST OF TESTS AND GROUPS\n')
    PrintTests(tests, 0)
    for group in groups:
        PrintGroup(group, 0)

# Parse tests from groups, check duplicity and extensions
def ProcessTests(tests, groups, args):

    def Groups(group, tests):
        duplicated = Tests(group['tests'], tests)
        for include in group['include']:
            duplicated += Groups(include, tests)
        return duplicated

    def Tests(testList, tests):
        duplicated = 0
        for test in testList:
            duplicate = False
            for reference in tests:
                if test['name'] == reference['name']:
                    duplicate = True
                    break
            if duplicate:
                duplicated += 1
            else:
                tests.append(test)
        return duplicated

    print('preparing tests for testing configuration')
    result = []
    duplicated = Tests(tests, result)
    for group in groups:
        duplicated += Groups(group, result)
    print('there were \'' + str(duplicated) + '\' duplicated tests, each test is run only once')

    final = []
    removed = 0
    for test in result:
        valid = True
        for e in test['extensions-must']:
            if e not in args.extensions:
                valid = False
                break
        if valid:
            for e in test['extensions-cant']:
                if e in args.extensions:
                    valid = False
                    break
        if valid:
            final.append(test)
        else:
            removed += 1

    print('\'' + str(removed) + '\' tests were removed from testing due to incompatible extensions')
    print('\'' + str(len(final)) + '\' tests will be run')
    return final
"""
def GenerateConfig(args, tests):

    if os.path.isfile(CONFIGURATION_OUTPUT):
        print('removing old test configuration')
        os.remove(CONFIGURATION_OUTPUT)
    if os.path.isdir(CONFIGURATION_OUTPUT):
         raise Exception('There is a directory with the same name as output configuration file \'' + CONFIGURATION_OUTPUT + '\'')

    print('generating testing configuration')
    with open(CONFIGURATION_OUTPUT, 'w') as f:
        if args.mode_all:
            f.write('TESTING_MODE = 0\n')
        elif args.mode_interpret_only:
            f.write('TESTING_MODE = 1\n')
        elif args.mode_compile_only:
            f.write('TESTING_MODE = 2\n')
        else:
            raise Exception('BUG: invalid testing mode')

        f.write('IFJCOMP_EXECUTABLE = \'' + args.compiler + '\'\n')
        f.write('IFJ_20_TEMPLATE_FILE = \'' + args.go_include_file + '\'\n')
        f.write('TMP_FILE = \'' + args.tmp_file + '\'\n')
        f.write('GO_INTERPRETTER = \'' + args.go_interpreter + '\'\n')
        f.write('ICL_INTERPRETTER = \'' + args.ifjcode_interpreter + '\'\n')
        f.write('OUTPUT_FOLDER = \'' + args.output_folder + '\'\n')
        f.write('SINGLE_TEST_TIMEOUT = \'' + str(args.timeout) + '\'\n')

        f.write('tests = [\n')
        for test in tests:
            f.write('    (\'' + test['file'] + '\', ' + str(test['compiler-codes']) + ', ' + str(test['interpret-codes']) + ', ' + (('\'' + test['input'] + '\'') if 'input' in test else 'None') + ')\n')
        f.write(']\n')
    print('testing configuration successfully generated')
"""

# Run test on native python interpreter
def RunGo(test_source, program_input, interpret, template):
    # Execute test on native python
    cmd = [interpret, 'run', test_source, template]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    capture_out, capture_err = process.communicate(input=program_input)
    # Return info about the execution
    return {'exit_code' : process.returncode,
            'stdout' : capture_out,
            'stderr' : capture_err}

# Run test on ifj20 compiler
def RunIfjcomp(test_source, compiler):
    # Open test source
    f = open(test_source, 'rb')
    # Execute test on ifj20 compiler
    process = subprocess.Popen(compiler, stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    capture_out, capture_err = process.communicate()
    # Close test source
    f.close()
    # Return info about the execution
    return {'exit_code' : process.returncode,
            'stdout' : capture_out,
            'stderr' : capture_err}

# Run interpret with intermediate code
def RunIclint(input_data, program_input, tmp_file, interpret):
    # Save intermediate code to file
    f = open(tmp_file, 'w')
    f.write(input_data)
    f.close()
    # Execute code on interpreter
    cmd = [interpret, tmp_file]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    capture_out, capture_err = process.communicate(input=program_input)
    # Return info about the execution
    return {'exit_code' : process.returncode,
            'stdout' : capture_out,
            'stderr' : capture_err}

# Check error code from ifj20 compiler
def CheckCompilerError(process_info, error_code, log):
    # Check for correct error code
    if process_info['exit_code'] not in error_code:
	# Log error
        log.write('Compiler error output:\n' + (process_info['stderr'] or '<empty>') + '\n')
        log.write('----\n')
        error = 'Unexpected exit code of IFJ compiler. Actual: ' + str(process_info['exit_code']) + ' Expected: ' + str(error_code) + '.'
        log.write('ERROR: ' + error + '\n')
	# Fail test
        raise RuntimeError(test_id + ' - ' + error)

# Check error code from ifj20 interpreter
def CheckInterpretError(process_info, error_code, log):
    if process_info['exit_code'] not in error_code:
	# Log error
        log.write('Interpret error output:\n' + (process_info['stderr'] or '<empty>') + '\n')
        log.write('----\n')
        error = 'Unexpected exit code of IFJ interpreter. Actual: ' + str(process_info['exit_code']) + ' Expected: ' + str(error_code) + '.'
        log.write('ERROR: ' + error + '\n')
	# Fail test
        raise RuntimeError(test_id + ' - ' + error)

# Check output from native go interpreter and ifj20 interpreter
def CheckSameOutput(interpret_info, go_info, log):
    # Check if go and ifj20 have the save exit code
    if interpret_info['exit_code'] != go_info['exit_code']:
	# Log error
        log.write('Go error output:\n' + (go_info['stderr'] or '<empty>') + '\n')
        log.write('----\n')
        log.write('Interpret error output:\n' + (interpret_info["stderr"] or '<empty>') + '\n')
        log.write('----\n')
        error = 'Go and IFJ interprets have different exit codes. Go: ' + str(go_info['exit_code']) + ' IFJ: ' + str(interpret_info['exit_code']) + '.'
        log.write('ERROR: ' + error + '\n')
	# Fail test
        raise RuntimeError(test_id + ' - ' + error)

    # Check standart output of go and ifj20
    if interpret_info['stdout'] != python_info['stdout']:
	# Log error
        log.write('Python error output:\n' + (python_info['stderr'] or '<empty>') + '\n')
        log.write('----\n')
        log.write('Interpret error output:\n' + (interpret_info['stderr'] or '<empty>') + '\n')
        log.write('----\n')
        log.write('Python output:\n' + (python_info['stdout'] or '<empty>') + '\n')
        log.write('----\n')
        log.write('Interpret output:\n' + (interpret_info['stdout'] or '<empty>') + '\n')
        log.write('----\n')
        error = 'Python and IFJ interprets have different outputs.'
        log.write('ERROR: ' + error + '\n')
	# Fail test
        raise RuntimeError(test_id + ' - ' + error)

def RunTest(test, args, log):
    # Global variables must be accessed here
    global test_index
    global test_id
    test_index = test_index + 1
    test_id = test['file']
    # Log current test
    log.write('\n********************\nTEST ' + str(test_index) + ': ' + test_id + '\n********************\n\n')
    if 'input' in test:
        log.write('PROGRAM INPUT:\n')
        log.write(test['input'] + '\n')
        log.write('----\n')
    # Run ifj20 compiler
    compiler_info = RunIfjcomp(test['file'], args.compiler)
    # Check compiler for error
    CheckCompilerError(compiler_info, test['compiler-codes'], log)
    # End execution if tests are compile only
    if args.mode_compile_only or (compiler_info['exit_code'] != 0):
        if args.mode_compile_only and (compiler_info['exit_code'] == 0):
	    # Log warning about incomplete testing
            log.write('WARNING: This test was not entirely completed, because of the MODE_COMPILE testing mode.\n')
            log.write('         Interpretation and output checks were not run.\n')
            log.write('----\n')
        log.write('SUCCESS\n')
        return

    # If this part fails, the intermedate code must be saved for further analysis
    try:
	# Run ifj20 interpret
        interpret_info = RunIclint(compiler_info['stdout'], test['input'] or None, args.tmp_file, args.ifj_interpreter)
	# Check interpret for error
        CheckInterpretError(interpret_info, test['interpret-codes'], log)
	# End execution if tests are compile and interpret only
        if args.mode_interpret_only or (interpret_info['exit_code'] != 0):
            if args.mode_interpret_only and (interpret_info['exit_code'] == 0):
		# Log warning about incomplete testing
                log.write('WARNING: This test was not entirely completed, because of the MODE_INTERPRET testing mode.\n')
                log.write('         Output checks were not run.\n')
                log.write('----\n')
            log.write('SUCCESS\n')
            return

	# Run test on native go interpreter and compare results with ifj20 interpreter
        go_info = RunGo(test['file'], test['input'] or None, args.go_interpret, args.go_include_file)
        CheckSameOutput(interpret_info, python_info, log)
    except:
	# Save intermetiate code
        f = open(args.output_folder + '/' + test['file'] + '.ifj20code', 'w')
        f.write(compiler_info['stdout'])
        f.close()
        raise

    # Test successfull
    log.write('SUCCESS\n')



# Main program

args = ParseArgs()
tests, groups = LoadTests(args)
if args.mode_list:
    ListTests(tests, groups)
else:
    tests = ProcessTests(tests, groups, args)
    #GenerateConfig(args, tests)
    with open(args.log_file, 'w') as log:
        for test in tests:
            RunTest(test, args, log)
"""
            try:
                RunTest(test, args, log)
            except Exception as error:
                log.write('FAIL: ' + error + '\n')
"""
