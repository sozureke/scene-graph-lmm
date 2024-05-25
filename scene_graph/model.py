import google.generativeai as genai
from google.generativeai import GenerationConfig
from collections.abc import Iterable

from enum import Enum
from .utils import Utils
import logging

class GeminiModelName(Enum):
    """Enumeration for supported Gemini model names."""
    GEMINI_PRO_VISION = 'models/gemini-pro-vision'
    GEMINI_PRO_LATEST = 'models/gemini-1.5-pro-latest'

class GenerativeModel:
    """
    A class to interact with API Gemini generative AI models.

    Attributes:
        API_KEY (str): API key for authentication.
        MODEL_NAME (GeminiModelName): The name of the Gemini model to use.
        SYSTEM_MESSAGE (str): System message or instruction for the model.
    """
    
    def __init__(self, API_KEY: str, MODEL_NAME: GeminiModelName, SYSTEM_MESSAGE: str) -> None:
        """
        Initializes the GenerativeModel with the given API key, model name, and system message.

        Args:
            API_KEY (str): API key for authentication.
            MODEL_NAME (GeminiModelName): The name of the Gemini model to use.
            SYSTEM_MESSAGE (str): System message or instruction for the model.
        """
        self.API_KEY = API_KEY
        self.MODEL_NAME = MODEL_NAME
        self.SYSTEM_MESSAGE = SYSTEM_MESSAGE
        
        self.set_api_key()
        self.model = self.initialize_model()
    
    def set_api_key(self) -> None:
        """
        Sets the API key for the generative AI model.

        Raises:
            Exception: If setting the API key fails.
        """
        try:
            genai.configure(api_key=self.API_KEY)
        except Exception as error:
            logging.error(f"Failed to set API key: {error}")
            raise
    
    def initialize_model(self) -> genai.GenerativeModel:
        """
        Initializes the generative AI model with the given model name and system message.

        Returns:
            genai.GenerativeModel: An instance of the generative AI model.

        Raises:
            Exception: If initializing the model fails.
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
        temperature: float | None = 0.7,
        top_p: float | None = 0.9,
        top_k: int | None = 50,
        response_mime_type: str | None = "application/json",
        **kwargs
    ) -> GenerationConfig:
        """
        Sets up the configuration for the generative AI model.

        Args:
            candidate_count (int | None): The number of response candidates to generate.
            max_output_tokens (int | None): Maximum number of output tokens to generate.
            stop_sequences (Iterable[str] | None): Sequences to stop generation.
            temperature (float | None): Sampling temperature.
            top_p (float | None): Top-p sampling value.
            top_k (int | None): Top-k sampling value.
            response_mime_type (str | None): The MIME type of the response.
            **kwargs: Additional configuration parameters.

        Returns:
            GenerationConfig: The configuration for the generative model.
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
    
    def prompt_preparation(self, prompt_path: str, image_path: str) -> tuple[str, str]:
        """
        Prepares the prompt and image for the generative AI model.

        Args:
            prompt_path (str): Path to the text prompt file.
            image_path (str): Path to the image file.

        Returns:
            tuple[str, str]: A tuple containing the text prompt and the image.

        Raises:
            FileNotFoundError: If the file is not found.
            Exception: If preparing the prompt and image fails.
        """
        try:
            text_prompt = Utils.read_file_content(prompt_path)
            image = genai.upload_file(path=image_path)
            return text_prompt, image
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            raise
        except Exception as e:
            logging.error(f"Failed to prepare prompt and image: {e}")
            raise
    
    def generate_response(self, prompt_path: str, image_path: str) -> str:
        """
        Generates a response from the generative AI model based on the provided prompt and image.

        Args:
            prompt_path (str): Path to the text prompt file.
            image_path (str): Path to the image file.

        Returns:
            str: The generated response from the model.

        Raises:
            Exception: If generating the response fails.
        """
        text_prompt, image = self.prompt_preparation(prompt_path, image_path)
        config = self.setup_config()
        if config:
            logging.info("Configuration file loaded successfully.")
        logging.info("[!] Generating response...")
        try:
            response = self.model.generate_content([text_prompt, image], stream=True, generation_config=config)
            response.resolve()
            
            logging.info("[!] Response generated successfully.")
            return response.text
        except Exception as error:
            logging.error(f"Failed to generate response: {error}")
            raise
