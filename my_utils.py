import os
import errno
import csv
from student import *
import zipfile
import shutil
import sys


def validate_input():
    assert len(sys.argv) == 2
    try:
        n = int(sys.argv[1])
    except:
        raise
    if n < 0 or n > 6:
        sys.exit("Invalid ex num, exiting...")

    return n

def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def find_student(students_lst, id_to_find):
    for student in students_lst:
        if student.id == id_to_find:
            return student
    return None


def extract_zip_files(path, ex, too_many_files, not_zip, bad_zip_name, students_lst):
    first_bad_file = True
    _, dirnames, _ = next(os.walk("."))
    for curr_dir in dirnames:
        if curr_dir == "__pycache__":
            continue
        curr_id = curr_dir.split("_file_", 1)[1][:9]
        # find current student
        curr_student = find_student(students_lst, curr_id)
        if curr_student is None:
            raise ValueError("No student was found!")

        curr_student.no_submission = None  # student submitted...

        _, _, filenames = next(os.walk(curr_dir))
        if len(filenames) != 1:  # should be only one .zip file
            curr_student.too_many_files = X
            too_many_files.append(curr_id)
        elif filenames[0].endswith(".zip"):
            if filenames[0][:-4] != (ex + "_" + curr_id):
                curr_student.bad_zip_name = X
                bad_zip_name.append(curr_id)

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
            not_zip.append(curr_id)


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

def compile_and_run_question(path, dir, ex, id, question_num, bad_c_name_lst, comp_error_lst, student):
    c_path = os.path.join(path, dir, ex + "_q" + str(question_num) + "_" + id + ".c")
    # check if .c file exists
    if not os.path.isfile(c_path):
        student.set_bad_c_file_err(question_num)
        bad_c_name_lst.append(id)
        return

    os.system("compile_single_file.bat " + ex + " " + dir + " " + c_path)
    exe_path = os.path.join(path, dir, ex + "_q" + str(question_num) + "_" + id + ".exe")
    if os.path.isfile(exe_path):
        os.system(exe_path + " > " + exe_path[:-4] + ".txt")
    else:  # ex does not exists - compilation error
        student.set_compilation_err(question_num)
        comp_error_lst.append(id)


def print_bads(lst):
    for bad in lst:
        print(bad)


def get_students_list(students_file_path, num_of_questions, tests_per_question_lst):
    students_lst = []
    students_file = open(students_file_path)
    for line in students_file:
        student_id = line.rstrip('\n')
        students_lst.append(Student(student_id, num_of_questions, tests_per_question_lst))
    #students_lst = [Student(student_id.rstrip('\n'), num_of_questions, tests_per_question_lst) for student_id in students_file]
    students_file.close()
    return students_lst


def write_grades_to_CSV(csv_cols, students_lst):
    with open('results.csv', 'w', newline="\n", encoding="utf-8") as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        wr.writerow(csv_cols)
        for student in students_lst:
            wr.writerow(list(student))


def filesAreIdentical(fpath1, fpath2, diffpath):
    result = True
    diff_file = open(diffpath, 'w')

    with open(fpath1, 'r') as file1, open(fpath2, 'r') as file2:
        lines1 = [line.rstrip('\n') for line in file1.readlines()]
        lines2 = [line.rstrip('\n') for line in file2.readlines()]
        lines_min_cnt = min(len(lines1), len(lines2))
        for i in range(lines_min_cnt):
            if lines1[i] != lines2[i]:
                diff_file.write("DIFF in line " + str(i + 1) + ":\n")
                diff_file.write("in file1: " + lines1[i] + "\n")
                diff_file.write("in file2: " + lines2[i] + "\n")
                result = False

        if len(lines1) < len(lines2):
            for i in range(lines_min_cnt, len(lines2)):
                diff_file.write("DIFF in line " + str(i + 1) + ":\n")
                diff_file.write("in file1: (no line)\n")
                diff_file.write("in file2: " + lines2[i] + "\n")
                result = False
        elif len(lines1) > len(lines2):
            for i in range(lines_min_cnt, len(lines1)):
                diff_file.write("DIFF in line " + str(i + 1) + ":\n")
                diff_file.write("in file1: " + lines1[i] + "\n")
                diff_file.write("in file2: (no line)\n")
                result = False

        diff_file.close()
        return result
