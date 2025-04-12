## Generate a resume using mistral-small locally with ollama.
## Here is a simple example of how to use the ollama library to generate a resume using mistral-small locally.
# import ollama
from datetime import datetime
import json
import os
# import openai
import requests
import time
import random
import string
import re
import logging
import sys
import yaml
import pandas as pd
import numpy as np
import torch                
# import transformers
# import gradio as gr
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import LlamaTokenizer, LlamaForCausalLM

## Protocol:
## 1. Load the mistral-small model locally using ollama.
## 2. Define a prompt for generating a resume.
## 3. Use the model to generate a resume in .tex format.
## 4. Convert the .tex file to PDF using pdflatex.

## To generate the prompt, we use the following method:
# Among all the criteria (Name, Gender, Age, companies, associations, professional expression), chose one that we will modify betwseen resumes
# For each other criteria, we will randomly select a value from the list of values. This value will be the same for all resumes
# For the selected criteria, we will randomly select a value from the list of values. This value will be different for each resume.
# We will generate batches of resumes following the same method, for each criteria.
# The final prompt will be a combination of all the selected values.

## testing Gemma

# pip install accelerate


from vllm import LLM
from vllm.sampling_params import SamplingParams
from datetime import datetime, timedelta

SYSTEM_PROMPT = "You are a conversational agent that always answers straight to the point, always end your accurate response with an ASCII drawing of a cat."

user_prompt = "Give me 5 non-formal ways to say 'See you later' in French."

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
    {
        "role": "user",
        "content": user_prompt
    },
]
model_name = "mistralai/Mistral-Small-3.1-24B-Instruct-2503"
# note that running this model on GPU requires over 60 GB of GPU RAM
llm = LLM(model=model_name, tokenizer_mode="mistral")

sampling_params = SamplingParams(max_tokens=512, temperature=0.15)
outputs = llm.chat(messages, sampling_params=sampling_params)

print(outputs[0].outputs[0].text)
# Here are five non-formal ways to say "See you later" in French:

# 1. **À plus tard** - Until later
# 2. **À toute** - See you soon (informal)
# 3. **Salut** - Bye (can also mean hi)
# 4. **À plus** - See you later (informal)
# 5. **Ciao** - Bye (informal, borrowed from Italian)

# ```
#  /\_/\
# ( o.o )
#  > ^ <
# ```



#### à tester (source: https://docs.vllm.ai/en/latest/features/quantization/auto_awq.html)


from vllm import LLM, SamplingParams

# Sample prompts.
prompts = [
    "Hello, my name is",
    "The president of the United States is",
    "The capital of France is",
    "The future of AI is",
]
# Create a sampling params object.
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

# Create an LLM.
llm = LLM(model="TheBloke/Llama-2-7b-Chat-AWQ", quantization="AWQ")
# Generate texts from the prompts. The output is a list of RequestOutput objects
# that contain the prompt, generated text, and other information.
outputs = llm.generate(prompts, sampling_params)
# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")





