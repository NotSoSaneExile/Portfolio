# Hogwarts Legacy Reviews Sentiment Analysis
This project performs a sentiment analysis of reviews for the video game "Hogwarts Legacy". The sentiment analysis is performed using the NLTK and Scikit-learn Python libraries.

# Dependencies
* nltk
* pandas
* scikit_learn

# Usage
To use this project, follow these steps:

1. Have Python >= 3.9 installed on your machine https://docs.python.org/3/using/index.html
2. Clone the repository to your local machine.
3. Install the required libraries using the command pip install -r requirements.txt.
4. Run python main.py to download necessary NLTK packages, create a SQLite3 database, and create a machine learning model pipeline.

# Files
The project contains the following files:

* database.py: Contains functions to create a SQLite3 database and run queries on it.
* sentiment_analysis.py: Contains functions to download NLTK packages, preprocess the data and prepare data for ML model.
* main.py: The main file that downloads necessary NLTK packages, creates a database, and creates a machine learning model pipeline.

# License
This project is licensed under the MIT License - see the LICENSE file for details.
