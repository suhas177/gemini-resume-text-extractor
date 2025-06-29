## Convert Raw text to Formatted JSON output using Pydantic and Gemini

### 1. Pre-Requisites

#### Clone the repository

```
git clone https://github.com/suhas177/gemini-resume-text-extractor.git
```

#### Base Package

```
Python 3.12+
```

#### Environment variables required to be set (.env file)

```
GOOGLE_API_KEY='<get-api-from-the-url-given-below>'
MODEL_NAME='gemini-2.5-flash'
```

Get the Gemini API key from here: https://aistudio.google.com/apikey

### 2. Create a Virtual Environment called 'python_env' and install the dependencies 

#### For Linux

```
$ python -m venv python_env
$ source python_env\bin\activate
$ pip install -r requirements.txt
```

#### For Windows

```
> python -m venv python_env
> python_env/Scripts/activate
> pip install -r requirements.txt
```

### 3. Running the backend application

####  In the same directory run the following command


```
$ uvicorn main:app --reload
```

And now open http://localhost:8000/docs on your browser to test the API.