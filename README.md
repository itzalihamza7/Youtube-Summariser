# YouTube Video Summarizer

A Streamlit app that summarizes YouTube videos: paste a link, and it fetches the video's transcript and asks an OpenAI model for a short summary.

## Features

- Validates YouTube links (`youtube.com/watch`, `youtu.be` and embed URLs) and extracts the video ID
- Fetches the transcript with the YouTube Transcript API
- Summarizes the transcript with OpenAI's `gpt-3.5-turbo`
- Shows clear errors for invalid links and videos without transcripts

## Tech stack

Python · Streamlit · OpenAI API · youtube-transcript-api

## Getting started

Requires Python 3.9+ and an OpenAI API key.

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
echo "OPENAI_API_KEY=your-key" > .env
cd src
streamlit run streamlit.py
```

Then open http://localhost:8501.

Summaries are capped at 150 tokens, and very long videos can exceed the model's context window.

## Project structure

```
src/streamlit.py    Streamlit interface
src/Summarizer.py   Link validation, transcript retrieval and summarization
transcript.py       Standalone example of listing and fetching transcripts
```

## Credits and license

Based on [Niez Gharbi's YouTube Summariser](https://github.com/Niez-Gharbi/Youtube-Summariser), licensed under Apache 2.0 (see [LICENSE](LICENSE)). This version replaces the original local BART model (`facebook/bart-large-cnn`) with OpenAI's chat completions API and loads the API key from `.env`.
