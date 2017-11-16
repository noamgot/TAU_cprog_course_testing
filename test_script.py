from my_utils import *

if __name__ == "__main__":
    # validate input
    n = validate_input()

    EX = "ex" + str(n)
    EXERCISE_PATH = "C:/Users/noamg/Desktop/C_exercises/{}".format(EX)

    # todo - put it where it should be....
    num_of_questions = 2
    tests_per_question_lst = [2, 3]

    # create a directory for the exercise
    make_dir(EXERCISE_PATH)

    # create students list
    students_lst = get_students_list('students.txt', num_of_questions, tests_per_question_lst)

    too_many_files = []
    not_zip = []
    bad_zip_name = []
    q1_bad_c_name = []
    q1_comp_err = []
    q2_bad_c_name = []
    q2_comp_err = []

    # extract zip files
    extract_zip_files(EXERCISE_PATH, EX, too_many_files, not_zip, bad_zip_name, students_lst)

    # compile files
    # os.system("compile.bat " + EX)

    # run all possible exe files:
    _, dirnames, _ = next(os.walk(EXERCISE_PATH))
    for dir in dirnames:
        if dir != "bad":
            id = dir
            current_student = find_student(students_lst, id)
            compile_and_run_question(EXERCISE_PATH, dir, EX, id, 1, q1_bad_c_name, q1_comp_err, current_student)
            compile_and_run_question(EXERCISE_PATH, dir, EX, id, 2, q2_bad_c_name, q2_comp_err, current_student)
            # run_exe_files(EXERCISE_PATH, dir, EX, id, str(1), q1_bad_c_name, q1_comp_err)
            # run_exe_files(EXERCISE_PATH, dir, EX, id, str(2), q2_bad_c_name, q2_comp_err)

            # test results
            student_res_q1 = os.path.join(EXERCISE_PATH, dir, EX + "_q" + str(1) + "_" + id + ".txt")
            student_res_q2 = os.path.join(EXERCISE_PATH, dir, EX + "_q" + str(2) + "_" + id + ".txt")
            q1_sol = 'ex0q1sol.txt'
            q2_sol = 'ex0q2sol.txt'
            diff1_path = os.path.join(EXERCISE_PATH, dir, EX + "_q" + str(1) + "_" + id + "_DIFF.txt")
            diff2_path = os.path.join(EXERCISE_PATH, dir, EX + "_q" + str(2) + "_" + id + "_DIFF.txt")
            if not os.path.isfile(student_res_q1) or not filesAreIdentical(student_res_q1, q1_sol, diff1_path):
                current_student.q1_wrong_output_err = X
            if not os.path.isfile(student_res_q2) or not filesAreIdentical(student_res_q2, q2_sol, diff2_path):
                current_student.q2_wrong_output_err = X

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
