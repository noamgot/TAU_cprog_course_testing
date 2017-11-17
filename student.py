X = "X"


class FatalErrorsLists:
    #general errors
    no_submission = []
    too_many_files = []
    no_zip_file = []
    bad_zip_name = []
    bad_c_file_name = []
    compilation_error = []
    test_timeout = []


class Question:
    def __init__(self, num_of_tests):
        self.bad_c_file_err = None
        self.compilation_err = None
        self.tests = [None] * num_of_tests

    def __iter__(self):
        return iter(
            [self.bad_c_file_err,
             self.compilation_err] +
            self.tests
        )


class Student:
    def __init__(self, student_id, num_of_questions, tests_per_qusetion_lst):
        # validate tests-per-question list is exactly at the size of the number of questions
        assert len(tests_per_qusetion_lst) == num_of_questions, "len(tests_per_qusetion_lst) != num_of_questions"

        self.student_id = student_id

        # general errors
        self.no_submission = X
        self.too_many_files = None
        self.bad_zip_name = None
        self.no_zip_file = None
        self.questions = [Question(n) for n in tests_per_qusetion_lst]

    def __iter__(self):
        questions_attr_lst = [list(q) for q in self.questions]
        return iter(
            [self.student_id,
             # general errors
             self.no_submission,
             self.too_many_files,
             self.bad_zip_name,
             self.no_zip_file] +
            [attr for question_attr in questions_attr_lst for attr in question_attr]
        )

    # for all the setters - question_num is passed 0-based
    def set_bad_c_file_err(self, question_num):
        self.questions[question_num].bad_c_file_err = X

    def set_compilation_err(self, question_num):
        self.questions[question_num].compilation_err = X

    def set_wrong_output_err(self, question_num, test_num):
        self.questions[question_num].tests[test_num] = X




        # def __init__(self, id):
        #     self.id = id
        #
        #     #general errors
        #     self.no_submission = X
        #     self.too_many_files = None
        #     self.bad_zip_name = None
        #     self.no_zip_file = None
        #
        #     #q1 errors
        #     self.q1_bad_c_file_err = None
        #     self.q1_compilation_err = None
        #     self.q1_wrong_output_err = None
        #
        #     #q2 errors
        #     self.q2_bad_c_file_err = None
        #     self.q2_compilation_err = None
        #     self.q2_wrong_output_err = None
        #
        #     # #q3 errors
        #     # self.q3_bad_c_file = None
        #     # self.q3_comp_err = None
        #     # self.q3_wrong_output = None
        #
        # def __iter__(self):
        #     return iter([
        #         self.id,
        #         # general errors
        #         self.no_submission,
        #         self.too_many_files,
        #         self.bad_zip_name,
        #         self.no_zip_file,
        #         # q1 errors
        #         self.q1_bad_c_file_err,
        #         self.q1_compilation_err,
        #         self.q1_wrong_output_err,
        #         # q2 errors
        #         self.q2_bad_c_file_err,
        #         self.q2_compilation_err,
        #         self.q2_wrong_output_err,
        #     ])
        #
        # def set_bad_c_file_err(self, q_num):
        #     if q_num == 1:
        #         self.q1_bad_c_file_err = X
        #     elif q_num == 2:
        #         self.q2_bad_c_file_err = X
        #     # elif q_num == 3:
        #     #     self.q3_bad_c_file = X
        #     else:
        #         return
        #
        # def set_compilation_err(self, q_num):
        #     if q_num == 1:
        #         self.q1_compilation_err = X
        #     elif q_num == 2:
        #         self.q2_compilation_err = X
        #     # elif q_num == 3:
        #     #     self.q3_comp_err = X
        #     else:
        #          return
        #
        # def set_wrong_output_err(self, q_num):
        #     if q_num == 1:
        #         self.q1_wrong_output_err = X
        #     elif q_num == 2:
        #         self.q2_wrong_output_err = X
        #     # elif q_num == 3:
        #     #     self.q3_wrong_output = X
        #     else:
        #          return
