from typing import List

import numpy as np

from clip_embedder import ClipEmbeder

class ClipSimilarity():
    """ Class to calculate similarity between image and categories """

    def __init__(self):
        """ Load vectors for wearable_items for use to see if they are in the incoming image """
        self.embeder = ClipEmbeder()
        """ Load pretrained categories and save the """
        self.fashion_categories = wearable_items = ["dress", "t-shirt", "jeans", "sneakers", "jacket", "hat", "scarf",
                                                    "gloves", "sunglasses", "watch", "belt", "socks", "boots",
                                                    "sandals", "tie", "suit", "sweater", "cardigan", "leggings",
                                                    "swimsuit"]
        self.fashion_vectors = self.embeder.embed_texts_and_image([], self.fashion_categories)[0]

    def fashion_in_the_image(self, image: object) -> List[str]:
        """
        Calculate similarity between image and categories.
        :param image: Object, image object.
        :return: List[str], list of top categories.
        """
        _, image_vector = self.embeder.embed_texts_and_image([image], [])
        category_score = {}
        for category, category_vector in zip(self.fashion_categories, self.fashion_vectors):
            category_score[category] = \
                (np.dot(category_vector, image_vector[0])
                   / (np.linalg.norm(category_vector) * np.linalg.norm(image_vector[0])))

        return sorted(category_score, key=category_score.get, reverse=True)[:3]





