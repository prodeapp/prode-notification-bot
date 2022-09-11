
REALITY_TEMPLATE_SINGLE_SELECT = '2'
REALITY_TEMPLATE_MULTIPLE_SELECT = '3'
INVALID_RESULT = "0x" + "f" * 64
ANSWERED_TOO_SOON = "0x" + "f" * 63 + "e"


def formatAnswer(currentAnswer, templateID, outcomes):

    if currentAnswer == INVALID_RESULT:
        return 'Invalid result'

    if currentAnswer == ANSWERED_TOO_SOON:
        return 'Answered too soon'

    value = int(currentAnswer, 16)
    if templateID == REALITY_TEMPLATE_MULTIPLE_SELECT:
        return getMultiSelectAnswers(value, outcomes)

    if templateID == REALITY_TEMPLATE_SINGLE_SELECT:
        return outcomes[value]
    return value


def getMultiSelectAnswers(currentAnswer, outcomes):
    """Get the currentAnswer (hex string with 0x leading) and
    return all the outcomes as a string with comma separated"""
    answers = bin(currentAnswer)[2:]
    indexes = []

    for i in range(0, len(answers)):
        if answers[i] == '1':
            indexes.append(len(answers) - i - 1)
    if len(indexes) == 1:
        return outcomes[indexes[0]]
    else:
        filt_outcomes = [outcomes[i] for i in indexes]
        return ', '.join(filt_outcomes)


if __name__ == '__main__':
    print(ANSWERED_TOO_SOON, INVALID_RESULT)
