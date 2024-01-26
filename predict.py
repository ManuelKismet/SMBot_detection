import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from scipy.sparse import hstack, csr_matrix, coo_matrix
import re
from nltk.stem import WordNetLemmatizer


# Download the WordNet resources (run once)
# import nltk
# nltk.download('wordnet')


def feature_engineering(arg):
    arg['TweetLength'] = arg['Tweet'].str.len()  # Create tweet length featur
    arg['HourCreated'] = pd.to_datetime(arg['CreatedAt']).dt.hour  # Extract hour
    arg['MentionCount'] = arg['Tweet'].apply(lambda x: len(re.findall(r'@\w+', x)))  # Count mentions
    arg['HashtagCount'] = arg['Tweet'].apply(lambda x: len(re.findall(r'#\w+', x)))  # Count hashtags
    arg['URLCount'] = arg['Tweet'].apply(lambda x: len(
        re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                   x)))  # Count URLs
    return arg


def custom_tokenizer(text_series):
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = []
    for text in text_series:
        words = re.findall(r'\b\w+\b', str(text))
        lemmatized_words.extend([lemmatizer.lemmatize(word) for word in words])
    return lemmatized_words


def preprocess_data(pp_data):
    x_data = pp_data.drop(['BotLabel', 'Hashtags'], axis=1)
    y_data = pp_data['BotLabel']

    numerical_features = ['TweetLength', 'HourCreated', 'MentionCount', 'HashtagCount', 'URLCount', 'RetweetCount',
                          'FollowerCount', 'Verified', 'URLCount']
    numerical_data = x_data[numerical_features]
    scaler = StandardScaler()
    scaled_numerical_data = scaler.fit_transform(numerical_data)

    categorical_columns = ['Username', 'Location', 'CreatedAt']
    encoder = OneHotEncoder()
    x_encoded = encoder.fit_transform(x_data[categorical_columns])

    count_vectorizer = CountVectorizer(
        tokenizer=custom_tokenizer,
        lowercase=True,
        strip_accents='ascii',
        ngram_range=(1, 2),
        max_df=0.9,
        min_df=2,
        max_features=5000
    )
    tokenized_tweets = count_vectorizer.fit_transform(x_data['Tweet'])
    combined_matrix = hstack([tokenized_tweets, x_encoded, scaled_numerical_data])

    return combined_matrix, y_data


data = feature_engineering(pd.read_csv('bot_detection_data.csv'))
X, y = preprocess_data(data)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Specify the hyperparameter grid for Logistic Regression
param_grid_lr = {'C': [0.001, 0.01, 0.1, 1, 10, 100], 'max_iter': [500, 1000, 1500]}
logistic_model = LogisticRegression()
grid_search_lr = GridSearchCV(logistic_model, param_grid_lr, cv=5)
grid_search_lr.fit(X_train, y_train)
best_logistic_model = grid_search_lr.best_estimator_
print("Best hyperparameters for Logistic Regression:", grid_search_lr.best_params_)

# # Specify the hyperparameter grid for Random Forest
# param_grid_rf = {
#     'n_estimators': [50, 100, 200],
#     'max_depth': [None, 10, 20, 30],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4]
# }
# random_forest_model = RandomForestClassifier()
# grid_search_rf = GridSearchCV(random_forest_model, param_grid_rf, cv=5)
# grid_search_rf.fit(X_train, y_train)
# best_rf_model = grid_search_rf.best_estimator_
# print("Best hyperparameters for Random Forest:", grid_search_rf.best_params_)

# Define the hyperparameter grid for GradientBoostingClassifie
param_grid_gb = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7]
}
gb_classifier = GradientBoostingClassifier(random_state=42)
grid_search_gb = GridSearchCV(gb_classifier, param_grid_gb, cv=5, scoring='accuracy', n_jobs=-1)
grid_search_gb.fit(X_train, y_train)
best_gb_model = grid_search_gb.best_estimator_
print("Best hyperparameters for GradientBoostingClassifier:", grid_search_gb.best_params_)

voting_classifier = VotingClassifier(estimators=[
    ('logistic', best_logistic_model),
    # ('random_forest', best_rf_model),
    ('gb_classifier', best_gb_model)
])
voting_classifier.fit(X_train, y_train)
voting_predict = voting_classifier.predict(X_test)
scores = cross_val_score(voting_classifier, X_train, y_train, cv=5)
print("Cross-validation accuracy:", np.mean(scores))
print("Printing for Voting Classifier")
print(voting_predict)
print(accuracy_score(y_test, voting_predict))
print(classification_report(y_test, voting_predict))

# # Logistic regression
# logistic = LogisticRegression().fit(X_train, y_train)
# logistic_predict = logistic.predict(X_test)
# print("printing for logistic regression")
# print(logistic_predict)
# print(accuracy_score(y_test, logistic_predict))
# print(classification_report(y_test, logistic_predict))
#
# # Random Forest
# rf = RandomForestClassifier()
# rf.fit(X_train, y_train)
# rf_predict = rf.predict(X_test)
# print("printing for random forest")
# print(rf_predict)
# print(accuracy_score(y_test, rf_predict))
# print(classification_report(y_test, rf_predict))

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


# encoding Label Encoding
# encoder = LabelEncoder()
# X['Username'] = encoder.fit_transform(data['Username'])
# X['Tweet'] = encoder.fit_transform(data['Tweet'])
# X['Location'] = encoder.fit_transform(data['Location'])
# X['CreatedAt'] = encoder.fit_transform(data['CreatedAt'])

# encoder = LabelEncoder()
# X = data[['Username', 'Location', 'TweetLength', 'NumHashtags', 'HourCreated']]
# X = X.apply(encoder.fit_transform)


# X = csr_matrix(hstack([X_encoded, X_tweet]))  # Combine encoded features and numerical features (if any)
# # X = np.hstack((X, X_tweet.toarray()))  # Combine text features with other features


# Split data into training and testing sets

# categorical_features = ['Username', 'Location', 'CreatedAt']  # encoding one-hot
# ohe = OneHotEncoder(sparse_output=True)
# sparse_matrices = [ohe.fit_transform(data[col].values.reshape(-1, 1)) for col in categorical_features]
# X_encoded = hstack(sparse_matrices)
# vectorizer = HashingVectorizer(preprocessor=True, lowercase=True, tokenizer=True, strip_accents='ascii',
#                                n_features=2 ** 18)
# tokenized_tweets = vectorizer.fit_transform(data['Tweet'])
# tfidf = TfidfVectorizer(input='content')  # Vectorize text using TF-IDF
# X_tweet = tfidf.fit_transform(tokenized_tweets)

# # Load
# data = pd.read_csv('bot_detection_data.csv')
#
# # Feature engineering
# data['TweetLength'] = data['Tweet'].str.len()  # Create tweet length feature
# # data['NumHashtags'] = data['Hashtags'].str.split().str.len()  # Count hashtags
# data['HourCreated'] = pd.to_datetime(data['CreatedAt']).dt.hour  # Extract hour

# preprocess data

# # Naive Bayes
# bayes = GaussianNB().fit(X_train, y_train)
# bayes_predict = bayes.predict(X_test)
# print("printing for GuassianNB")
# print(bayes_predict)
# print(accuracy_score(y_test, bayes_predict))
# print(classification_report(y_test, bayes_predict))


# clf = MultinomialNB()
# clf.fit(X_train, y_train)
# y_pred = clf.predict(X_test)
# print("printing for MultinomialNB")
# print(y_pred)
# print(accuracy_score(y_test, y_pred))
# print(classification_report(y_test, y_pred))
# print("Accuracy:", clf.score(X_test, y_test))
