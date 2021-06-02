def divide(speech):
    words = speech.split(' ')
    grouped_words = []

    for (i,j) in zip(words, range(len(words))):
        if j%10==0 and j !=0:
            group = []
        else:
            group.append()
