import io

import torch
from PIL import Image
from torchvision import transforms

# adapted from https://pytorch.org/hub/pytorch_vision_deeplabv3_resnet101/


def get_segmentator():

    model = torch.hub.load(
        "pytorch/vision:v0.6.0", "deeplabv3_resnet101", pretrained=True
    )
    model.eval()

    return model


def get_segments(model, binary_image, max_size=512):

    input_image = Image.open(io.BytesIO(binary_image)).convert("RGB")
    width, height = input_image.size
    resize_factor = min(max_size / width, max_size / height)
    resized_image = input_image.resize(
        (
            int(input_image.width * resize_factor),
            int(input_image.height * resize_factor),
        )
    )

    preprocess = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )

    input_tensor = preprocess(resized_image)
    input_batch = input_tensor.unsqueeze(
        0
    )  # create a mini-batch as expected by the model

    with torch.no_grad():
        output = model(input_batch)["out"][0]

    output_predictions = output.argmax(0)

    # create a color palette, selecting a color for each class
    palette = torch.tensor([2 ** 25 - 1, 2 ** 15 - 1, 2 ** 21 - 1])
    colors = torch.as_tensor([i for i in range(21)])[:, None] * palette
    colors = (colors % 255).numpy().astype("uint8")

    # plot the semantic segmentation predictions of 21 classes in each color
    r = Image.fromarray(output_predictions.byte().cpu().numpy()).resize(
        input_image.size
    )
    r.putpalette(colors)

    return r
