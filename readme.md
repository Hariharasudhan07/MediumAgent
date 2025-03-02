# News & Web Scraping Agent

This project consists of agents for searching news articles, scraping web data, and presenting results using Streamlit.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Hariharasudhan07/MediumAgent.git
cd MediumAgent
```

### 2. Create and Activate a Virtual Environment

#### On Windows (Command Prompt)
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

This will launch the web application in your browser.

## Project Structure
```
📂 MediumAgent
 ├️ 💜 .env               # Environment variables (add API keys here)
 ├️ 💜 app.py             # Streamlit app for displaying results
 ├️ 💜 googlesearchagent.py # Fetches top 10 news/articles using Google Search
 ├️ 💜 main.py            # Main script for running agents
 ├️ 💜 requirements.txt   # Required Python libraries
 ├️ 💜 webscrapagent.py   # Scrapes article content from URLs
```

## Configuration
- Ensure `.env` contains necessary API keys if required.
- Modify `googlesearchagent.py` and `webscrapagent.py` as needed for different search or scraping functionalities.

## Contributing
Feel free to fork and contribute to this project.

## License
This project is licensed under the MIT License.

