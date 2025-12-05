import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

df = pd.read_csv("datasets/processed_dataset.csv")

texts = df["text"]
labels = df["label"]

train_text, test_text, train_labels, test_labels = train_test_split(texts, labels, test_size=0.2)

tfidf = TfidfVectorizer()
train_text = tfidf.fit_transform(train_text)
test_text = tfidf.transform(test_text)

nb = MultinomialNB()
nb.fit(train_text, train_labels)

correct = 0
predictions = nb.predict(test_text)
for i in range(len(predictions)):
    if predictions[i] == test_labels.iloc[i]:
        correct = correct + 1

accuracy = correct / len(predictions)
print("accuracy: " + str(round(accuracy * 100, 2)) + "%")

joblib.dump(nb, "models/model.pkl")
joblib.dump(tfidf, "models/vectorizer.pkl")

print("model saved")
