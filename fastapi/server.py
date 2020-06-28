from fastapi import FastAPI, File
import tempfile
from starlette.responses import FileResponse
from segmentation import get_segmentator, get_segments

model = get_segmentator()

app = FastAPI(title="DeepLabV3 image segmentation",
              description='''Obtain semantic segmentation maps of the image in input via DeepLabV3 implemented in PyTorch.
                           Visit this URL at port 8501 for the streamlit interface.''',
              version="0.1.0",
              )


@app.post("/segmentation")
def get_segmentation_map(file: bytes = File(...)):
    '''Get segmentation maps from image file'''
    segmented_image = get_segments(model, file)
    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".png", delete=False) as outfile:
        segmented_image.save(outfile)
        return FileResponse(outfile.name, media_type="image/png")
