# https://huggingface.co/Thouph/eva02-vit-large-448-8046

from PIL import Image
import torch
import io
import os
import json
import traceback
from torchvision.transforms import transforms

from flask import Blueprint, request
from aipi_util import error, success

model_path = os.path.join(os.path.dirname(__file__), "eva_model")

bp = Blueprint("eva", __name__)

print("Setup torch...")
device = "cuda:0" if torch.cuda.is_available() else "cpu"
print("  Device: {}".format(device))
device = torch.device(device)

print("Loading model...")
print("  Load")
model = torch.load(model_path + '/model.pth', map_location='cpu').to(device)
print("  Eval")
model.eval()
print("  Setup transform")
transform = transforms.Compose([
    transforms.Resize((448, 448)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[
        0.48145466,
        0.4578275,
        0.40821073
    ], std=[
        0.26862954,
        0.26130258,
        0.27577711
    ])
])
print("  Load tags")
with open(model_path + "/tags_8041.json", "r") as file:
    tags = json.load(file)

allowed_tags = sorted(tags)
allowed_tags.insert(0, "placeholder0")
allowed_tags.append("placeholder1")
allowed_tags.append("explicit")
allowed_tags.append("questionable")
allowed_tags.append("safe")
print("Done loading model.")

def predict(image_input: bytes, score_threshold: float):
    img = Image.open(io.BytesIO(image_input)).convert('RGB')
    tensor = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        out = model(tensor)

    probabilities = torch.nn.functional.sigmoid(out[0])
    indices = torch.where(probabilities > score_threshold)[0]
    values = probabilities[indices]

    result_threshold = dict()

    for i in range(indices.size(0)):
        result_threshold[allowed_tags[indices[i]]] = values[i].item()
        
    return result_threshold

@bp.route('/predict', methods=['POST'])
def route():
    threshold = request.args.get('threshold', type=float)

    if threshold is None:
        threshold = 0.5

    try:
        results = predict(request.data, threshold)
    except Exception as e:
        traceback.print_exc()
        return error(str(e))

    return success(results)