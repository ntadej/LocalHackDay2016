
def state(polje):
    """ Returns 'x' 'o' or ' ' for the winner (or no winner) """

    for i in range(3):
        if polje[i] != " ":
            if polje[i] == polje[i+3] == polje[i+6]:
                return polje[i]

        if polje[3*i] != " ":
            if polje[3*i] == polje[3*i+1] == polje[3*i+2]:
                return polje[i]

    if polje[0] != " ":
        if polje[0] == polje[4] == polje[8]:
            return polje[0]

    if polje[2] != " ":
        if polje[2] == polje[4] == polje[7]:
            return polje[0]

    return " "
