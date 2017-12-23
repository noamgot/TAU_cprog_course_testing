from my_utils import *
import mmap

bad_ret_code = []
sol_ret_code = []


# giving a very generous default timout of 15 seconds
def run_command2(cmd, cmd_stdin=None, cmd_stdout=None, cmd_timeout=15):
    try:
        rc = subprocess.run(cmd, timeout=cmd_timeout, stdin=cmd_stdin, stdout=cmd_stdout)
        return rc.returncode
    except subprocess.TimeoutExpired:
        return -123
    except subprocess.CalledProcessError as exc:
        print('error: code={}, out="{}"'.format(exc.returncode, exc.output, ))
        return -1


def compile_and_run_question2(path, ex, student_id, question_num, num_of_tests, student):
    """question_num should be passed 0-based, i.e - question 1 will be passed as 0, etc. """
    c_path = os.path.join(path, student_id, ex + "_" + student_id + ".c")
    # check if .c file exists
    if not os.path.isfile(c_path):
        student.set_bad_c_file_err(question_num)
        FatalErrorsLists.bad_c_file_name[question_num].append(student_id)
        return

    os.system("compile_single_file.bat " + ex + " " + student_id + " " + c_path)
    exe_path = c_path[:-2] + ".exe"
    if os.path.isfile(exe_path):
        # the compilation succeeded - run tests!
        for i in range(num_of_tests):
            ex_qt_identifier = ex + "_q" + str(question_num + 1) + "t" + str(i + 1)
            input_file = open(os.path.join(INPUT_DIR_NAME, ex_qt_identifier + "_input.txt"), "r")
            res_file = open(os.path.join(path, student_id, ex_qt_identifier + "_" + student_id + ".txt"), "w")
            rc = run_command2(exe_path, input_file, res_file)
            if rc == -123:  # timeout!
                FatalErrorsLists.test_timeout[question_num][i].append(student_id)
            elif rc == -1:
                FatalErrorsLists.test_runtime_error[question_num][i].append(student_id)
            elif rc != sol_ret_code[question_num][i]:
                bad_ret_code[question_num].add(student_id)
            input_file.close()
            res_file.close()
    else:  # exe does not exists - compilation error
        student.set_compilation_err(question_num)
        FatalErrorsLists.compilation_error[question_num].append(student_id)


def compile_and_run_all_tests2(path, ex, student_id, num_of_questions, tests_per_question_lst, student):
    for i in range(num_of_questions):
        num_of_tests = tests_per_question_lst[i]
        compile_and_run_question2(path, ex, student_id, i, num_of_tests, student)


def check_if_used_math_lib(path, ex, student_id, used_math_lib):
    c_path = os.path.join(path, student_id, ex + "_" + student_id + ".c")
    try:
        with open(c_path, 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(b"<math.h>") != -1:
                used_math_lib.append(student_id)
    except (FileNotFoundError, PermissionError):
        pass


def run_tests_on_solution2(ex, num_of_questions, tests_per_question_lst):
    for i in range(num_of_questions):
        num_of_tests = tests_per_question_lst[i]
        exe_path = os.path.join(SOLUTION_DIR_NAME, ex + "_sol.exe")
        for j in range(num_of_tests):
            ex_qt_identifier = ex + "_q" + str(i + 1) + "t" + str(j + 1)
            input_file = open(os.path.join(INPUT_DIR_NAME, ex_qt_identifier + "_input.txt"), "r")
            res_file = open(os.path.join(SOLUTION_DIR_NAME, ex_qt_identifier + "_sol.txt"), "w")
            rc = run_command2(exe_path, input_file, res_file)
            assert rc != -123, "Unexpected solution timeout!!!"  # timeout!
            input_file.close()
            res_file.close()
            sol_ret_code[i].append(rc)


if __name__ == "__main__":

    # validate input
    args = parse_input()

    ex = "ex" + str(args.ex)
    num_of_questions = args.qs
    tests_per_question_lst = args.tests_per_question

    bad_ret_code = [set() for i in range(num_of_questions)]
    sol_ret_code = [[] for i in range(num_of_questions)]

    EXERCISE_PATH = os.path.join(EXERCISE_PATH, ex)

    run_tests_on_solution2(ex, num_of_questions, tests_per_question_lst)

    used_math_lib = []
    FatalErrorsLists.bad_c_file_name = [[] for i in range(num_of_questions)]
    FatalErrorsLists.compilation_error = [[] for i in range(num_of_questions)]
    FatalErrorsLists.test_timeout = [
        [
            [] for j in range(tests_per_question_lst[i])
        ] for i in range(num_of_questions)
    ]

    FatalErrorsLists.test_runtime_error = [
        [
            [] for j in range(tests_per_question_lst[i])
        ] for i in range(num_of_questions)
    ]

    # create a directory for the exercise
    make_dir(EXERCISE_PATH)

    # create students list
    students_lst = init_students_list('students.txt', num_of_questions, tests_per_question_lst)

    # extract zip files
    extract_zip_files(EXERCISE_PATH, ex, students_lst)

    # update the no-submission list in the FatalErrorsLists class
    update_no_submission_lst(students_lst)

    # compile and run all possible exe files:
    _, dirnames, _ = next(os.walk(EXERCISE_PATH))
    for dir in dirnames:
        if dir != "bad":
            student_id = dir
            current_student = find_student(students_lst, student_id)
            compile_and_run_all_tests2(EXERCISE_PATH, ex, student_id, num_of_questions, tests_per_question_lst,
                                       current_student)

            check_if_used_math_lib(EXERCISE_PATH, ex, student_id, used_math_lib)
            # test results
            for i in range(num_of_questions):
                for j in range(tests_per_question_lst[i]):
                    ex_qt_identifier = ex + "_q" + str(i + 1) + "t" + str(j + 1)
                    student_res_file_name = os.path.join(EXERCISE_PATH, dir,
                                                         ex_qt_identifier + "_" + student_id + ".txt")
                    sol_file_name = os.path.join(SOLUTION_DIR_NAME, ex_qt_identifier + "_sol.txt")
                    # compare files only if the result file exists
                    if os.path.isfile(student_res_file_name):
                        if not files_are_identical(student_res_file_name, sol_file_name):  # , diff1_path):
                            current_student.set_wrong_output_err(i, j)

    csv_cols = [
        "Student ID",
        # general errors
        "No submission",
        "Too many files",
        "Bad zip file name",
        "No zip file",
    ]

    # individual question erros
    for i in range(num_of_questions):
        qi = "Q" + str(i + 1)
        csv_cols += [qi + " - bad .c file name", qi + " - compilation error"]
        for j in range(tests_per_question_lst[i]):
            csv_cols += [qi + ", Test " + str(j + 1) + " - Wrong output"]

    write_grades_to_CSV(csv_cols, students_lst)

    # print errors and IDs:
    print_fatal_errors(num_of_questions, tests_per_question_lst)
    print_bads(used_math_lib, "Used math.h library")
    print_bads(list(bad_ret_code[0]), "Q1 bad return code")
    print_bads(list(bad_ret_code[1]), "Q2 bad return code")
