import csv
import numpy as np
import matplotlib.pyplot as plt
from textwrap import wrap


reader = csv.reader(open("Studying in Dibner (Responses) - Form Responses 1.csv", "r"), delimiter=",")
data = np.array(list(reader))

# Remove timestamp
data = data[:, 1:]

# Separate field names
fieldnames = data[0]
data = data[1:, :]

# 4 answer choices from strongly disagree to strongly agree
choice_num = 4
fields_choice_num = ['Strongly Disagree', 'Disagree', 'Agree', 'Strongly Agree']
questions_num = 8
questions = ['By education status, do students often study at Dibner?',
             'By education status, do students prefer to study in groups?',
             'By education status, do students mostly study alone?',
             'By education status, do students wish they knew other students in their courses to study with?',
             'By education status, are students interested in meeting classmates?',
             'By education status, do students feel that discussion and mutual explanations are effective study'
             ' methods?',
             'By education status, do students use books at Dibner?',
             'By education status, do students struggle with navigating Dibner?']

# Graphs of questions by education status
for j in range(questions_num):
    # Initialize plotting arrays
    grad_array = np.zeros(4)
    undergrad_array = np.zeros(4)
    for i in range(choice_num):
        grad_count = 0
        undergrad_count = 0
        for sample in data:
            if int(sample[j]) == i + 1 and sample[-1] == 'Graduate':
                grad_count = grad_count + 1
            elif int(sample[j]) == i + 1 and sample[-1] == 'Undergraduate':
                undergrad_count = undergrad_count + 1
        grad_array[i] = grad_count
        undergrad_array[i] = undergrad_count
    # Plot
    plt.figure(j + 1)
    ind = np.arange(choice_num)
    width = 0.3  # Bar width
    p1 = plt.bar(ind, grad_array, width, color='blue')
    p2 = plt.bar(ind, undergrad_array, width, bottom=grad_array, color='red')
    plt.ylabel('Number of Students')
    if len(questions[j]) > 60:
        plt.title(("\n".join(wrap(questions[j], int(len(questions[j]) / 2)))))
    else:
        plt.title(("\n".join(wrap(questions[j], 60))))
    plt.xticks(ind, ('1', fields_choice_num))
    plt.legend((p1[0], p2[0]), ('Graduate', 'Undergraduate'))
    plt.savefig('orig_question_bar_' + str(j + 1) + '.png')

# Correlating preferring to study in groups with wishing they knew more students in their courses
# Supplement to calculating correlation score?

compare_questions = [1, 3]

compare_data = data[:, compare_questions].astype(int)
count_array = np.zeros((choice_num, choice_num))
for sample in compare_data:
    sample -= 1
    count_array[sample[0], sample[1]] += 1
print(count_array)

plt.figure(questions_num + 1)
fig, ax = plt.subplots()
im = ax.imshow(count_array)

ax.set_xticks(np.arange(choice_num))
ax.set_yticks(np.arange(choice_num))
ax.set_xticklabels(fields_choice_num)
ax.set_yticklabels(list(reversed(fields_choice_num)))

plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Loop over data dimensions and create text annotations.
for i in range(choice_num):
    for j in range(choice_num):
        text = ax.text(j, i, count_array[i, j], ha="center", va="center", color="w")

ax.set_title('Correlating questions 2 and 4')
question_length = np.zeros(2)
# Wrap ax titles
# REMOVE "EDUCATION STATUS"
for i in range(len(compare_questions)):
    if len(questions[compare_questions[i]]) > 60:
        question_length[i] = int(len(questions[i]) / 2)
    else:
        question_length[i] = len(questions[i])
plt.xlabel("\n".join(wrap(questions[compare_questions[0]], question_length[0])))
plt.ylabel("\n".join(wrap(questions[compare_questions[1]], question_length[1])))
fig.tight_layout()
plt.savefig('correlation_test.png')

plt.show()