import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from scipy.sparse import hstack, csr_matrix

# Load
data = pd.read_csv('bot_detection_data.csv')
X = data.drop(['BotLabel', 'Hashtags'], axis=1)
print(X.info())
y = data['BotLabel']

# preprocess data
# encoding Label Encoding
# encoder = LabelEncoder()
# X['Username'] = encoder.fit_transform(data['Username'])
# X['Tweet'] = encoder.fit_transform(data['Tweet'])
# X['Location'] = encoder.fit_transform(data['Location'])
# X['CreatedAt'] = encoder.fit_transform(data['CreatedAt'])

categorical_features = ['Username', 'Location', 'CreatedAt']  # encoding one-hot
ohe = OneHotEncoder(sparse=True)
sparse_matrices = [ohe.fit_transform(data[col].values.reshape(-1, 1)) for col in categorical_features]
X_encoded = hstack(sparse_matrices)
tfidf = TfidfVectorizer()  # Vectorize text using TF-IDF
X_tweet = tfidf.fit_transform(data['Tweet'])
X = np.hstack((X, X_tweet.toarray()))  # Combine text features with other features
X = csr_matrix(hstack([X_encoded, X_tweet]))  # Combine encoded features and numerical features (if any)

# Feature engineering
data['TweetLength'] = data['Tweet'].str.len()  # Create tweet length feature
data['NumHashtags'] = data['Hashtags'].str.split().str.len()  # Count hashtags
data['HourCreated'] = pd.to_datetime(data['CreatedAt']).dt.hour  # Extract hour

# Encode categorical features
encoder = LabelEncoder()
X = data[['Username', 'Location', 'TweetLength', 'NumHashtags', 'HourCreated']]
X = X.apply(encoder.fit_transform)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Naive Bayes
bayes = GaussianNB().fit(X_train, y_train)
bayes_predict = bayes.predict(X_test)
print("printing for GuassianNB")
print(bayes_predict)
print(accuracy_score(y_test, bayes_predict))
print(classification_report(y_test, bayes_predict))

clf = MultinomialNB()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("printing for MultinomialNB")
print(y_pred)
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
print("Accuracy:", clf.score(X_test, y_test))

# Random Forest
rf = RandomForestClassifier()
rf.fit(X_train, y_train)
rf_predict = rf.predict(X_test)
print("printing for random forest")
print(rf_predict)
print(accuracy_score(y_test, rf_predict))
print(classification_report(y_test, rf_predict))

print("random Forest")

# Logistic regression
logistic = LogisticRegression().fit(X_train, y_train)
logistic_predict = logistic.predict(X_test)
print("printing for logistic regression")
print(logistic_predict)
print(accuracy_score(y_test, logistic_predict))
print(classification_report(y_test, logistic_predict))

# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import accuracy_score, classification_report
# from sklearn.preprocessing import LabelEncoder
#
# data = pd.read_csv('bot_detection_data.csv')
# encoder = LabelEncoder()
# data['Username', 'Tweet'] = encoder.fit_transform(data['Username', 'Tweet'])
# X = data.drop('BotLabel', axis=1)
# y = data['BotLabel']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# model = LogisticRegression()
# model.fit(X_train, y_train)
#
# predictions = model.predict(X_test)
# accuracy = model.score(X_test, y_test)
# print("Accuracy:", accuracy)
#
# y_pred = model.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# print(f'Accuracy: {accuracy}')
# print(classification_report(y_test, y_pred))
