# Word Cloud Generator (web application)

## Introduction

This is a web application that allows users to generate word cloud.

The application is mainly built by Flask (python), Bootstrap library and some jQuery.

It generates word cloud mainly by [wordcloud](https://github.com/amueller/word_cloud).

Users can upload text from docx/pdf/txt files in English/Chinese/Japanese.

Python library Jieba and Mecab are used to detect the words in Chinese and Japanese respectively.

Users can either generate the word cloud with or without a shape.

## Editing and Setup

1. Start by editing app.py and generate.py by filling in the #TODO for the path (for font selection and storage path).

2. As this application is developed using Flask, a virtual environment is needed to run this application.

Please refer to [venv](https://docs.python.org/3/library/venv.html) on installing and activating virtual environment.

3. Run `pip install -r requirements.txt` to install dependencies under virtual environment

4. Run `flask run` under virtual environment

5. Navigate to http://localhost:5000/ in your browser

## Usage

Just follow the instructions on the webpage once you host the web application:)
