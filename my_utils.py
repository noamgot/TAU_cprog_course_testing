import argparse
import csv
import errno
import os
import shutil
import subprocess
import zipfile

from student import *


EXERCISE_PATH = os.path.join(os.environ['HOMEDRIVE'], os.environ['HOMEPATH'], "Desktop","C_exercises")
SOLUTION_DIR_NAME = os.path.join(os.getcwd(),"solutions")
INPUT_DIR_NAME = os.path.join(os.getcwd(),"input")


def run_tests_on_solution(ex, num_of_questions, tests_per_question_lst):
    for i in range(num_of_questions):
        num_of_tests = tests_per_question_lst[i]
        exe_path = os.path.join(SOLUTION_DIR_NAME, ex + "_q" + str(i + 1) + "_sol.exe")
        for j in range(num_of_tests):
            ex_qt_identifier = ex + "_q" + str(i + 1) + "t" + str(j + 1)
            input_file = open(os.path.join(INPUT_DIR_NAME, ex_qt_identifier + "_input.txt"), "r")
            res_file = open(os.path.join(SOLUTION_DIR_NAME, ex_qt_identifier + "_sol.txt"), "w")
            rc = run_command(exe_path, input_file ,res_file)
            assert rc == 0, "Unexpected solution timeout!!!"  # timeout!
            input_file.close()
            res_file.close()


# giving a very generous default timout of 10 seconds
def run_command(cmd, cmd_stdin=None, cmd_stdout=None, timeout=10):
    try:
        subprocess.run(cmd, timeout, stdin=cmd_stdin, stdout=cmd_stdout)
        return 0
    except subprocess.TimeoutExpired:
        return 1


def parse_input():

    parser = argparse.ArgumentParser()
    parser.add_argument("ex", help="Exercise number", type=int, choices=list(range(7)))
    parser.add_argument("qs", help="Number of questions", type=int, choices=list(range(1, 11)))
    parser.add_argument("tests_per_question", help="How many tests per question", type=int, choices=list(range(1, 21)),
                        nargs="+")

    args = parser.parse_args()
    if args.qs != len(args.tests_per_question):
        parser.error("tests_per_question list doesn't match the number of questions")

    print("Exercise number: " + str(args.ex))
    print("Number of questions: " + str(args.qs))
    print("Tests per question: " + str(args.tests_per_question))

    return args


def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def find_student(students_lst, id_to_find):
    for student in students_lst:
        if student.student_id == id_to_find:
            return student
    return None


def update_no_submission_lst(students_lst):
    for student in students_lst:
        if student.no_submission == X:
            FatalErrorsLists.no_submission.append(student.student_id)


def extract_zip_files(path, ex, students_lst):
    first_bad_file = True
    _, dirnames, _ = next(os.walk("."))
    for curr_dir in dirnames:
        # our legal directories contain the "_file_" substring
        if "_file_" not in curr_dir:
            continue
        curr_id = curr_dir.split("_file_", 1)[1][:9]
        # find current student
        curr_student = find_student(students_lst, curr_id)
        if curr_student is None:
            raise ValueError("No student was found with id - {}".format(curr_id))

        curr_student.no_submission = None  # student submitted...

        _, _, filenames = next(os.walk(curr_dir))
        if len(filenames) != 1:  # should be only one .zip file
            curr_student.too_many_files = X
            FatalErrorsLists.too_many_files.append(curr_id)
        elif filenames[0].endswith(".zip"):
            if filenames[0][:-4] != (ex + "_" + curr_id):
                curr_student.bad_zip_name = X
                FatalErrorsLists.bad_zip_name.append(curr_id)
            zip_file = os.path.join(".", curr_dir, filenames[0])
            dir_to_extract = os.path.join(path, curr_id)
            make_dir(dir_to_extract)
            zip_ref = zipfile.ZipFile(zip_file, 'r')
            zip_ref.extractall(dir_to_extract)
            zip_ref.close()
        else:  # not a .zip file
            not_zip_dir = os.path.join(path, "bad")
            if first_bad_file:
                make_dir(not_zip_dir)
                first_bad_file = False
            shutil.copy(os.path.join(".", curr_dir, filenames[0]), os.path.join(not_zip_dir))
            curr_student.no_zip_file = X
            FatalErrorsLists.no_zip_file.append(curr_id)


# def run_exe_files(path ,dir, ex, id, question_num, bad_c_name_lst, comp_error_lst):
#     c_path = os.path.join(path, dir, ex + "_q" + question_num + "_" + id + ".c")
#     if os.path.isfile(c_path):
#         exe_path = os.path.join(path, dir, ex + "_q" + question_num + "_" + id + ".exe")
#         if os.path.isfile(exe_path):
#             os.system(exe_path + " > " + exe_path[:-4] + ".txt")
#         else:  # compilation error
#             comp_error_lst.append(id)
#     else:
#         bad_c_name_lst.append(id)


def compile_and_run_question(path, ex, student_id, question_num, num_of_tests, student):
    """question_num should be passed 0-based, i.e - question 1 will be passed as 0, etc. """
    c_path = os.path.join(path, student_id, ex + "_q" + str(question_num+1) + "_" + student_id + ".c")
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
            rc = run_command(exe_path, input_file, res_file)
            if rc != 0:  # timeout!
                FatalErrorsLists.test_timeout[question_num][i].append(student_id)
            input_file.close()
            res_file.close()
    else:  # ex does not exists - compilation error
        student.set_compilation_err(question_num)
        FatalErrorsLists.compilation_error[question_num].append(student_id)


def compile_and_run_all_tests(path, ex, student_id, num_of_questions, tests_per_question_lst, student):
    for i in range(num_of_questions):
        num_of_tests = tests_per_question_lst[i]
        compile_and_run_question(path, ex, student_id, i, num_of_tests, student)


def print_bads(lst, title):
    if not lst:
        return #print only non-empty lists
    print("*** " + title + " ***")
    for bad in lst:
        print(bad)

def print_fatal_errors(num_of_questions, tests_per_question_lst):
    print_bads(FatalErrorsLists.no_submission, "No submission")
    print_bads(FatalErrorsLists.too_many_files, "Too many files")
    print_bads(FatalErrorsLists.no_zip_file, "No zip file")
    print_bads(FatalErrorsLists.bad_zip_name, "Bad zip file name")
    for i in range(num_of_questions):
        qi = "Q" + str(i + 1)
        print_bads(FatalErrorsLists.bad_c_file_name[i], qi + " - Bad .c file name")
        print_bads(FatalErrorsLists.compilation_error[i], qi + " - Compilation error")
        for j in range(tests_per_question_lst[i]):
            qitj = qi + "T" + str(j + 1)
            print_bads(FatalErrorsLists.test_timeout[i][j], qitj + " - Timout error")

def init_students_list(students_file_path, num_of_questions, tests_per_question_lst):
    students_lst = []
    students_file = open(students_file_path)
    for line in students_file:
        student_id = line.rstrip('\n')
        students_lst.append(Student(student_id, num_of_questions, tests_per_question_lst))
    # students_lst = [Student(student_id.rstrip('\n'), num_of_questions, tests_per_question_lst) for student_id in students_file]
    students_file.close()
    return students_lst


def write_grades_to_CSV(csv_cols, students_lst):
    with open('results.csv', 'w', newline="\n", encoding="utf-8") as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        wr.writerow(csv_cols)
        for student in students_lst:
            wr.writerow(list(student))


def filesAreIdentical(test_path, sol_path):  # , diffpath):
    # result = True
    # diff_file = open(diffpath, 'w')
    with open(test_path, 'r') as test_file, open(sol_path, 'r') as sol_file:
        test_lines = [line.rstrip('\n') for line in test_file.readlines()]
        sol_lines = [line.rstrip('\n') for line in sol_file.readlines()]
        if len(sol_lines) != len(test_lines):
            return False
        for i in range(len(sol_lines)):
            if test_lines[i] != sol_lines[i]:
                return False
        return True

        # lines_min_cnt = min(len(test_lines), len(sol_lines))
        # for i in range(lines_min_cnt):
        #     if test_lines[i] != sol_lines[i]:
        #         diff_file.write("DIFF in line " + str(i + 1) + ":\n")
        #         diff_file.write("in test_file: " + test_lines[i] + "\n")
        #         diff_file.write("in sol_file: " + sol_lines[i] + "\n")
        #         result = False
        #
        # if len(test_lines) < len(sol_lines):
        #     for i in range(lines_min_cnt, len(sol_lines)):
        #         diff_file.write("DIFF in line " + str(i + 1) + ":\n")
        #         diff_file.write("in test_file: (no line)\n")
        #         diff_file.write("in sol_file: " + sol_lines[i] + "\n")
        #         result = False
        # elif len(test_lines) > len(sol_lines):
        #     for i in range(lines_min_cnt, len(test_lines)):
        #         diff_file.write("DIFF in line " + str(i + 1) + ":\n")
        #         diff_file.write("in test_file: " + test_lines[i] + "\n")
        #         diff_file.write("in sol_file: (no line)\n")
        #         result = False
        #
        # diff_file.close()
        # return result
