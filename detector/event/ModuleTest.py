from wanderer.main import WandererEvent
import argparse
import os
import json
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Please check your model")
    parser.add_argument("--json_path", type=str, default=os.path.join(os.getcwd(), "data", "json", "sample1.json"), help="sample json file path")

    try:
        opt = parser.parse_known_args()[0]

        model = WandererEvent()
        json_path = opt.json_path
        # print(json_path)
        json_file_list = os.listdir(json_path)

        json_file_list.sort()
        # print(json_file_list)
        for json_file in json_file_list:
            json_file_path = os.path.join(json_path,json_file)
            # print(json_file_path)
            with open(json_file_path) as od_result_file:
                detection_result = json.load(od_result_file)

            print(model.inference(detection_result))

    except:
        print("")
        parser.print_help()
        sys.exit(0)