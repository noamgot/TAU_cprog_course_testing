from my_utils import *

if __name__ == "__main__":
    # validate input
    n = validate_input()

    EX = "ex" + str(n)
    EXERCISE_PATH = "C:/Users/noamg/Desktop/C_exercises/{}".format(EX)
    SOLUTION_DIR_NAME = "solutions"

    # todo - put it where it should be....
    num_of_questions = 3
    tests_per_question_lst = [2, 3, 4]

    FatalErrorsLists.bad_c_file_name = [[] for i in range(num_of_questions)]
    FatalErrorsLists.compilation_error = [[] for i in range(num_of_questions)]
    FatalErrorsLists.test_timeout = [
        [
            [] for j in range(tests_per_question_lst[i])
        ] for i in range(num_of_questions)
    ]

    # create a directory for the exercise
    make_dir(EXERCISE_PATH)

    # create students list
    students_lst = init_students_list('students.txt', num_of_questions, tests_per_question_lst)

    # extract zip files
    extract_zip_files(EXERCISE_PATH, EX, students_lst)

    # update the no-submission list in the FatalErrorsLists class
    update_no_submission_lst(students_lst)

    # compile and run all possible exe files:
    _, dirnames, _ = next(os.walk(EXERCISE_PATH))
    for dir in dirnames:
        if dir != "bad":
            student_id = dir
            current_student = find_student(students_lst, student_id)
            compile_and_run_all_tests(EXERCISE_PATH, EX, student_id, num_of_questions, tests_per_question_lst,
                                      current_student)

            # compile_and_run_question(EXERCISE_PATH, dir, EX, student_id, 1, q1_bad_c_name, q1_comp_err, current_student)
            # compile_and_run_question(EXERCISE_PATH, dir, EX, student_id, 2, q2_bad_c_name, q2_comp_err, current_student)
            # run_exe_files(EXERCISE_PATH, dir, EX, id, str(1), q1_bad_c_name, q1_comp_err)
            # run_exe_files(EXERCISE_PATH, dir, EX, id, str(2), q2_bad_c_name, q2_comp_err)

            # test results
            # all_results_file_names = [
            #     [
            #         [
            #             os.path.join(EXERCISE_PATH, dir,
            #                          EX + "_q" + str(i + 1) + "t" + str(j + 1) + "_" + student_id + ".txt")
            #         ] for j in range(tests_per_question_lst[i])
            #     ] for i in range(num_of_questions)
            # ]
            # all_sols_file_names = [
            #     [
            #         [
            #             os.path.join(SOLUTION_DIR_NAME, EX + "_q" + str(i + 1) + "t" + str(j + 1) + "_sol.txt")
            #         ] for j in range(tests_per_question_lst[i])
            #     ] for i in range(num_of_questions)
            # ]
            # for i in range(num_of_questions):
            #     for j in range(tests_per_question_lst[i]):
            #         all_results_file_names[i][j] = os.path.join(EXERCISE_PATH, dir, EX + "_q" + str(i+1) + "t" + str(j+1) + "_" + student_id + ".txt")
            #         all_sols_file_names[i][j] = os.path.join(SOLUTION_DIR_NAME,  EX + "_q" + str(i+1) + "t" + str(j+1) + "_sol.txt")

            # test results
            for i in range(num_of_questions):
                for j in range(tests_per_question_lst[i]):
                    ex_qt_identifier = EX + "_q" + str(i + 1) + "t" + str(j + 1)
                    student_res_file_name = os.path.join(EXERCISE_PATH, dir,
                                                         ex_qt_identifier + "_" + student_id + ".txt")
                    sol_file_name = os.path.join(SOLUTION_DIR_NAME, ex_qt_identifier + "_sol.txt")
                    # compare files only if the result file exists
                    if os.path.isfile(student_res_file_name):
                        if not filesAreIdentical(student_res_file_name, sol_file_name):  # , diff1_path):
                            current_student.set_wrong_output_err(i, j)

                    # student_res_q1 = os.path.join(EXERCISE_PATH, dir, EX + "_q" + str(1) + "_" + student_id + ".txt")
                    # student_res_q2 = os.path.join(EXERCISE_PATH, dir, EX + "_q" + str(2) + "_" + student_id + ".txt")
                    # q1_sol = 'ex0q1sol.txt'
                    # q2_sol = 'ex0q2sol.txt'
                    # diff1_path = os.path.join(EXERCISE_PATH, dir, EX + "_q" + str(1) + "_" + student_id + "_DIFF.txt")
                    # diff2_path = os.path.join(EXERCISE_PATH, dir, EX + "_q" + str(2) + "_" + student_id + "_DIFF.txt")
                    # if not os.path.isfile(student_res_q1) or not filesAreIdentical(student_res_q1, q1_sol):  # , diff1_path):
                    #     current_student.q1_wrong_output_err = X
                    # if not os.path.isfile(student_res_q2) or not filesAreIdentical(student_res_q2, q2_sol):  # , diff2_path):
                    #     current_student.q2_wrong_output_err = X

    csv_cols = [
        "ID",
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
            csv_cols += [qi + " - Test " + str(j + 1) + ": Wrong output"]

    write_grades_to_CSV(csv_cols, students_lst)

    # # print results
    # print("*** too many files ***")
    # print_bads(too_many_files)
    #
    # print("*** not a zip file ***")
    # print_bads(not_zip)
    #
    # print("*** bad zip file name ***")
    # print_bads(bad_zip_name)
    #
    # print("*** bad q1 c file name ***")
    # print_bads(q1_bad_c_name)
    #
    # print("*** q1 compilation error ***")
    # print_bads(q1_comp_err)
    #
    # print("*** bad q2 c file name ***")
    # print_bads(q2_bad_c_name)
    #
    # print("*** q2 compilation error ***")
    # print_bads(q2_comp_err)
