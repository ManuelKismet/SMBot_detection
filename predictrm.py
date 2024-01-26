import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from scipy.sparse import hstack, csr_matrix
import re
from nltk.stem import WordNetLemmatizer
import psutil


# Download the WordNet resources (run once)
# import nltk
# nltk.download('wordnet')

def feature_engineering(arg):
    arg['TweetLength'] = arg['Tweet'].str.len()  # Create tweet length feature
    arg['HourCreated'] = pd.to_datetime(arg['CreatedAt']).dt.hour  # Extract hour
    arg['MentionCount'] = arg['Tweet'].apply(lambda x: len(re.findall(r'@\w+', x)))  # Count mentions
    arg['HashtagCount'] = arg['Tweet'].apply(lambda x: len(re.findall(r'#\w+', x)))  # Count hashtags
    arg['URLCount'] = arg['Tweet'].apply(lambda x: len(
        re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                   x)))  # Count URLs
    return arg


data = feature_engineering(pd.read_csv('bot_detection_data.csv'))

lemmatizer = WordNetLemmatizer()


def custom_tokenizer(text):
    words = re.findall(r'\b\w+\b', text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return lemmatized_words


def preprocess_data(pp_data, chunk_size=1000):
    x_data = pp_data.drop(['BotLabel', 'Hashtags'], axis=1)
    y_data = pp_data['BotLabel']

    # Extract numerical features
    numerical_features = ['TweetLength', 'HourCreated', 'MentionCount', 'HashtagCount', 'URLCount', 'RetweetCount',
                          'FollowerCount', 'Verified', 'URLCount']
    numerical_data = x_data[numerical_features]

    # Scaling numerical features
    scaler = StandardScaler()
    for start_idx in range(0, len(numerical_data), chunk_size):
        end_idx = min(start_idx + chunk_size, len(numerical_data))
        chunk_numerical = numerical_data[start_idx:end_idx]
        scaler.partial_fit(chunk_numerical)
    scaled_numerical_data = scaler.transform(numerical_data)

    categorical_features = ['Username', 'Location', 'CreatedAt']

    ohe = OneHotEncoder(sparse_output=True)
    sparse_matrices = [ohe.fit_transform(x_data[col].values.reshape(-1, 1)) for col in categorical_features]
    x_encoded = hstack(sparse_matrices)

    # Extract text features and perform TF-IDF vectorization
    print("Before vectorization:")
    print(x_data['Tweet'].describe())
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
    print("\nAfter vectorization:")
    print(pd.DataFrame(tokenized_tweets.toarray()).describe())
    print("Negative values in tokenized_tweets:", (tokenized_tweets < 0).sum())
    for i in range(5):  # Print the first 5 tokenized tweets
        print(f"Tokenized tweet {i + 1}: {tokenized_tweets[i]}")
    print("Shape of tokenized_tweets:", tokenized_tweets.shape)
    print("Available memory:", psutil.virtual_memory().available)

    # Combine features
    x_combined = csr_matrix(hstack([x_encoded, tokenized_tweets, csr_matrix(scaled_numerical_data)]))

    return x_combined, y_data


X, y = preprocess_data(data)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Multinomial Naive Bayes
clf = MultinomialNB()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print("Printing for MultinomialNB")
scores = cross_val_score(clf, X_train, y_train, cv=5)
print("Cross-validation accuracy:", np.mean(scores))
print(y_pred)
print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
print("Accuracy:", clf.score(X_test, y_test))

# Random Forest
rf = RandomForestClassifier(n_estimators=120)
rf.fit(X_train, y_train)
rf_predict = rf.predict(X_test)
importances = rf.feature_importances_
print("Feature importances:\n", importances)
print("Printing for random forest")
print(rf_predict)
print(accuracy_score(y_test, rf_predict))
print(classification_report(y_test, rf_predict))

# Ensemble with MNB and RF
ensemble = VotingClassifier([('mnb', clf), ('rf', rf)], voting='soft')
ensemble.fit(X_train, y_train)
ensemble_pred = ensemble.predict(X_test)
print(ensemble_pred)
