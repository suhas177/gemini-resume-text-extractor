## Convert Raw text to Formatted JSON output using pydantic and Gemini

### 1. Pre-Requisites

```
Python 3.12+
```

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

### 3. Running the backend application: In the same directory run the following

```
$ uvicorn main:app --reload
```

And now open http://localhost:8000/docs on your browser to test the API.