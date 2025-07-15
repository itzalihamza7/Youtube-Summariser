import re
import os
import logging
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

# Suppress OpenAI logging
logging.getLogger("openai").setLevel(logging.ERROR)

class Summarizer:
    """
    A class for generating summaries from YouTube video transcripts using OpenAI's GPT model.

    Attributes:
    - api_key: Your OpenAI API key for authentication.

    Methods:
    - is_valid_youtube_link(link): Validates if the provided link is a valid YouTube video link.
    - extract_video_id(link): Extracts the video ID from a valid YouTube video link.
    - generate_summary(link): Generates a summary for a YouTube video given its link.
    """

    def __init__(self):
        """
        Initializes the Summarizer class by loading environment variables.
        """
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)

    @staticmethod
    def is_valid_youtube_link(link):
        """
        Validates if the provided link is a valid YouTube video link.
        """
        regex_pattern = r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([\w-]+)"
        return bool(re.match(regex_pattern, link))

    def extract_video_id(self, link):
        """
        Extracts the video ID from a valid YouTube video link.
        """
        match = re.search(r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([\w-]+)", link)
        return match.group(4) if match else None

    def generate_summary(self, link):
        """
        Generates a summary for a YouTube video given its link.
        """
        try:
            if not self.is_valid_youtube_link(link):
                raise ValueError("Invalid YouTube video link format.")

            video_id = self.extract_video_id(link)
            if not video_id:
                raise ValueError("Unable to extract video ID.")

            try:
                sub = YouTubeTranscriptApi.get_transcript(video_id)
            except Exception as e:
                return f"Error retrieving transcript: {str(e)}"

            subtitle = " ".join([x['text'] for x in sub])
            prompt = f"Summarize the following YouTube transcript:\n\n{subtitle}"

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes videos."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=150
            )

            summary = response.choices[0].message.content.strip()
            return summary

        except ValueError as ve:
            return f"Error: {str(ve)}"
        except Exception as e:
            return f"Error: {str(e)}"

