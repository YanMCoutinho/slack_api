import sys
sys.path.append('../')
from fastapi import FastAPI, Request, Query
from flask import Flask, request, jsonify
import joblib
import gensim
import spacy
import pickle
import pandas as pd
import torch
import uvicorn
import gradio as gr
from transformers import AutoTokenizer, AutoModelForSequenceClassification

app = FastAPI()

path = '../data/GoogleNews-vectors-negative300.bin.gz.gz'
w2v = gensim.models.KeyedVectors.load_word2vec_format(path, binary=True)   
try:
    spacy.load('en_core_web_lg')
except:
    spacy.cli.download('en_core_web_lg')

def get_word_vector(word):
    """
    Transform a word into a list of components of that word vector

    Args:
        word(str): a single word
    Returns:
        if the word to vector doesnt have the word returns None
        otherwise, returns the list of components, which create a vector
        
    """
    if word in w2v:
        return w2v[word]
    else:
        return None


@app.get('/pipeline')
def pipeline(text=""):
    """
    Endpoint to process text through a pre-trained pipeline.

    This route accepts a text input either as a query parameter or as a function argument,
    and processes it using a pre-trained pipeline loaded from a pickle file. The processed
    tokens are then returned.

    Args:
        text (str): The input text to be processed. Default is an empty string.
                    If empty, the function will attempt to get the text from the 
                    query parameter 'text'.

    Returns:
        text (str): The processed tokens output by the pipeline. The type and structure 
             of the output is also a text after the process.
    """
    
    if text == "":
        text = request.args.get('text', '')

    path = '../data/pipeline.joblib'
    pipeline = joblib.load(path)
        
    tokens = pipeline.transform(text)
        
    return tokens


@app.get('/w2v')
def word2vec(tokens=""):
    """
    Endpoint to get word vectors for a list of tokens.

    This route accepts a comma-separated list of tokens either as a query parameter or 
    as a function argument and returns their corresponding word vectors.

    Args:
        tokens (str): A comma-separated string of tokens. Default is an empty string.
                      If empty, the function will attempt to get tokens from the query 
                      parameter 'tokens'.

    Returns:
        list: A list which contains the sum of all word vectors for the provided tokens.
    """
    if tokens == "":
        tokens = request.args.get('tokens', '')
        
    tokens = str(tokens).strip('[').strip(']').split(',')

    array_vectors = []
    for token in tokens:
        vector = get_word_vector(token)
        if vector is not None:
            array_vectors.append(vector.tolist())
    
    vector = [0 for i in range(0, len(array_vectors[0]))]
    
    for item in array_vectors:
        for i in range(0, len(item)):
            vector[i] += item[i]

    return vector


@app.get('/model')
def model(vectors=""):
    """
    Endpoint to return the predicted value based on the word vector

    Args:
        vectors (str): a list with the word vectors
    Returns:
        json: key "predictions" which contains the 1, 0 or -1
    """
    if vectors == "":
        vectors = request.args.get('vectors', '')

    vectors_str = str(vectors).replace(" ", '').strip('[').strip(']')
    brute_array = vectors_str.split(',')
    vectors_array = {str(i): [float(brute_array[i])] for i in range(0, len(brute_array))}
    vectors_array['id'] = [0]

    path = '../data/model.pkl'
    with open(path, 'rb') as file:
        model = pickle.load(file)
        
    data = pd.DataFrame(vectors_array)
    results = model.predict(data)
    return jsonify({"predictions": results[0]})

model_path = "../data/BERT_model_and_tokenizer.pkl"

with open(model_path, 'rb') as f:
    model, tokenizer = pickle.load(f)

model.eval()  

def classify_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = outputs.logits.argmax(-1).item()
    
    predictions = "Negative" if predictions == 0 else "Non-negative"
    
    return predictions

@app.get('/prescribe')
def prescribe(text: str = Query(...)):
    """
    Endpoint to return the predicted value based on a text

    Args:
        text (str): the text that will be prescribed
    
    Returns:
        json: key "predictions" which contains the predicted values 1 (Negative) or 0 (Non-negative)
    """

    if text == "":
        return {"error": "No text provided"}
    
    predictions = classify_sentiment(text)
    
    if predictions == "Negative":
        visual = "<div style='display: flex; justify-content: center; text-align: center;; height: 100%;'><span style='color:red; font-size: 30px;'> &#9888; ATTENTION &#9888; <br> The sentence has been classified as negative. <br> Please review it carefully! </span></div>"
    else:
        visual = "<div style='display: flex; justify-content: center; text-align: center;; height: 100%;'><span style='color:green; font-size: 30px;'>All good! &#11088; <br> The sentence is considered non-negative.</span></div>"
    
    return predictions, visual


with gr.Blocks() as io:
    gr.Markdown("<h1 style='text-align: center;'>Emotion</h1>")
    gr.Markdown("<h3 style='text-align: center;'>BERT - Sentiment Classifier</h3>")

    with gr.Row():
        text_input = gr.Textbox(label="Enter text to classify its sentiment here:")

    with gr.Column():
        sentiment_label = gr.Label(label="The text is...")
        html_output = gr.HTML()

    text_input.change(fn=prescribe, inputs=text_input, outputs=[sentiment_label, html_output])

app = gr.mount_gradio_app(app, io, path="/interface")

if __name__ == '__main__':
    uvicorn.run(app, debug=True)  
