import numpy as np
from typing import List, Tuple

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """
    def pref_gender_mult(pref, gender):
        if pref == "Men":
            return 1 if gender == "Female" else 0.1
        elif pref == "Women":
            return 1 if gender == "Male" else 0.1
        else:
            return 1 if gender == "Non-binary" else 0.1

    n = len(scores)
    # random assign half the population to be proposers
    props = list(np.random.choice(n, n//2, replace=False))
    recvs = [i for i in range(n) if i not in props]
    print(props)
    print(recvs)

    # get the scores assigned by proposers, assigning the correct multiplier based on gender preferences
    # sorts the list in ascending order
    # afterwards, drop the score information, leaving only a ranking
    prop_scores = [ [(scores[props[i]][j]*pref_gender_mult(gender_pref[props[i]], gender_id[j]),j) for j in recvs] 
        for i in range(n//2)]
    for q in prop_scores:
        q.sort()
    prop_ls = list(map(lambda ls:list(map(lambda x:x[1], ls)), prop_scores))
    print(prop_ls)

    # same thing for receivers, but with a descending order sort
    recvs_scores =  [ [(scores[recvs[i]][j]*pref_gender_mult(gender_pref[recvs[i]], gender_id[j]),j) for j in props] 
        for i in range(n//2)]
    for pr in recvs_scores:
        pr.sort(reverse=True)
    recvs_ls = list(map(lambda ls:list(map(lambda x:x[1], ls)), recvs_scores))
    print(recvs_ls)

    # maps the person_id to their index in the props or recvs arrays
    mapback = [-1 for i in range(n)]
    for i, id in enumerate(props):
        mapback[id]=i
    for i, id in enumerate(recvs):
        mapback[id]=i

    # tracks who the receivers are currently assigned to
    current_matching = [-1 for i in recvs]

    # helper function for GS alg - assigns a proposer to the receiver and pops elements 
    # from receiver's ranking until current proposer is at the top
    def pair(pr, rcv):
        current_matching[mapback[rcv]] = pr
        while recvs_ls[mapback[rcv]][-1] != pr:
            recvs_ls[mapback[rcv]].pop()

    # list tracking unmatched proposers
    free_props = list(props)

    # GS - translation of pseudo-code in the pdf
    while(len(free_props)>0):
        pr = free_props.pop()
        rcv = prop_ls[mapback[pr]].pop()
        if current_matching[mapback[rcv]] == -1:
            pair(pr, rcv)
        elif pr in recvs_ls[mapback[rcv]]:
            free_props.append(current_matching[mapback[rcv]])
            pair(pr, rcv)
        else:
            free_props.append(pr)

    # collects the pairings
    matches = [(current_matching[mapback[rcv]], rcv) for rcv in recvs]
    print(matches)
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
