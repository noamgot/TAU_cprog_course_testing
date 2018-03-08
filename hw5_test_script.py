from my_utils import *


def run_tests_on_solution5(ex, num_of_questions, tests_per_question_lst):
    for i in range(num_of_questions):
        num_of_tests = tests_per_question_lst[i]
        exe_path = os.path.join(SOLUTION_DIR_NAME, ex + "_q" + str(i + 1) + "_sol.exe")
        for j in range(num_of_tests):
            books = os.path.join(INPUT_DIR_NAME, "books{}.txt".format(j + 1))
            orders = os.path.join(INPUT_DIR_NAME, "orders{}.txt".format(j + 1))
            upd_books = os.path.join(SOLUTION_DIR_NAME, "updated_books{}.txt".format(j + 1))
            cmd_args = [exe_path, books, orders, upd_books]
            rc = run_command(cmd_args, cmd_timout=10)
            assert rc != -123, "Unexpected solution timeout!!!"  # timeout!
            assert rc != -1, "Unexpected solution runtime error!!!"  # runtime error!


def arrange_files(path, students_lst):
    _, _, filenames = next(os.walk("submissions"))
    for curr_file in filenames:
        student_id_sig = curr_file[4:-2]  # remove "ex4_" prefix and ".c" suffix
        student_id1, student_id2 = get_student_ids(student_id_sig)

        curr_student1 = find_student(students_lst, student_id1)
        if curr_student1 is None:
            raise ValueError("No student was found with id - {}".format(student_id1))
        curr_student2 = find_student(students_lst, student_id2)

        curr_student1.no_submission = None  # student submitted...
        if student_id2 is not None:
            curr_student2.no_submission = None  # student submitted...

        dir_to_copy = os.path.join(path, student_id_sig)
        make_dir(dir_to_copy)
        shutil.copy2(os.path.join(SUBMISSIONS_DIR_NAME, curr_file), dir_to_copy)


def get_student_ids(dir_name):
    if "_" in dir_name:  # 2 students
        students = dir_name.split("_")
        id1 = students[0]
        id2 = students[1]
    else:
        id1 = dir_name
        id2 = None
    return id1, id2


def compile_and_run_question5(path, ex, student_id_sig, question_num, num_of_tests, student1, student2=None):
    """question_num should be passed 0-based, i.e - question 1 will be passed as 0, etc. """
    c_path = os.path.join(path, student_id_sig, ex + "_" + student_id_sig + ".c")
    # check if .c file exists
    if not os.path.isfile(c_path):
        student1.set_bad_c_file_err(question_num)
        FatalErrorsLists.bad_c_file_name[question_num].append(student_id_sig)
        if student2 is not None:
            student2.set_bad_c_file_err(question_num)
        return

    os.system("compile_single_file.bat " + ex + " " + student_id_sig + " " + c_path)
    exe_path = c_path[:-2] + ".exe"
    if os.path.isfile(exe_path):
        # the compilation succeeded - run tests!
        for i in range(num_of_tests):
            books = os.path.join(INPUT_DIR_NAME, "books{}.txt".format(i + 1))
            orders = os.path.join(INPUT_DIR_NAME, "orders{}.txt".format(i + 1))
            upd_books = os.path.join(path, student_id_sig, "updated_books{}_{}.txt".format(i + 1, student_id_sig))
            cmd_args = [exe_path, books, orders, upd_books]
            # mem_log_path = os.path.join(path, student_id_sig)
            # cmd = "drmemory -quiet -batch -logdir " + mem_log_path + " -- " + exe_path
            rc = run_command(cmd_args, cmd_timout=10)
            if rc == -123:  # timeout!
                FatalErrorsLists.test_timeout[question_num][i].append(student_id_sig)
            elif rc == -1:  # runtime error!
                FatalErrorsLists.test_runtime_error[question_num][i].append(student_id_sig)

    else:  # exe file does not exists - compilation error
        student1.set_compilation_err(question_num)
        FatalErrorsLists.compilation_error[question_num].append(student_id_sig)
        if student2 is not None:
            student2.set_compilation_err(question_num)


def compile_and_run_all_tests5(path, ex, student_id_sig, num_of_questions, tests_per_question_lst, student1,
                               student2=None):
    for i in range(num_of_questions):
        num_of_tests = tests_per_question_lst[i]
        compile_and_run_question5(path, ex, student_id_sig, i, num_of_tests, student1, student2)


if __name__ == "__main__":
    # validate input
    args = parse_input()

    ex = "ex" + str(args.ex)
    num_of_questions = args.qs
    tests_per_question_lst = args.tests_per_question
    EXERCISE_PATH = os.path.join(EXERCISE_PATH, ex)

    run_tests_on_solution5(ex, num_of_questions, tests_per_question_lst)

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

    # arrange files
    arrange_files(EXERCISE_PATH, students_lst)

    # update the no-submission list in the FatalErrorsLists class
    update_no_submission_lst(students_lst)

    # compile and run all possible exe files:
    _, dirnames, _ = next(os.walk(EXERCISE_PATH))
    for dir in dirnames:
        if dir != "bad":
            student_id1, student_id2 = get_student_ids(dir)
            curr_student1 = find_student(students_lst, student_id1)
            curr_student2 = find_student(students_lst, student_id2)
            student_id_sig = dir

            compile_and_run_all_tests5(EXERCISE_PATH, ex, student_id_sig, num_of_questions, tests_per_question_lst,
                                       curr_student1, curr_student2)

            # test results
            for i in range(num_of_questions):
                for j in range(tests_per_question_lst[i]):
                    student_res_file_name = os.path.join(EXERCISE_PATH, dir,
                                                         "updated_books{}_{}.txt".format(j + 1, student_id_sig))
                    sol_file_name = os.path.join(SOLUTION_DIR_NAME, "updated_books{}.txt".format(j + 1))
                    # compare files only if the result file exists
                    if os.path.isfile(student_res_file_name):
                        if not files_are_identical(student_res_file_name, sol_file_name):
                            curr_student1.set_wrong_output_err(i, j)
                            if curr_student2 is not None:
                                curr_student2.set_wrong_output_err(i, j)
            # memory test


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
        # qi = "Q" + str(i + 1)
        csv_cols += ["bad .c file name", "compilation error"]
        for j in range(tests_per_question_lst[i]):
            csv_cols += ["Test " + str(j + 1)]

    write_grades_to_CSV(csv_cols, students_lst)

    # print errors and IDs:
    print_fatal_errors(num_of_questions, tests_per_question_lst)
