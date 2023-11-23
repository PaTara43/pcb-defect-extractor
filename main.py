import json
from ultralyticsplus import YOLO
import glob


model = YOLO('keremberke/yolov8s-pcb-defect-segmentation')


model.overrides['conf'] = 0.25  # NMS confidence threshold
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000  # maximum number of detections per image

def process_file(filepath):
    image = filepath
    results = model.predict(image)
    return {
        "names": model.names,
        "classes": results[0].boxes.cls.tolist(),
        "xyxy": results[0].boxes.xyxy.tolist(),
        "labels": [model.names[int(cls)] for cls in results[0].boxes.cls]
    }




def main():
    filepaths = glob.glob('inputs/*')
    result = process_file(filepaths[0])
    print(result)
    with open("outputs/result.json", "w") as f:
        f.write(json.dumps(result))

if __name__=='__main__':
    main()
