import spacy
import wikipedia
import datetime
nlp = spacy.load('en')

KEYWORDS = ['when', 'where', 'build']
TIME_KEYWORDS = ['when']
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

TIME_SEARCH_PARAMS = ['created', 'built', 'born', 'erected']
TIME_DAY_KEYWORDS = ['until', 'year', 'in']

def read_input():
    input_data = input("> ")
    process_input(input_data)

def process_input(data):
    doc = nlp(data)
    nouns = []
    verbs = []
    keywords = []
    for word in doc:
        if word.lemma_ in KEYWORDS:
            keywords.append(word)
        elif word.pos_ == "NOUN" or word.pos_ == "PROPN":
            nouns.append(word.text)
        elif word.pos_ == "VERB":
            verbs.append(word)
    find_data(nouns, verbs, keywords)

def find_data(nouns, verbs, keywords):
    try:
        summary = wikipedia.summary(' '.join(nouns))
        output = ""
        for keyword in keywords:
            if keyword.lemma_ in TIME_KEYWORDS:
                output = find_dates(summary)
                min_date = None
                max_date = None
                if output != None:
                    for date in output:
                        if min_date == None or date < min_date:
                            min_date = date
                        if max_date == None or date > max_date:
                            max_date = date
                    output = "Created/Born: " + min_date.isoformat() + "\nRemoved/Died: " + max_date.isoformat()
                else:
                    output = "No dates could be found."
        print(output)
        print(summary)
    except wikipedia.PageError:
        print("No entry found with that name")

def find_dates(summary):
    doc = nlp(summary)
    results = []
    for i, word in enumerate(doc):
        if word.lemma_ in MONTHS:
            try:
                if doc[i - 1].lemma_ not in  TIME_DAY_KEYWORDS:
                    results.append(datetime.date(int(doc[i + 1].lemma_), MONTHS.index(doc[i].lemma_) + 1, int(doc[i - 1].lemma_)))
                else:
                    results.append(datetime.date(int(doc[i + 1].lemma_), MONTHS.index(doc[i].lemma_) + 1, 1))
            except ValueError as ex:
                return None
    if results == []:
        return None
    return results
if __name__ == "__main__":
    while True:
        read_input()