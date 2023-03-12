import sqlite3
import csv
import os

def create_database():
# Check if the database file already exists.
    if not os.path.isfile('hogwarts_legacy_reviews.db'):
        with sqlite3.connect('hogwarts_legacy_reviews.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE reviews
                            (reviewID INTEGER PRIMARY KEY, playtime INTEGER, feedback TEXT, reviewText TEXT)''')
            # Insert the data from csv file into the database, utf-8 encoding is used for handling the codec errors
            with open('hogwarts_legacy_reviews.csv', 'r', encoding='utf-8') as csvfile:
                csvreader = csv.DictReader(csvfile)
                rows = [(row['Playtime'], row['Feedback'], row['Review']) for row in csvreader]
                cursor.executemany('INSERT INTO reviews (playtime, feedback, reviewText) VALUES (?, ?, ?)', rows)
            conn.commit()
            print("Successfully created the .db file.")
    else:
        return

def positive_negative_ratio():
    """Query to get the sum of positive, negative reviews, total count of reviews and what is the positive/negative ratio"""
    with sqlite3.connect('hogwarts_legacy_reviews.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT
                        SUM(CASE WHEN feedback = "Positive" THEN 1 ELSE 0 END) AS positive_count,
                        SUM(CASE WHEN feedback = "Negative" THEN 1 ELSE 0 END) AS negative_count,
                        COUNT(*) AS total_count,
                        ROUND((SUM(CASE WHEN feedback = "Positive" THEN 1 ELSE 0 END) * 1.0 / COUNT(*)), 2) AS positive_ratio,
                        ROUND((SUM(CASE WHEN feedback = "Negative" THEN 1 ELSE 0 END) * 1.0 / COUNT(*)), 2) AS negative_ratio
                        FROM reviews;
                        """)
        result = cursor.fetchone()
        #annotated_result = f"Count of positive reviews: {result[0]}. Count of negative reviews: {result[1]}. Total count of reviews: {result[2]}. Positive ratio: {result[3]}. Negative ratio: {result[4]}."
    return result

def max_negative_positive_playtime_review():
    """Query to get reviewTexts with most playtime for both negative and positive review along with the playtime"""
    with sqlite3.connect('hogwarts_legacy_reviews.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT 
                        CASE WHEN feedback = 'Positive' THEN 'Positive' ELSE 'Negative' END AS feedback_type,
                        MAX(playtime) AS max_playtime,
                        reviewText
                        FROM reviews
                        GROUP BY feedback_type;
                        """)
        result = cursor.fetchall()
    return result

def average_playtime():
    with sqlite3.connect('hogwarts_legacy_reviews.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT feedback_type, AVG(avg_playtime) AS avg_playtime
                        FROM (
                        SELECT 
                            CASE WHEN feedback = 'Positive' THEN 'Positive' ELSE 'Negative' END AS feedback_type,
                            AVG(playtime) AS avg_playtime
                        FROM reviews
                        GROUP BY feedback_type
                        
                        UNION ALL
                        
                        SELECT 'All' AS feedback_type, AVG(playtime) AS avg_playtime
                        FROM reviews
                        ) AS subquery
                        GROUP BY feedback_type;
                        """)
        result = cursor.fetchall()
    return result

def fetch_all_data():
    with sqlite3.connect('hogwarts_legacy_reviews.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM reviews')
        result = cursor.fetchall()
        return result
            