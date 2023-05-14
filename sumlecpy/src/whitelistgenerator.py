#!/usr/bin/env python3
"""
Arguments:
  -dir: directory containing the input file and where the output file will be written
  -input: filename of the input transcript file (.txt)
  -output: filename of the output shortened transcript file (.txt)
  -desired_length: desired length of the output transcript file in tokens (default is 2000)

This script takes a text file and reduces it's length to a desired length, whilst losing the least amount of information possible.
It will do this by:
1. splitting the text into equal size chunks, such that each chunk is less than or equal to the desired length, and each chunk must end not cut a sentence in half.
2. for each chunk, it will ask chatgpt to shorten it to a length that is less than len(chunk)/x, where x is the number of chunks.
3. it will then combine the chunks together to form the output file.
Here's an example of how to use the chatgpt api: 
```
import openai

openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "user", "content": "Condense the given transcript of a lecture to under 1000 tokens, while preserving as much important information and key points as possible. Here's the transcript: "},
    ]
)
```
Write a python script that does what I explained above.


prompt to output shortened gradually:

Here is a python script:

```

```

Rewrite it such that the shortened text appended to the output file after each chunk is shortened.
If the file doesn't exist, create it.
"""

import openai
import os
import math
import argparse
from util.ApiHandler import call_api 
openai.api_key = "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"
prompt = '''
Generate a list of words each on a newline, such that:
    Choose the 10 most important words from the given a transcript of a lecture.
    You must only output 1 word per line.
'''

def wordArrayToString(wordArray):
    return ' '.join(wordArray)
    
    
def tokenize(string):
    return string.split(' ')

def generate_flashcards(dir, input_file, output_file, maxLlmTokens):
    input_path = os.path.join(dir, input_file)
    output_path = os.path.join(dir, output_file)

    with open(input_path, 'r') as f:
        text = f.read()
    tokens = tokenize(text)
    tokenLen = math.floor(len(tokens)/0.75)
    num_chunks = math.ceil(tokenLen/maxLlmTokens) 
    chunk_size = len(tokens)/num_chunks
    chunks = [] 
    for i in range(num_chunks-1):
        chunk = tokens[int(i*chunk_size):int((i+1)*chunk_size)]
        chunks.append(chunk)
    chunks.append(tokens[int((num_chunks-1)*chunk_size):])
    print("total length:", tokenLen)
    print("Number of chunks:", num_chunks)
    print(len(chunks))
    assert(num_chunks == len(chunks))
    if not os.path.exists(output_path):
        with open(output_path, 'w'):
            pass

    i = 1
    for chunk in chunks:
        chunkTokenLen = len(chunk)/0.75
        print(f"chunk {i}/{num_chunks}")
        print("chunk token length:", chunkTokenLen/0.75)
        # print(wordArrayToString(chunk))
        i += 1
        response = call_api(
            openai.ChatCompletion.create,
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"{prompt}\n\nHere's the transcript: \n```\n{wordArrayToString(chunk)}\n```"}
            ]
        )

        flashcards = response.choices[0].message.content
        print("\n\n")
        with open(output_path, 'a') as f:
            f.write(flashcards)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", help="directory containing the input file and where the output file will be written", required=True)
    parser.add_argument("-input", help="filename of the input transcript file (.txt)", required=True)
    parser.add_argument("-output", help="filename of the output text file", required=True)
    parser.add_argument("-maxLlmTokens", default="3000", help="maximum tokens the llm can take at once", required=False)
    args = parser.parse_args()

    generate_flashcards(args.dir, args.input, args.output, int(args.maxLlmTokens))