---
license: mit
language:
- en
datasets:
- garythung/trashnet
- Zesky665/TACO
- detection-datasets/coco
tags:
- computer-vision
- yolov8
- segmentation
---

### Model Description
[Ultralytics:](https://github.com/ultralytics/ultralytics/) YOLOv8 in PyTorch > ONNX > CoreML > TFLite]


### Installation
```
pip install ultralytics
```

### Yolov8 Inference
```python
from ultralytics import YOLO

model = YOLO('turhancan97/yolov8-segment-trash-detection')
prediction = model.predict(image, imgsz=image_size, show=False, save=False)
```