import os
import sys
from django.conf import settings

# Path where uploaded images has been stored.\
# I have used media folder for this.
path_for_image = settings.MEDIA_ROOT

def get_parent_dir(n=1):
    """ returns the n-th parent directory of the current
    working directory """
    # print(__file__)
    # print(os.path.abspath(__file__))
    current_path = os.path.dirname(os.path.abspath(__file__))
    for k in range(n):
        current_path = os.path.dirname(current_path)
    return current_path

# source is the path where I will create a folder \
# Test_Image_Detection_Results to save the results

src_path = os.path.join(get_parent_dir(1), "2_Training", "src")
utils_path = os.path.join(get_parent_dir(1), "Utils")
# appending the path to system
sys.path.append(src_path)
sys.path.append(utils_path)

# libraries are imported
from keras_yolo3.yolo import YOLO, detect_video
from timeit import default_timer as timer
from utils import load_extractor_model, load_features, parse_input, detect_object
import pandas as pd
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Set up folder names for default values
data_folder = os.path.join(get_parent_dir(n=1), "Data")
image_folder = os.path.join(data_folder, "Source_Images")
detection_results_folder = os.path.join(image_folder, "Test_Image_Detection_Results")
detection_results_file = os.path.join(detection_results_folder, "Detection_Results.csv")
model_folder = os.path.join(data_folder, "Model_Weights")
model_weights = os.path.join(model_folder, "trained_weights_final.h5")
model_classes = os.path.join(model_folder, "data_classes.txt")
anchors_path = os.path.join(src_path, "keras_yolo3", "model_data", "yolo_anchors.txt")

# saved images are those images whch are uploaded \
# by the person and is placed in the media folder
def main_detector(saved_file):
    # Split images and videos
    img_endings = (".jpg", ".jpeg", ".png")
    input_image_paths = []
    input_paths = saved_file
    input_image = os.path.join(path_for_image, input_paths)
    item = input_image
    if item.endswith(img_endings):
        input_image_paths.append(item)
    output_path = detection_results_folder
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    yolo = YOLO(
        **{
            "model_path": model_weights,
            "anchors_path": anchors_path,
            "classes_path": model_classes,
            "score": 0.25,
            "gpu_num": 1,
            "model_image_size": (416, 416),
        }
    )

    # Make a dataframe for the prediction outputs
    out_df = pd.DataFrame(
        columns=[
            "image",
            "image_path",
            "xmin",
            "ymin",
            "xmax",
            "ymax",
            "label",
            "confidence",
            "x_size",
            "y_size",
        ]
    )
    # labels to draw on images
    class_file = open(model_classes, "r")
    input_labels = [line.rstrip("\n") for line in class_file.readlines()]
    print("Found {} input labels: {} ...".format(len(input_labels), input_labels))

    if input_image_paths:
        print(
            "Found {} input images: {} ...".format(
                len(input_image_paths),
                [os.path.basename(f) for f in input_image_paths[:5]],
            )
        )
        start = timer()
        text_out = ""

        # This is for images
        for i, img_path in enumerate(input_image_paths):
            # prediction comes for the images user have uploaded
            prediction, image = detect_object(
                yolo,
                img_path,
                save_img=True,
                save_img_path=output_path,

            )
            y_size, x_size, _ = np.array(image).shape
            for single_prediction in prediction:
                # results is transformed in form of dataframe
                out_df = out_df.append(
                    pd.DataFrame(
                        [
                            [
                                os.path.basename(img_path.rstrip("\n")),
                                img_path.rstrip("\n"),
                            ]
                            + single_prediction
                            + [x_size, y_size]
                        ],
                        columns=[
                            "image",
                            "image_path",
                            "xmin",
                            "ymin",
                            "xmax",
                            "ymax",
                            "label",
                            "confidence",
                            "x_size",
                            "y_size",
                        ],
                    )
                )
        end = timer()
        print(
            "Processed {} images in {:.1f}sec - {:.1f}FPS".format(
                len(input_image_paths),
                end - start,
                len(input_image_paths) / (end - start),
            )
        )
        out_df.to_csv(detection_results_file, index=False)
    # yolo session is closed here
    yolo.close_session()
    # pandas frame which contains result is returned to the main program
    return detection_results_file
