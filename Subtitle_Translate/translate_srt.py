import os
import re
from googletrans import Translator
from tqdm import tqdm
from retrying import retry
import httpcore

# Change this to your file name
file_name = 'test.srt'


src='en' # source language
dest='zh-cn' # destination language

base_name, ext = os.path.splitext(file_name)
translated_srt_file_path = f"{base_name}_translated{ext}"  



# Change the current working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"Changed working directory to: {script_dir}")

# Confirm the current working directory and check if the file exists

print(f"Current working directory: {os.getcwd()}")
if os.path.isfile(file_name):
    print(f"File '{file_name}' exists.")
else:
    print(f"File '{file_name}' does not exist. Check the path and file name.")

# Initialize the translator
translator = Translator()

# Function to translate subtitle lines using Google Translate with retry logic
@retry(stop_max_attempt_number=5, wait_fixed=2000, retry_on_exception=lambda x: isinstance(x, httpcore._exceptions.ConnectTimeout))
def translate_line(line, src=src, dest=dest):
    # Translate the line
    if len(line) == 0:
        return ''
    else:
        translated = translator.translate(line, src=src, dest=dest)
        return translated.text

# Read the original SRT content
with open(file_name, 'r', encoding='utf-8') as file:
    srt_lines = file.readlines()

# Initialize a list to hold translated lines
translated_srt_lines = []

# Translate each line with progress bar
for line in tqdm(srt_lines, desc="Translating lines", unit="line"):
    # Check if the line is a subtitle text line or a timestamp
    if re.match(r'^\d+$', line.strip()) or re.match(r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$', line.strip()):
        # timestamp
        translated_srt_lines.append(line)
    else:
        # Translate the subtitle text line
        try:
            translated_text = translate_line(line.strip())
            if translated_text != '':
                translated_srt_lines.append(translated_text + '\n\n')
        except Exception as e:
            print(f"Error translating line: {line.strip()} - {e}")
            translated_srt_lines.append(line + '\n')

# Save the translated content to a new SRT file

with open(translated_srt_file_path, 'w', encoding='utf-8') as file:
    file.writelines(translated_srt_lines)

print(f"Translated SRT file saved to: {translated_srt_file_path}")
