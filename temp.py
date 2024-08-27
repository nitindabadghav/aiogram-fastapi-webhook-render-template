import os
from dotenv import load_dotenv
from services.app_logging.logger import Logger
from langchain.chains.question_answering import load_qa_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import PromptTemplate
from langchain_community.vectorstores import FAISS
import traceback


print("Initializing ..........................")
# logger = Logger().get_logger(__name__)

# load_dotenv()

GOOGLE_API_KEY = "AIzaSyBPNlxK0jsb9Et0bjViu4zOuy8d13-50P8"

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")


llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.9,
)

prompt_template = """ You are an expert in Bhavishya Maalika.
  Read the context carefully and Answer the question as detailed as possible from the provided context, make sure to provide all the details\n\n
  Context:\n {context}?\n
  Question: \n{question}\n

  Answer:
"""

prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
# logger.info(llm)
new_db = FAISS.load_local("data/faiss_index", embeddings, allow_dangerous_deserialization=True)
