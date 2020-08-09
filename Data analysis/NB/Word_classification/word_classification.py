#!/usr/bin/env python3

from collections import Counter
import urllib.request
from lxml import etree

import pandas as pd
import numpy as np

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn import model_selection

alphabet="abcdefghijklmnopqrstuvwxyzäö-"
alphabet_set = set(alphabet)

# Returns a list of Finnish words
def load_finnish():
    finnish_url="https://www.cs.helsinki.fi/u/jttoivon/dap/data/kotus-sanalista_v1/kotus-sanalista_v1.xml"
    filename="src/kotus-sanalista_v1.xml"
    load_from_net=False
    if load_from_net:
        with urllib.request.urlopen(finnish_url) as data:
            lines=[]
            for line in data:
                lines.append(line.decode('utf-8'))
        doc="".join(lines)
    else:
        with open(filename, "rb") as data:
            doc=data.read()
    tree = etree.XML(doc)
    s_elements = tree.xpath('/kotus-sanalista/st/s')
    return list(map(lambda s: s.text, s_elements))

def load_english():
    with open("src/words", encoding="utf-8") as data:
        lines=map(lambda s: s.rstrip(), data.readlines())
    return lines

def get_features(a):
    df = pd.DataFrame(index=a, columns=list(alphabet), data=[Counter(i) for i in a])
    df.replace(np.nan, 0, inplace=True)
    d = df.to_numpy()
    return d

def contains_valid_chars(s):
    x = True
    for a in s:
        if a not in list(alphabet):
            x = False
            break
    return x

def get_features_and_labels():
    e=[]
    f=[]
    english = list(load_english())
    finn = load_finnish()
    for words in english:
        if words[0].isupper():
            continue
        else:
            lower1=words.lower()
            if contains_valid_chars(lower1)==True:
                e.append(words)
            else:
                continue
    
    for word in finn:
        lower=word.lower()
        if contains_valid_chars(lower)==True:
            f.append(word)
        else:
            continue
    
    x1 = get_features(e)
    x0 = get_features(f)
    X = np.concatenate((x0, x1), axis=0)
    d = pd.Series(data = np.zeros(len(x0)))
    e = pd.Series(data = np.ones(len(x1)))
    y = d.append(e)
    
    return X, y

def word_classification():
    X, y = get_features_and_labels()
    cv = model_selection.KFold(n_splits=5, shuffle=True, random_state=0)
    model = MultinomialNB()
    model.fit(X, y)
    s = cross_val_score(model, X, y)
    s2 = cross_val_score(model, X, y, cv = cv)
    return s


def main():
    print("Accuracy scores are:", word_classification())

if __name__ == "__main__":
    main()
