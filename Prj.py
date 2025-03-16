import streamlit as st
import requests
from youtube_transcript_api import YouTubeTranscriptApi
import openai

# Set your OpenAI API key
openai.api_key = 'your-api-key'

def summarize_text(transcript):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Summarize the following transcript: {transcript}"}]
    )
    return response['choices'][0]['message']['content']

def main():
    st.title("YouTube Transcript Summarizer")
    url = st.text_input("Enter YouTube Video URL:")
    
    if st.button("Summarize"):
        video_id = url.split("v=")[-1]
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([entry['text'] for entry in transcript])
            summary = summarize_text(transcript_text)
            st.subheader("Summary:")
            st.write(summary)
        except Exception as e:
            st.error(f"Error: {e}")

if _name_ == "_main_":
    main()
    from flask import Flask, request, render_template_string
from youtube_transcript_api import YouTubeTranscriptApi
import openai

app = Flask(_name_)

# Set your OpenAI API key here
openai.api_key = "GOOD"

# HTML templates
login_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <title>YouTube Transcript Summarizer</title>
</head>
<body>
    <div class="container">
        <h2 class="mt-5">YouTube Transcript Summarizer</h2>
        <form action="/summarize" method="post">
            <div class="form-group">
                <label for="video_id">YouTube Video URL:</label>
                <input type="text" class="form-control" id="video_id" name="video_id" required>
            </div>
            <button type="submit" class="btn btn-primary">Get Summary</button>
        </form>
    </div>
</body>
</html>
"""

summary_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <title>Transcript Summary</title>
</head>
<body>
    <div class="container">
        <h2 class="mt-5">Transcript Summary</h2>
        <p>{{ summary }}</p>
        <a href="/" class="btn btn-secondary">Back</a>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(login_html)

@app.route('/summarize', methods=['POST'])
def summarize():
    video_url = request.form['video_id']
    video_id = extract_video_id(video_url)
    transcript = fetch_transcript(video_id)
    summary = summarize_transcript(transcript)
    return render_template_string(summary_html, summary=summary)

def extract_video_id(url):
    """
    Extract the video ID from the YouTube URL.
    """
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")

def fetch_transcript(video_id):
    """
    Fetch the transcript for a given YouTube video ID using the YouTube Transcript API.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])
    except Exception as e:
        return f"Error fetching transcript: {e}"

def summarize_transcript(transcript):
    """
    Summarize the fetched transcript using OpenAI's API.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Summarize the following text: {transcript}"}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error summarizing transcript: {e}"

if _name_ == "_main_":
    app.run(debug=True)