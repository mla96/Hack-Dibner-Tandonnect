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

print(data)

# 4 answer choices from strongly disagree to strongly agree
choice_num = 4
fields_choice_num = ['Strongly Disagree', 'Disagree', 'Agree', 'Strongly Agree']
questions_num = 8
questions = ['Do students often study at Dibner?',
             'Do students prefer to study in groups?',
             'Do students mostly study alone?',
             'Do students wish they knew other students in their courses to study with?',
             'Are students interested in meeting classmates?',
             'Do students feel that discussion and mutual explanations are effective study methods?',
             'Do students use books at Dibner?',
             'Do students struggle with navigating Dibner?']

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
    fig, ax = plt.subplots()
    ind = np.arange(choice_num)
    width = 0.3  # Bar width
    p1 = plt.bar(ind, grad_array, width, color='blue')
    p2 = plt.bar(ind, undergrad_array, width, bottom=grad_array, color='red')
    plt.ylabel('Number of Students')
    if len(questions[j]) > 85:
        plt.title(("\n".join(wrap(questions[j], int(len(questions[j]) / 2)))))
    else:
        plt.title(("\n".join(wrap(questions[j], 50))))
    ax.set_xticks(np.arange(choice_num))
    ax.set_xticklabels(fields_choice_num)
    plt.legend((p1[0], p2[0]), ('Graduate', 'Undergraduate'))
    plt.savefig('orig_question_bar_' + str(j + 1) + '.png')


compare_questions = [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 2], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5],
                     [3, 4], [3, 5], [4, 5]]

for k in range(len(compare_questions)):

    # Print questions and correlation values
    compare_data = data[:, compare_questions[k]].astype(int)
    print(questions[compare_questions[k][0]])
    print(questions[compare_questions[k][1]])
    print(np.corrcoef(compare_data[:, 0], compare_data[:, 1]))

    count_array = np.zeros((choice_num, choice_num))
    for sample in compare_data:
        sample -= 1
        count_array[sample[0], sample[1]] += 1
    count_array = np.flipud(count_array)

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
            text = ax.text(j, i, int(count_array[i, j]), ha="center", va="center", color="w")

    ax.set_title('Correlating Questions ' + str(compare_questions[k][0] + 1) + ' and ' + str(compare_questions[k][1]
                                                                                             + 1))

    plt.xlabel("\n".join(wrap(questions[compare_questions[k][0]], len(questions[0]))))
    plt.ylabel("\n".join(wrap(questions[compare_questions[k][1]], int(len(questions[0]) / 2))), rotation=0)
    plt.tight_layout()
    plt.savefig('question_compare_' + str(int(compare_questions[k][0]) + 1) + '-' + str(int(compare_questions[k][1])
                                                                                       + 1) + '.png')

plt.show()
print(np.corrcoef(data[:, 0:7].astype(int).T))

true_data = data[:, 0:7].astype(int)
binary_data = np.zeros(true_data.shape)
for i in range(len(true_data)):
    for j in range(len(true_data[0])):
        binary_data[i][j] = 0 if true_data[i][j] <= 2 else 1
print(np.corrcoef(binary_data.astype(int).T))