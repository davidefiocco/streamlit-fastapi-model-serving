from fastapi import FastAPI, File
import tempfile
from starlette.responses import FileResponse
from segmentation import get_segmentator, get_segments
import uvicorn

model = get_segmentator()

app = FastAPI(title="Deeplab image segmentation",
              description="Use Deeplabv3 implemented in PyTorch to obtain semantic segmentation maps of the image in input",
              version="0.1.0",
              )


@app.post("/segmentation")
async def get_segmentation(file: bytes = File(...)):
    segmented_image = get_segments(model, file)
    with tempfile.NamedTemporaryFile(mode="w+b", suffix=".png", delete=False) as outfile:
        segmented_image.save(outfile)
        return FileResponse(outfile.name, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
