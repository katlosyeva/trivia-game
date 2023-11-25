# class Lifeline:
#
#     def provide_lifeline(self):
#         pass
#
#
#
# class Fifty_Fifty(Lifeline):
#     def __init__(self, question_id):
#         self.question_id = question_id
#
#     def provide_lifeline(self):
#         # request to database is made, and two wrong answers are sent and returned
#         # front sees them and eliminates these two
#         pass
#
#
# class Phone(Lifeline):
#     def __init__(self, question_id):
#         self.question_id = question_id
#     def provide_lifeline(self):
#         # request to database is made, and correct and one wrong answer is sent back
#         # one is randomly chosen out of two and sent to FE
#         # front shows face of Bill Gates who says this answer
