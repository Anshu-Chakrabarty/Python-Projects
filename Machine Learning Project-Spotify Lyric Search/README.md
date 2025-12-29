# Song Identification from Lyric Snippets

This project implements a TensorFlow-based text classification model
that predicts the **song title and artist** from a short snippet of lyrics.

The model was built as part of a learning exercise on NLP pipelines,
covering text preprocessing, vectorization, and neural network modeling.

---

## Approach

- Lyrics are cleaned using custom preprocessing (lowercasing, regex filtering,
  tokenization, and stop-word removal).
- A `TextVectorization` layer converts text into integer sequences.
- An embedding layer with global average pooling is used for efficient
  representation learning.
- The final classifier predicts a combined **Song – Artist** label.

During development, LSTM-based architectures were tested but were not used
in the final version due to overfitting and slower training on limited data.

---

## Dataset

A subset of a publicly available Spotify lyrics dataset was used.
For demonstration purposes, the dataset size was limited to allow
training on local hardware.

---

## Results

The model demonstrates reasonable accuracy on validation data
and can correctly identify songs when given short lyric snippets.

Example:

> Input: *"Look at her face, it's a wonderful face"*  
> Output: **Dancing Queen – ABBA**

---

## How to Run

```bash
pip install -r requirements.txt

Then run the cells one by one
Atlast, give the user input too, to test the model

