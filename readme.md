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

## 4.Configure API keys:**  
   - Get your **Google Gemini API Key** from [[Google AI](https://ai.google.dev/)](https://ai.google.dev/).  
   - Create a `.env` file and add the key:  
     ```
     geminiapi=your_api_key_here

## 5.Running the Application

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
- Obtain an API key from [Google Gemini](https://ai.google.dev/) and add it to your `.env` file.
- Ensure `.env.example` is committed instead of `.env` to avoid exposing sensitive API keys.
- Ensure `.env.example` is committed instead of `.env` to avoid exposing sensitive API keys.
- Modify `googlesearchagent.py` and `webscrapagent.py` as needed for different search or scraping functionalities.



## Contributing
Feel free to fork and contribute to this project.

## License
This project is licensed under the MIT License.











