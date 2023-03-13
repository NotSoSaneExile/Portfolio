import sqlite3
import pandas as pd
from database import create_database, positive_negative_ratio
from sentiment_analysis import download_nltk_packages, prepare_data
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix, classification_report

if __name__ == '__main__':
    try:
        download_nltk_packages()
        create_database()
        with sqlite3.connect("hogwarts_legacy_reviews.db") as conn:
            X_train, X_test, y_train, y_test = prepare_data(conn)
            pipeline = Pipeline(
                [('vectorizer', TfidfVectorizer()), ('classifier', MultinomialNB())],
                verbose=True
                )
            params = {
                'vectorizer__max_df': [0.5, 0.75, 1.0],
                'vectorizer__ngram_range': [(1, 1), (1, 2)],
                'classifier__alpha': [0.1, 0.5, 1.0]
            }
            grid_search = GridSearchCV(pipeline, params, cv=5, n_jobs=-1, verbose=1)
            grid_search.fit(X_train, y_train)
            y_pred = grid_search.best_estimator_.predict(X_test)
            conf_matrix = confusion_matrix(y_test, y_pred)
            conf_matrix_df = pd.DataFrame(conf_matrix, columns=['Negative', 'Positive'], index=['Negative', 'Positive'])
            conf_matrix_df.columns.name = "True value \ Predicted value"
            print(conf_matrix_df)
            print(classification_report(y_test, y_pred))
            score = grid_search.score(X_test, y_test)
            print('Accuracy:', score)
    except Exception as e:
        print("Error:", e)