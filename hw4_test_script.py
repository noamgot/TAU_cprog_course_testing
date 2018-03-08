from my_utils import *

# class Student3(Student):
#     def set_grade(self, question_num, test_num, grade):
#         self.questions[question_num].tests[test_num] = str(grade)


def arrange_files(path, students_lst):
    _, _, filenames = next(os.walk("submissions"))
    for curr_file in filenames:
        student_id_sig = curr_file[4:-2] # remove "ex4_" prefix and ".c" suffix
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
        shutil.copy2(os.path.join(SUBMISSIONS_DIR_NAME, curr_file),dir_to_copy)



def get_student_ids(dir_name):
    if "_" in dir_name: # 2 students
        students = dir_name.split("_")
        id1 = students[0]
        id2 = students[1]
    else:
        id1 = dir_name
        id2 = None
    return id1, id2


def compile_and_run_question4(path, ex, student_id_sig, question_num, num_of_tests, student1, student2=None):
    """question_num should be passed 0-based, i.e - question 1 will be passed as 0, etc. """
    c_path = os.path.join(path, student_id_sig, ex + "_" + student_id_sig + ".c")
    # check if .c file exists
    if not os.path.isfile(c_path):
        student1.set_bad_c_file_err(question_num)
        FatalErrorsLists.bad_c_file_name[question_num].append(student_id_sig)
        if student2 is not None:
            student2.set_bad_c_file_err(question_num)
        return

    os.system("compile_single_file_ex4.bat " + ex + " " + student_id_sig + " " + c_path)
    exe_path = c_path[:-2] + ".exe"
    if os.path.isfile(exe_path):
        # the compilation succeeded - run tests!
        for i in range(num_of_tests):
            ex_qt_identifier = ex + "_q" + str(question_num + 1) + "t" + str(i + 1)
            input_file = open(os.path.join(INPUT_DIR_NAME, ex_qt_identifier + "_input.txt"), "r")
            res_file = open(os.path.join(path, student_id_sig, ex_qt_identifier + "_" + student_id_sig + ".txt"), "w")
            mem_log_path = os.path.join(path, student_id_sig)
            cmd = "drmemory -quiet -batch -logdir " + mem_log_path + " -- " + exe_path
            rc = run_command(cmd, input_file, res_file)
            if rc == -123:  # timeout!
                FatalErrorsLists.test_timeout[question_num][i].append(student_id_sig)
            elif rc == -1: # runtime error!
                FatalErrorsLists.test_runtime_error[question_num][i].append(student_id_sig)
            input_file.close()
            res_file.close()
    else:  # exe file does not exists - compilation error
        student1.set_compilation_err(question_num)
        FatalErrorsLists.compilation_error[question_num].append(student_id_sig)
        if student2 is not None:
            student2.set_compilation_err(question_num)


def compile_and_run_all_tests4(path, ex, student_id_sig, num_of_questions, tests_per_question_lst, student1, student2=None):
    for i in range(num_of_questions):
        num_of_tests = tests_per_question_lst[i]
        compile_and_run_question4(path, ex, student_id_sig, i, num_of_tests, student1, student2)

if __name__ == "__main__":
    # validate input
    args = parse_input()

    ex = "ex" + str(args.ex)
    num_of_questions = args.qs
    tests_per_question_lst = args.tests_per_question
    EXERCISE_PATH = os.path.join(EXERCISE_PATH, ex)

    run_tests_on_solution(ex, num_of_questions, tests_per_question_lst)

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

            compile_and_run_all_tests4(EXERCISE_PATH, ex, student_id_sig, num_of_questions, tests_per_question_lst, curr_student1, curr_student2)

            # test results
            for i in range(num_of_questions):
                for j in range(tests_per_question_lst[i]):
                    ex_qt_identifier = ex + "_q" + str(i + 1) + "t" + str(j + 1)
                    student_res_file_name = os.path.join(EXERCISE_PATH, dir,
                                                         ex_qt_identifier + "_" + student_id_sig + ".txt")
                    sol_file_name = os.path.join(SOLUTION_DIR_NAME, ex_qt_identifier + "_sol.txt")
                    # compare files only if the result file exists
                    if os.path.isfile(student_res_file_name):
                        if not files_are_identical(student_res_file_name, sol_file_name):  # , diff1_path):
                            curr_student1.set_wrong_output_err(i, j)
                            if curr_student2 is not None:
                                curr_student2.set_wrong_output_err(i, j)


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
        #qi = "Q" + str(i + 1)
        csv_cols += ["bad .c file name", "compilation error"]
        for j in range(tests_per_question_lst[i]):
            csv_cols += ["Test " + str(j + 1)]

    write_grades_to_CSV(csv_cols, students_lst)

    # print errors and IDs:
    print_fatal_errors(num_of_questions, tests_per_question_lst)

