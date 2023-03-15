from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd


def Classifier(columns):
    data = pd.read_csv("Dataset/Model_Dataset.csv")
    vector = TfidfVectorizer()
    x_train = vector.fit_transform(data.iloc[:,0])
    target = data.iloc[:,1]
    model = MultinomialNB()
    model.fit(x_train, target)
    new = vector.transform(columns)
    print(new)
    return model.predict(new)

