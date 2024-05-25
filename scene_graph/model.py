import google.generativeai as genai
from google.generativeai import GenerationConfig
from collections.abc import Iterable
from typing import List, Tuple

from enum import Enum
from .utils import Utils
import logging

class GeminiModelName(Enum):
    """Enumeration for supported Gemini model names."""
    GEMINI_PRO_VISION = 'models/gemini-pro-vision'
    GEMINI_PRO_LATEST = 'models/gemini-1.5-pro-latest'

class GenerativeModel:
    """
    A class to interact with API Gemini generative AI models, providing methods for configuration, 
    prompt preparation, and response generation.

    ### Attributes:
        - API_KEY (str): API key for authentication with the Gemini API.
        - MODEL_NAME (GeminiModelName): The specific Gemini model to use for generating responses.
        - SYSTEM_MESSAGE (str): Initial system message or instruction provided to the model.
    """
    
    def __init__(self, API_KEY: str, MODEL_NAME: GeminiModelName, SYSTEM_MESSAGE: str) -> None:
        """
        Initializes the GenerativeModel with the provided API key, model name, and system message.

        ### Args:
            - API_KEY (str): The API key required for authenticating requests to the Gemini API.
            - MODEL_NAME (GeminiModelName): The specific Gemini model to use (e.g., GEMINI_PRO_VISION or GEMINI_PRO_LATEST).
            - SYSTEM_MESSAGE (str): Initial instruction or message given to the model to set the context.

        ### Raises:
            - Exception: If setting the API key or initializing the model fails.
        """
        self.API_KEY = API_KEY
        self.MODEL_NAME = MODEL_NAME
        self.SYSTEM_MESSAGE = SYSTEM_MESSAGE
        
        self.set_api_key()
        self.model = self.initialize_model()
    
    def set_api_key(self) -> None:
        """
        Configures the API key for accessing the Gemini generative AI services.

        ### Raises:
            - Exception: If the API key configuration process fails.
        """
        try:
            genai.configure(api_key=self.API_KEY)
        except Exception as error:
            logging.error(f"Failed to set API key: {error}")
            raise
    
    def initialize_model(self) -> genai.GenerativeModel:
        """
        Initializes the generative AI model with the specified model name and system message.

        ### Returns:
           - genai.GenerativeModel: An initialized instance of the specified Gemini model.

        ### Raises:
            - Exception: If there is an error during the model initialization process.
        """
        try:
            return genai.GenerativeModel(model_name=self.MODEL_NAME, system_instruction=self.SYSTEM_MESSAGE)
        except Exception as error:
            logging.error(f"Failed to initialize model: {error}")
            raise
    
    def setup_config(
        self,
        candidate_count: int | None = 1,
        max_output_tokens: int | None = 2000,
        stop_sequences: Iterable[str] | None = None,
        temperature: float | None = 0.3,
        top_p: float | None = 0.95,
        top_k: int | None = 30,
        response_mime_type: str | None = "application/json",
        **kwargs
    ) -> GenerationConfig:
        """
        Configures the generation settings for the AI model, allowing customization of various parameters.

        ### Args:
            - candidate_count (int | None): The number of response candidates to generate (default is 1).
            - max_output_tokens (int | None): The maximum number of tokens in the generated response (default is 2000).
            - stop_sequences (Iterable[str] | None): Sequences where the generation should stop (optional).
            - temperature (float | None): The sampling temperature, controlling randomness (default is 0.3).
            - top_p (float | None): The cumulative probability for nucleus sampling (default is 0.95).
            - top_k (int | None): The number of highest probability vocabulary tokens to keep for top-k filtering (default is 30).
            - response_mime_type (str | None): The MIME type of the response (default is "application/json").
            - **kwargs: Additional configuration parameters.

        ### Returns:
            - GenerationConfig: The configured generation settings for the model.
        """
        return GenerationConfig(
            candidate_count=candidate_count,
            stop_sequences=stop_sequences,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            response_mime_type=response_mime_type,
            **kwargs
        )
    
    def prompt_preparation(self, prompt_path: str, image_paths: List[str]) -> Tuple[str, List[str]]:
        """
        Prepares the text prompt and uploads the images for the generative AI model.

        ### Args:
            - prompt_path (str): The file path to the text prompt.
            - image_paths (List[str]): A list of file paths to the images.

        ### Returns:
            - Tuple[str, List[str]]: A tuple containing the text prompt and the list of uploaded image IDs.

        ### Raises:
            - FileNotFoundError: If the specified file(s) are not found.
            - Exception: If there is an error during the preparation of the prompt or image upload.
        """
        try:
            text_prompt = Utils.read_file_content(prompt_path)
            images = [genai.upload_file(path=image_path) for image_path in image_paths]
            return text_prompt, images
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            raise
        except Exception as e:
            logging.error(f"Failed to prepare prompt and images: {e}")
            raise
    
    def generate_response(self, prompt_path: str, image_paths: List[str]) -> str:
        """
        Generates a response from the generative AI model using the provided text prompt and images.

        ### Args:
            - prompt_path (str): The file path to the text prompt.
            - image_paths (List[str]): A list of file paths to the images.

        ### Returns:
            - str: The generated response from the model.

        ### Raises:
            - Exception: If there is an error during the response generation process.
        """
        text_prompt, images = self.prompt_preparation(prompt_path, image_paths)
        config = self.setup_config()
        if config:
            logging.info("Configuration file loaded successfully.")
        logging.info("[!] Generating response...")
        try:
            response = self.model.generate_content([text_prompt] + images, stream=True, generation_config=config)
            response.resolve()
            
            logging.info("[!] Response generated successfully.")
            return response.text
        except Exception as error:
            logging.error(f"Failed to generate response: {error}")
            raise
