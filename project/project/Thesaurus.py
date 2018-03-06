from nltk.corpus import wordnet as wn

import inverted_index

def GetSimilarNames(str):
    similarNames = []
    for word in str.split():
        for synonym in wn.synsets(word):
            for lemma in synonym.lemmas():
                new_query_term = lemma.name().lower()
                if word != new_query_term:
                    similarNames.append(new_query_term)
    return inverted_index.process_text({'TEXT': " ".join(similarNames)})
