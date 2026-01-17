# movie-recommendation-
🎬 Intelligent Movie Recommendation System
A personalized movie recommendation engine that suggests films based on Content Similarity (using metadata like cast, director, and genres) and Mood Analysis (mapping user emotions to genres).

📌 Project Overview
Finding the right movie to watch can be overwhelming due to the sheer volume of choices. This project solves the "Paradox of Choice" by offering two recommendation pathways:

Similarity Search: Recommends movies similar to a specific title you already love.

Mood-Based Filtering: Recommends movies based on your current emotional state (e.g., Happy, Sad, Thrilling).

🚀 Features
Content-Based Filtering: Uses TF-IDF Vectorization and Cosine Similarity to analyze movie plots, genres, and cast information.

Mood-Based Suggestions: Maps human emotions (Happy, Sad, Action, etc.) to specific genre combinations for curated lists.

Smart Search: Handles spelling errors in movie titles using string matching (difflib).

Interactive Interface: Can be run via Command Line (CLI) or as a Web App using Streamlit.

🛠️ Tech Stack
Language: Python 3.14

Data Analysis: Pandas, NumPy

Machine Learning: Scikit-learn (TfidfVectorizer, Cosine Similarity)

Web Framework: Streamlit (Optional for UI)

📂 Dataset
The system uses the movies.csv dataset, which includes the following columns:

title

genres

cast

director

keywords

tagline

⚙️ Installation & Setup
Clone the Repository

Bash

cd movie-recommendation-system
Install Dependencies Ensure you have Python installed. Then run:

Bash

pip install pandas numpy scikit-learn streamlit
Add the Dataset Place your movies.csv file in the root directory of the project.

🖥️ Usage
Option 1: Run with Streamlit (Web App)
This provides a user-friendly graphical interface.

Bash

streamlit run app.py
Option 2: Run in Terminal (CLI)
This runs the script directly in your command prompt.

Bash

python main.py
🧠 How It Works
Data Preprocessing:

Fills missing values with empty strings.

Combines genres, cast, director, and keywords into a single "content string" for every movie.

Vectorization:

Converts the text data into numerical vectors using TF-IDF.

Similarity Calculation:

Calculates the Cosine Similarity score between the input movie and all other movies in the database.

Recommendation:

Returns the top 5-10 movies with the highest similarity scores.

🔮 Future Scope
Hybrid Filtering: Incorporate user ratings for more personalized accuracy.

Sentiment Analysis: Analyze movie reviews to determine the "mood" of a movie automatically.

Live Deployment: Host the web app on Streamlit Cloud or Heroku.

🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements.

Made with ❤️ by [Mahaveer]
