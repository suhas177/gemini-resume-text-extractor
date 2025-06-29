import os
import io
import docx
import PyPDF2
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Use the new Client from the google.generativeai library
from google import genai

# Assuming your Pydantic models are in a file named models.py
from models import ResumeData

# --- Configuration & Initialization ---
load_dotenv()

# Load environment variables
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("MODEL_NAME")

if not (api_key and model_name):
    raise ValueError(
        "GOOGLE_API_KEY or MODEL_NAME environment variable not set.")


# --- FastAPI App Initialization ---
app = FastAPI(
    title="Resume Parser API",
    description="An API to parse resume files and return structured JSON data using Gemini.",
    version="2.0.0"
)

# Set up CORS middleware to allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    # You can restrict this to your frontend's domain in production
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Helper Function for Text Extraction ---
async def extract_text_from_file(file: UploadFile) -> str:
    """Extracts raw text from PDF or DOCX files."""
    content = ""
    # Read the file content into an in-memory buffer
    file_content = file.file.read()

    if file.filename.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            for page in pdf_reader.pages:
                content += page.extract_text() or ""
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error reading PDF file: {e}")

    elif file.filename.endswith(".docx"):
        try:
            doc = docx.Document(io.BytesIO(file_content))
            for para in doc.paragraphs:
                content += para.text + "\n"
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error reading DOCX file: {e}")
    else:
        raise HTTPException(
            status_code=400, detail="Unsupported file type. Please upload a .pdf or .docx file.")

    return content


# --- API Endpoint ---
@app.post("/upload-and-parse-resume/", response_model=ResumeData)
async def parse_resume(file: UploadFile = File(...)):
    """
    Receives a resume file (.pdf or .docx), extracts the text, and uses the 
    Gemini API with a response schema to parse it into the ResumeData structure.
    """
    raw_text = await extract_text_from_file(file)

    if not raw_text.strip():
        raise HTTPException(
            status_code=400, detail="Could not extract any text from the uploaded file.")

    try:
        # --- NEW: Using the genai.Client for Structured Output ---

        # 1. Instantiate the client (it uses the configured API key)
        client = genai.Client(api_key=api_key)

        # 2. Define the prompt. It's simpler now as the schema is passed separately.
        prompt = f"""
        You are an expert resume parser. Analyze the following raw text from a resume and extract the key information.
        Your output must be a JSON object that strictly follows the provided schema.

        Raw Resume Text:
        ---
        {raw_text}
        ---
        """

        # 3. Call the API with the content and the new config object
        response = client.models.generate_content(
            model=model_name,  # The model name from your .env file
            contents=prompt,
            config={
                # Use the new 'response_mime_type' for JSON output
                "response_mime_type": "application/json",
                "response_schema": ResumeData
            },

        )

        # 4. Use the convenient `.parsed` attribute to get the validated Pydantic object
        # This replaces the manual JSON cleaning and validation.
        parsed_data = response.parsed

        if not parsed_data:
            raise HTTPException(
                status_code=500, detail="Model returned an empty response.")

        return parsed_data

    except Exception as e:
        # This will catch errors from the API call or from the file processing.
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to parse resume data. Error: {e}")
