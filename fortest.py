# import csv
# import filecmp
#
# class MyClass:
#     def __init__(self, id):
#         self.id = id
#
#         #general errors
#         self.no_submission = True
#         self.too_many_files = False
#         self.bad_zip_name = False
#         self.no_zip_file = False
#
#         #q1 errors
#         self.q1_bad_c_file_err = False
#         self.q1_compilation_err = False
#         self.q1_wrong_output_err = False
#
#         #q2 errors
#         self.q2_bad_c_file_err = False
#         self.q2_compilation_err = False
#         self.q2_wrong_output_err = False
#
#         # #q3 errors
#         # self.q3_bad_c_file = False
#         # self.q3_comp_err = False
#         # self.q3_wrong_output = False
#
#
#     def __iter__(self):
#         return iter([
#             self.id,
#             # general errors
#             self.no_submission,
#             self.too_many_files,
#             self.bad_zip_name,
#             self.no_zip_file,
#             # q1 errors
#             self.q1_bad_c_file_err,
#             self.q1_compilation_err,
#             self.q1_wrong_output_err,
#             # q2 errors
#             self.q2_bad_c_file_err,
#             self.q2_compilation_err,
#             self.q2_wrong_output_err,
#         ])
#
#
#     def set_bad_c_file_err(self, q_num):
#         if q_num == 1:
#             self.q1_bad_c_file_err = True
#         elif q_num == 2:
#             self.q2_bad_c_file_err = True
#         # elif q_num == 3:
#         #     self.q3_bad_c_file = True
#         else:
#             return
#
#     def set_comp_err(self, q_num):
#         if q_num == 1:
#             self.q1_compilation_err = True
#         elif q_num == 2:
#             self.q2_compilation_err = True
#         # elif q_num == 3:
#         #     self.q3_comp_err = True
#         else:
#              return
#
#     def set_wrong_output_err(self, q_num):
#         if q_num == 1:
#             self.q1_wrong_output_err = True
#         elif q_num == 2:
#             self.q2_wrong_output_err = True
#         # elif q_num == 3:
#         #     self.q3_wrong_output = True
#         else:
#              return
#
# def toCSV(students_lst):
#     csv_cols = [
#             "ID",
#             # general errors
#             "No submission",
#             "Too many files",
#             "Bad zip file name",
#             "No zip file",
#             # q1 errors
#             "Q1 - bad .c file name",
#             "Q1 - compilation error",
#             "Q1 - wrong output",
#             # q2 errors
#             "Q2 - bad .c file name",
#             "Q2 - compilation error",
#             "Q2 - wrong output",
#         ]
#     with open('results.csv', 'w') as csv_file:
#         wr = csv.writer(csv_file, delimiter=',')
#         wr.writerow(csv_cols)
#         for student in students_lst:
#             wr.writerow(list(student))
#
# #
# # lst = []
# # lst.append(MyClass("123456789"))
# # lst.append(MyClass("987654321"))
# # lst.append(MyClass("555555555"))
# # lst[0].bad_zip_name = None
# # toCSV(lst)
#
# # def compare_files(fpath1, fpath2):
# #     result = True
# #     with open(fpath1, 'r') as file1, open(fpath2, 'r') as file2:
# #         lines1 = [line.rstrip('\n') for line in file1.readlines()]
# #         lines2 = [line.rstrip('\n') for line in file2.readlines()]
# #         lines_min_cnt = min(len(lines1), len(lines2))
# #         for i in range(lines_min_cnt):
# #             if lines1[i] != lines2[i]:
# #                 print("DIFF in line " + str(i+1) + ":")
# #                 print("in file1: " + lines1[i])
# #                 print("in file2: " + lines2[i])
# #                 result = False
# #
# #         if len(lines1) < len(lines2):
# #             for i in range(lines_min_cnt, len(lines2)):
# #                 print("DIFF in line " + str(i+1) + ":")
# #                 print("in file1: (no line)")
# #                 print("in file2: " + lines2[i])
# #                 result = False
# #         elif len(lines1) > len(lines2):
# #             for i in range(lines_min_cnt, len(lines1)):
# #                 print("DIFF in line " + str(i+1) + ":")
# #                 print("in file1: " + lines1[i])
# #                 print("in file2: (no line)")
# #                 result = False
# #
# #         return result
# #

from student import *

class B:
    def __init__(self):
        self.Ba = "Ba"
        self.Bb = "Bb"

    def __iter__(self):
        return iter([self.Ba, self.Bb])
class A:
    def __init__(self):
        self.Aa = "Aaaaaaaaaaaaaaaaaa"
        self.Ab = "Ab"
        self.AB = B()

    def __iter__(self):
        return iter([self.Aa, self.Ab] + list(self.AB))
        #return iter(vars(self))



class C:
    def __init__(self, num_of_fields):
        for i in range(1, num_of_fields + 1):
            setattr(self, "f" + str(i), 12)

    def __iter__(self):
        return iter(vars(self))

a1 = A()
a2 = A()
b = B()
da = a1.__dict__.keys()
db = b.__dict__.keys()
# print(da)
# print(db)
#
# print(list(a1))
#
# c = C(4)
# print(c.__dict__.keys())
# print(list(c))

s = Student("123456789", 3, [2,2,3])
s.no_zip_file = "no zip"
s.bad_zip_name = "bad zip"
s.too_many_files = "too many"
s.no_submission = "no submission"
for i in range(3):
    current_q = s.questions[i]
    qi = "Q" + str(i)
    current_q.bad_c_file_err = qi + "-bad c file"
    current_q.compilation_err = qi + "-compilaton"
    num_of_tests = [2,2,3][i]
    for j in range(num_of_tests):
        current_q.tests[j] = qi + "T" + str(j)

print(list(s))



# students_lst = [a1, a2]
# with open('results.csv', 'w', newline="\n", encoding="utf-8") as csv_file:
#     wr = csv.writer(csv_file, delimiter=',')
#     #wr.writerow(csv_cols)
#     for student in students_lst:
#         wr.writerow(list(student))



