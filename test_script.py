from my_utils import *

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

    # extract zip files
    extract_zip_files(EXERCISE_PATH, ex, students_lst)

    # update the no-submission list in the FatalErrorsLists class
    update_no_submission_lst(students_lst)

    # compile and run all possible exe files:
    _, dir_names, _ = next(os.walk(EXERCISE_PATH))
    for dir_name in dir_names:
        if dir_name != "bad":
            student_id = dir_name
            current_student = find_student(students_lst, student_id)
            compile_and_run_all_tests(EXERCISE_PATH, ex, student_id, num_of_questions, tests_per_question_lst,
                                      current_student)
            # test results
            for i in range(num_of_questions):
                for j in range(tests_per_question_lst[i]):
                    ex_qt_identifier = ex + "_q" + str(i + 1) + "t" + str(j + 1)
                    student_res_file_name = os.path.join(EXERCISE_PATH, dir_name,
                                                         ex_qt_identifier + "_" + student_id + ".txt")
                    sol_file_name = os.path.join(SOLUTION_DIR_NAME, ex_qt_identifier + "_sol.txt")
                    # compare files only if the result file exists
                    if os.path.isfile(student_res_file_name):
                        if not files_are_identical(student_res_file_name, sol_file_name):  # , diff1_path):
                            current_student.set_wrong_output_err(i, j)
                    else: # no result file
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

