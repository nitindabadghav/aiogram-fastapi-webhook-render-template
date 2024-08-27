# from main import chain, new_db
from io import BytesIO  # for image
from typing import Any

from services.app_logging.logger import Logger

logger = Logger().get_logger(__name__)
print("in helper ................................................................")

def get_response(chain, new_db,question: str) -> str:
    print(f"into get_response ...... {question}")
    try:
        docs = new_db.similarity_search(question, k=5)
        print(docs)
        print(f"Got {len(docs)} from FAISS")
        response = chain(
            {"input_documents":docs, "question": question}
            , return_only_outputs=True)
        print("---------got response----------")
        print(response['output_text'])
        return response['output_text']
    except Exception as e:
        logger.error(f"Error in get_response: {str(e)}", exc_info=True)


