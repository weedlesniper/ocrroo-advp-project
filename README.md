# Overview

This project provides an accessible learning tool designed to support students with visual impairments—specifically those who use screen readers such as JAWS—when studying software development. Traditional coding tutorial videos present a significant barrier to accessibility, as critical on-screen information is visual-only. This tool addresses that gap.

The system allows a student to pause a coding tutorial video and automatically generate screen-reader-friendly text derived from the paused frame using OCR [Optical Character Recognition](https://en.wikipedia.org/wiki/Optical_character_recognition). Code, UI elements, and on-screen actions are converted into text that can be read aloud by assistive technology.

# Contribution Guidelines.

See the [Contributions Guide](./CONTRIBUTIONS.md) for how to get involved.

# Pre-requisites
To successfully build and run the project, ensure that you have the following installed. 
### Tesseract executable 
Tesseract is an open source text recognition (OCR) Engine.
This is used to extract the text that is on screen and being played in the video.

It can be downloaded at:
- Windows - https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe

### NodeJS
Node is required to run npm and build the front end.
It can be downloaded at https://nodejs.org/en/download

###Windows users - Important Notice:
Before completing the backend installation, make sure you are using Python 3.13.x.
Using Python 3.11 or Python 3.14 can cause uv sync to fail due to numpy build issues on Windows.
You can find some more details in the .python-version file inside the backend folder.

## Installation Backend

TODO:

> expand upon installation instructions (Windows Linux (and separately) TAFE machines with their installation restrictions)

```bash
cd backend
python -m venv .venv
#make sure you've c'd into the backend/ folder otherwise, append backend on front of the following command
source .venv/Scripts/activate
pip install uv #if you dont have uv, you can check with uv --version
uv sync
uv run fastapi dev preliminary/simple_api.py
```

## Installation Front End (react)

With the backend running, open another terminal. In this second terminal, run the following commands.
```bash
    cd frontend
    npm install
    npm run dev
```

## Running the application
Now that you have 2 terminals running, one for the backend, and the other for the frontend,
in the terminal running the frontend, click on the link for the local host (eg 
http://localhost:5173/) and it will open up a tab in your default browser (eg Google Chrome)


# Windows Installation Instructions
## Installation Backend
Ensure that you have the pre-requisites highlighted above before commencing. 
The Windows installer for Tesseract can be found at https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe 
and NodeJS at https://nodejs.org/dist/v24.11.1/node-v24.11.1-x64.msi

Ensure that Tesseract is installed at the following location: C:\Program Files\Tesseract-OCR\tesseract.exe. 
Otherwise, you will need to change the value of pytesseract.pytesseract.tesseract_cmd location found library_basics.py in order to work.

Open up a terminal, and run the following commands.

```bash
cd backend
python -m venv .venv
#make sure you've c'd into the backend/ folder otherwise, append backend on front of the following command
source .venv/Scripts/activate
pip install uv #if you dont have uv, you can check with uv --version
uv sync
uv run fastapi dev preliminary/simple_api.py
```
Once you see [INFO] Application startup complete, move on to the next step.

## Installation Front End (react)

With the backend running, open another terminal. In this second terminal, run the following commands.
```bash
    cd frontend
    npm install
    npm run dev
```
You will know it is successful when you see 

Vite v7.2.1 ready in xx ms

  ➜  Local:   http://localhost:5173/

  ➜  Network: use --host to expose

  ➜  press h + enter to show help


## Running the application
Now that you have 2 terminals running, one for the backend, and the other for the frontend,
in the terminal running the frontend, click on the link for the local host (eg 
http://localhost:5173/) and it will open up a tab in your default browser (eg Google Chrome)



# Common Errors
- When you are trying to build the frontend and run into an issue where npm command not found, check to
see that NodeJS has been installed.
- When trying to build the backend, and one of the last outputs is Tessaract not found, check to see
that it has been installed (see install links) at the same location as highlighted in library_basics.py.
Issues with Tesseract can also be seen when trying to run the OCR in the application.


## Running the unit tests
We are using the unittest framework for testing.
There are a few things you need to setup in your IDE before the tests will run successfully.
 
## Using Pycharm
### Step 1 - Setting the backend as Sources Root
So that the IDE picks up the correct package, right click on the ```Backend``` folder and Mark Directory as Sources Root

### Step 2 - Use the correct interpreter
You'll notice that there are 2 venvs in this project. We need to use the one in the ```Backend``` folder instead.
If it throws an error indicating things like module cv not found, but you are able to build the project successfully, you're likely using the wrong interpreter.
Make sure that it is pointed to the ocrroo-advp-project/backend/.venv/Scripts/python.exe.

To do so
1) Click on the right hand corner of Pycharm. You should see Python 3.x (where x is the version number). Doing so should bring up a Python Interpreter list. 
2) Select Add New Interpreter -> Add Local Interpreter
3) You should see options to select Existing or New environments. Select the Radio button for Existing, and ensure you've still selected Virtualenv Environment on the left hand menu.
4) Where it asks for Interpreter, click on the menu box, navigate to the project folder, and then select the venv folder nested in the backend folder, then Scripts and finally select python.exe
5) The folder path should look like .\ocrroo-advp-project\backend\.venv\Scripts\python.exe. If so, click ok, and try running the tests.

<!-- TODO: Add steps for other IDES such as VSCode-->

