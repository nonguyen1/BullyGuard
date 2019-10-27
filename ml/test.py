a = ["sent one and some more", "sent three and some more", "sent four and some more"]


def findPhrase(phrase, data):


    for sent in data:
        if phrase in sent:
            print(sent)


    return "cool"


print(findPhrase("some more", a))
