# Paint App for Alphabet Recognition

This is a simple Paint App for alphabet recognition using a trained neural network model. The app allows you to draw letters on a canvas and recognizes single or multiple letters. It is built using Python with the help of the Tkinter library for the GUI, TensorFlow and Keras for the neural network model, and OpenCV for image processing.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Files](#files)
5. [How It Works](#how-it-works)

## Features

- Draw single or multiple letters on a canvas
- Recognize drawn letter(s) using a pre-trained neural network model
- Supports both single letter and multiple letters recognition

## Installation

1. Make sure you have Python 3.6 or higher installed on your machine.

2. Clone the repository or download the source code:

    ```
    git clone https://github.com/yourusername/paint-app-alphabet-recognition.git
    ```

3. Navigate to the project directory:

    ```
    cd paint-app-alphabet-recognition
    ```

4. Install the required libraries by running the following command in your terminal or command prompt:

    ```bash
    pip install -r requirements.txt
    ```

    Make sure you have a `requirements.txt` file in your project directory with the following content:

    ```
    tensorflow
    keras
    opencv-python
    Pillow
    scikit-image
    tkinter
    numpy
    ```

## Usage

1. Run `main.py` to start the Paint App:

    ```bash
    python main.py
    ```

2. Draw a letter or multiple letters on the canvas using the brush tools.

3. Click the "Single letter process" or "Multiple letters process" button to recognize the drawn letter(s).

4. The recognized letter(s) will be displayed on the canvas.

## Files

1. `main.py`: The main script to run the Paint App.
2. `paint_app.py`: Contains the implementation of the PaintApp class, which is responsible for the GUI and user interactions.
3. `processing.py`: Contains the implementation of AlphabetRecognition class, which processes and recognizes the drawn letter(s).
4. `emnistCNN.h5`: The pre-trained neural network model for alphabet recognition.
5. `y_label.txt`: Contains the mapping of the model's output to the corresponding letters.

## How It Works

The Paint App uses the Tkinter library to create a simple GUI where users can draw letters on a canvas. The drawn letters are processed and recognized using the AlphabetRecognition class in the `processing.py` file.

The AlphabetRecognition class uses the pre-trained `emnistCNN.h5` model to recognize the drawn letters. It preprocesses the drawn letters to fit the input requirements of the model, such as resizing, thresholding, and converting to the necessary data format.

The app offers two recognition modes: single letter recognition and multiple letters recognition. In single letter recognition mode, the app processes the entire canvas as one letter. In multiple letters recognition mode, the app segments the canvas into individual letters and processes them separately.

After processing the drawn letters, the app uses the pre-trained model to predict the letter(s) and displays the recognized letter(s) along with the confidence score for each prediction (if below the set threshold) on the canvas.