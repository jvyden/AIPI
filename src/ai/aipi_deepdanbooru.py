import io
import os

import tensorflow as tf
import deepdanbooru as dd
import numpy as np
import PIL.Image

from flask import Blueprint, request
from aipi_util import error, success
import traceback

os.environ["CUDA_VISIBLE_DEVICES"] = "-1" # disable CUDA
# os.environ["XLA_FLAGS"] = "--xla_gpu_cuda_data_dir=/opt/cuda" # fix CUDA

model_path = os.path.join(os.path.dirname(__file__), "deepdanbooru_model")

bp = Blueprint("deepdanbooru", __name__)

def load_model() -> tf.keras.Model:
    return tf.keras.models.load_model(model_path + "/model.h5")

def load_labels() -> list[str]:
    with open(model_path + "/tags.txt") as f:
        labels = [line.strip() for line in f.readlines()]
    return labels

print("Loading model...")

model = load_model()
labels = load_labels()

print("Done loading model.")

def load_image(image_input: bytes) -> PIL.Image.Image:
    width = model.input_shape[2]
    height = model.input_shape[1]

    image = dd.data.load_image_for_evaluate(io.BytesIO(image_input), width=width, height=height)
    return image

def predict(
        image: PIL.Image.Image, score_threshold: float
) -> dict[str, float]:
    _, height, width, _ = model.input_shape

    probs = model.predict(image[None, ...])[0]
    probs = probs.astype(float)

    indices = np.argsort(probs)[::-1]
    result_threshold = dict()
    for index in indices:
        label = labels[index]
        prob = probs[index]
        if prob < score_threshold:
            break
        result_threshold[label] = prob
    return result_threshold

@bp.route('/predict', methods=['POST'])
def route():
    # Get the value of 'threshold' query parameter as a float
    threshold = request.args.get('threshold', type=float)

    if threshold is None:
        threshold = 0.5

    try:
        image = load_image(request.data)
        results = predict(image, threshold)
    except Exception as e:
        traceback.print_exc()
        return error(str(e))

    return success(results)