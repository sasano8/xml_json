import os

import onnx
import requests


def download_model(model_url, output_path):
    if not os.path.exists(output_path):
        res = requests.get(model_url)
        res.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(res.content)


def summarize_model(onnx_model):
    # ONNX形式のモデルを読み込む
    # model = onnx.load(filepath)

    # モデル（グラフ）を構成するノードを全て出力する
    print("====== Nodes ======")
    for i, node in enumerate(onnx_model.graph.node):
        if i > 0:
            break
        print(f"{type(node)}")
        print(node)

    # モデルの入力データ一覧を出力する
    print("====== Inputs ======")
    for i, input in enumerate(onnx_model.graph.input):
        if i > 0:
            break
        print(f"{type(node)}")
        print(input)

    # # モデルの出力データ一覧を出力する
    print("====== Outputs ======")
    for i, output in enumerate(onnx_model.graph.output):
        if i > 0:
            break
        print(f"{type(node)}")
        print(output)


def main():
    FILENAME = "tinyyolov2-7.onnx"
    MODEL_URL = f"https://github.com/onnx/models/raw/main/vision/object_detection_segmentation/tiny-yolov2/model/{FILENAME}"
    FILEPATH = ".tmp/" + FILENAME
    if not os.path.exists(".tmp"):
        os.mkdir(".tmp")
    download_model(MODEL_URL, FILEPATH)
    model = onnx.load(FILEPATH)
    summarize_model(model)


if __name__ == "__main__":
    main()
