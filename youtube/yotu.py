import os
import pytube
from pytube import YouTube
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    # Get the YouTube video URL and selected format from the form
    video_url = request.form['url']
    download_format = request.form['format']

    # Download the video using pytube
    youtube = YouTube(video_url)
    if download_format == 'video':
        stream = youtube.streams.get_highest_resolution()
        stream.download(output_path='downloads')
        file_path = os.path.join('downloads', stream.default_filename)
    elif download_format == 'audio':
        stream = youtube.streams.get_audio_only()
        stream.download(output_path='downloads', filename_prefix='audio_')
        file_path = os.path.join('downloads', f'audio_{stream.default_filename}')

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
