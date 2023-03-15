from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd

# Create Classifier Method to classify column names
def Classifier(columns):
    
    # Read Dataset for Classification
    data = pd.read_csv("Dataset/Model_Dataset.csv")

    # Create TfidfVectorizer to fit and transform labels
    vector = TfidfVectorizer()
    
    # Train and Transform labels into vectors
    x_train = vector.fit_transform(data.iloc[:,0])
    target = data.iloc[:,1]

    # Create MultinomialNB model
    model = MultinomialNB()
    
    #Train the model using label and target
    model.fit(x_train, target)

    # Transform arguments into vector
    new = vector.transform(columns)
    
    # Return Predicted value
    return model.predict(new)

