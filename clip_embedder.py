import os
from typing import List, Tuple
from transformers import CLIPProcessor, CLIPModel
import torch

class ClipEmbeder():
    """ Create texts and images embedding for given texts and images. """

    def __init__(self):
        """ Load the model and processor from huggingface directly """
        clip_model = os.environ.get("CLIP_MODEL") if "CLIP_MODEL" in os.environ else 'openai/clip-vit-large-patch14'
        self.model = CLIPModel.from_pretrained(clip_model)
        self.processor = CLIPProcessor.from_pretrained(clip_model)

    def embed_texts_and_image(self, images: List[object], texts: List[str]) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Takes images and texts and run them through the clip model - done separately for simplicity (maybe change later)
        :param images: List[object], List of Pil images o feed into the processor
        :param texts: List[str], List of texts to feed into the processor
        :return: Tuple[torch.Tensor, torch.Tensor], Tuple of embeddings for "texts" and "images" in this order,
                    if text or image or both not present than None it's palace will be return as None
        """
        # Generate inputs
        inputs_images = None
        inputs_texts = None
        if len(images) > 0:
            inputs_images = self.processor(images=images, return_tensors="pt", padding=True)
        if len(texts) > 0:
            inputs_texts = self.processor(text=texts, return_tensors="pt", padding=True)

        # generated embeddings
        image_embedding \
            = self.model.get_image_features(**inputs_images).detach().numpy().tolist() if inputs_images else None
        text_embedding \
            = self.model.get_text_features(**inputs_texts).detach().numpy().tolist() if inputs_texts else None

        return text_embedding, image_embedding
