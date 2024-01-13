import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Load and preprocess data
data = pd.read_csv('bot_detection_data.csv')
X = data.drop(['BotLabel', 'Hashtags'], axis=1)
y = data['BotLabel']
encoder = LabelEncoder()
X['Username'] = encoder.fit_transform(data['Username'])
X['Tweet'] = encoder.fit_transform(data['Tweet'])
X['Location'] = encoder.fit_transform(data['Location'])
X['CreatedAt'] = encoder.fit_transform(data['CreatedAt'])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Naive Bayes
bayes = GaussianNB().fit(X_train, y_train)
bayes_predict = bayes.predict(X_test)
print(bayes_predict)
print(accuracy_score(y_test, bayes_predict))
print(classification_report(y_test, bayes_predict))

# Logistic regression
logistic = LogisticRegression().fit(X_train, y_train)
logistic_predict = logistic.predict(X_test)
print(logistic_predict)
print(accuracy_score(y_test, logistic_predict))
print(classification_report(y_test, logistic_predict))

# Random Forest
rf = RandomForestClassifier().fit(X_train, y_train)
rf_predict = rf.predict(X_test)
print(rf_predict)
print(accuracy_score(y_test, rf_predict))
print(classification_report(y_test, rf_predict))




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
