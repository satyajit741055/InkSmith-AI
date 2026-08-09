from huggingface_hub import InferenceClient
from app.config import settings
import io
from openai import OpenAI
import base64


def _generate_hf_image_bytes(prompt: str) -> bytes:
    client = InferenceClient(
                    api_key=settings.HF_API_KEY
                )

    try:
        image = client.text_to_image(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-dev",
        )

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()


    except Exception as e:
        raise RuntimeError(f"Image generation failed: {e}") from e



def _generate_openai_image_bytes(prompt:str,quality:str,size:str):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        result = client.images.generate(
                                model="gpt-image-2",
                                prompt=prompt,
                                size=size,  
                                quality=quality
                            )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        return image_bytes
    except Exception as e:
            raise RuntimeError(f"Image generation failed: {e}") from e

