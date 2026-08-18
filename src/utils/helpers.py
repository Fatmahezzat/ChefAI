import os
import base64
from typing import Optional


def image_to_base64(
    image_path: Optional[str]
) -> Optional[str]:

    if not image_path:
        return None

    if not os.path.exists(image_path):
        return image_path

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode("utf-8")