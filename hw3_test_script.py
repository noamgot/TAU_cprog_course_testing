from my_utils import *
import mmap

class Student3(Student):
    def set_grade(self, question_num, test_num, grade):
        self.questions[question_num].tests[test_num] = str(grade)


def extract_zip_files3(path, students_lst):
    _, _, filenames = next(os.walk("submissions"))
    for curr_file in filenames:
        curr_id = curr_file.split("_file_", 1)[1][:9]
        # find current student
        curr_student = find_student(students_lst, curr_id)
        if curr_student is None:
            raise ValueError("No student was found with id - {}".format(curr_id))
        curr_student.no_submission = None  # student submitted...

        if curr_file.endswith(".zip"):
            zip_file = os.path.join(os.getcwd(), "submissions", curr_file)
            dir_to_extract = os.path.join(path, curr_id)
            make_dir(dir_to_extract)
            zip_ref = zipfile.ZipFile(zip_file, 'r')
            zip_ref.extractall(dir_to_extract)
            zip_ref.close()
        else: # no zip file
            not_zip_dir = os.path.join(path, "bad")
            make_dir(not_zip_dir)
            shutil.copy(os.path.join(os.getcwd(), "submissions", curr_file), os.path.join(not_zip_dir))
            curr_student.no_zip_file = X
            FatalErrorsLists.no_zip_file.append(curr_id)

def init_students_list3(students_file_path, num_of_questions, tests_per_question_lst):
    students_lst = []
    students_file = open(students_file_path)
    for line in students_file:
        student_id = line.rstrip()
        students_lst.append(Student3(student_id, num_of_questions, tests_per_question_lst))
    # students_lst = [Student(student_id.rstrip('\n'), num_of_questions, tests_per_question_lst) for student_id in students_file]
    students_file.close()
    return students_lst


header_file_name = "test_data.h"


def get_test_grade(test_path, sol_path):  # , diffpath):
    # result = True
    # diff_file = open(diffpath, 'w')
    with open(test_path, 'r') as test_file, open(sol_path, 'r') as sol_file:
        test_lines = ["".join(line.lower().split()) for line in test_file.readlines()]
        sol_lines = ["".join(line.lower().split()) for line in sol_file.readlines()]
        if len(sol_lines) != len(test_lines):
            return 0
        grade = len(sol_lines)-1  # number of lines printed minus the first one which is always the same
        for i in range(1,len(sol_lines)):
            if test_lines[i] != sol_lines[i]:
                grade -= 1
        return 100.0 * grade / (len(sol_lines)-1)  # return test grade 100-based


def compile_and_run_test3(path, ex, student_id, test_num, student):
    """question_num should be passed 0-based, i.e - question 1 will be passed as 0, etc. """
    c_path = os.path.join(path, student_id, ex + "_" + student_id + ".c")
    # check if .c file exists
    if not os.path.isfile(c_path):
        student.set_bad_c_file_err(test_num)
        FatalErrorsLists.bad_c_file_name[test_num].append(student_id)
        return
    # copy relevant .h file
    header_file_to_copy = os.path.join(INPUT_DIR_NAME, "test_data" + str(test_num + 1) + ".h")
    shutil.copy2(header_file_to_copy, os.path.join(path, student_id, header_file_name))

    os.system("compile_single_file.bat " + ex + " " + student_id + " " + c_path)
    exe_path = c_path[:-2] + ".exe"
    if os.path.isfile(exe_path):
        # the compilation succeeded - run tests!
        for i in range(3):  # 3 questions
            ex_qt_identifier = ex + "_q" + str(i + 1) + "t" + str(test_num + 1)
            # input_file = open(os.path.join(INPUT_DIR_NAME, ex_qt_identifier + "_input.txt"), "r")
            res_file = open(os.path.join(path, student_id, ex_qt_identifier + "_" + student_id + ".txt"), "w")
            cmd = "(echo {}) | ".format(str(i + 1)) + exe_path
            rc = run_command(cmd, cmd_stdout=res_file)
            if rc == -123:  # timeout!
                FatalErrorsLists.test_timeout[i][test_num].append(student_id)
            elif rc == -1:
                FatalErrorsLists.test_runtime_error[i][test_num].append(student_id)
            res_file.close()
    else:  # exe does not exists - compilation error
        student.set_compilation_err(test_num)  # todo - handle this
        FatalErrorsLists.compilation_error[test_num].append(student_id)


def compile_and_run_all_tests3(path, ex, student_id, student):
    for i in range(2):  # 2 tests
        compile_and_run_test3(path, ex, student_id, i, student)


def check_if_used_stdlib(path, ex, student_id, used_math_lib):
    c_path = os.path.join(path, student_id, ex + "_" + student_id + ".c")
    try:
        with open(c_path, 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(b"<stdlib.h>") != -1:
                used_math_lib.append(student_id)
    except (FileNotFoundError, PermissionError):
        pass


def run_tests_on_solution3(ex):
    for j in range(2):  # 2 tests (h files)
        exe_path = os.path.join(SOLUTION_DIR_NAME, ex + "_t" + str(j + 1) + "_sol.exe")
        # header_file_to_copy = os.path.join(INPUT_DIR_NAME, "test_data" + str(j+1) + ".h")
        # shutil.copy2(header_file_to_copy, os.path.join(header_file_path)
        for i in range(3):  # 3 questions
            ex_qt_identifier = ex + "_q" + str(i + 1) + "t" + str(j + 1)
            # input_file = open(os.path.join(INPUT_DIR_NAME, ex_qt_identifier + "_input.txt"), "r")
            res_file = open(os.path.join(SOLUTION_DIR_NAME, ex_qt_identifier + "_sol.txt"), "w")
            cmd = "(echo {}) | ".format(str(i + 1)) + exe_path
            rc = run_command(cmd, cmd_stdout=res_file)
            assert rc != -123, "Unexpected solution timeout!!!"  # timeout!
            assert rc != -1, "Unexpected runtime error!!!"  # runtime error!
            res_file.close()


if __name__ == "__main__":

    # validate input
    args = parse_input()

    ex = "ex" + str(args.ex)
    num_of_questions = args.qs
    tests_per_question_lst = args.tests_per_question
    EXERCISE_PATH = os.path.join(EXERCISE_PATH, ex)

    run_tests_on_solution3(ex)

    used_stdlib = []
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
    students_lst = init_students_list3('students.txt', num_of_questions, tests_per_question_lst)

    # extract zip files
    extract_zip_files3(EXERCISE_PATH, students_lst)

    # update the no-submission list in the FatalErrorsLists class
    update_no_submission_lst(students_lst)

    # compile and run all possible exe files:
    _, dirnames, _ = next(os.walk(EXERCISE_PATH))
    for dir in dirnames:
        if dir != "bad":
            student_id = dir
            current_student = find_student(students_lst, student_id)
            compile_and_run_all_tests3(EXERCISE_PATH, ex, student_id, current_student)

            check_if_used_stdlib(EXERCISE_PATH, ex, student_id, used_stdlib)
            # test results
            for i in range(num_of_questions):
                for j in range(tests_per_question_lst[i]):
                    ex_qt_identifier = ex + "_q" + str(i + 1) + "t" + str(j + 1)
                    student_res_file_name = os.path.join(EXERCISE_PATH, dir,
                                                         ex_qt_identifier + "_" + student_id + ".txt")
                    sol_file_name = os.path.join(SOLUTION_DIR_NAME, ex_qt_identifier + "_sol.txt")
                    # compare files only if the result file exists
                    if os.path.isfile(student_res_file_name):
                        grade = get_test_grade(student_res_file_name, sol_file_name)
                        current_student.set_grade(i, j, grade)

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
            csv_cols += [qi + ", Test " + str(j + 1)]

    write_grades_to_CSV(csv_cols, students_lst)

    # print errors and IDs:
    print_fatal_errors(num_of_questions, tests_per_question_lst)
    print_bads(used_stdlib, "Used stdlib.h library")
