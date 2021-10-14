#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    # YOUR CODE HERE
    # If preferences do not align, auto 0
    if user1.gender not in user2.preferences or user2.gender not in user1.preferences:
        return 0

    # maximum number of matching responses, expected value
    maximum = len(user1.responses)
    mean = maximum/5

    # counts matches in responses
    raw = 0
    for i, opt in enumerate(user1.responses):
        raw += (opt == user2.responses[i])

    # Baseline scoring: if the number of matches is worse than random, give a 0. 
    # Otherwise, linear in the number of matches in range 0-1
    score = max(raw-mean, 0)/(maximum-mean)

    # At worst 0.75 multiplier if year difference is 3
    year_diff = abs(user1.grad_year - user2.grad_year)
    score *= 1/(1+year_diff/9) 

    return score


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
