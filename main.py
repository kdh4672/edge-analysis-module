import argparse
import json
import os
from Decoder.CvDecoder import DecoderThread
from Detection.EventsDetector import EventDetector
from Detection.ObjectDetector import JIDetector
import time
import cv2

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--video", type=str, required=True, help="Video path")
    parser.add_argument("--event_dir", type=str, required=True, help="Event json dir")
    parser.add_argument("--fps", type=int, default=6, help="FPS of extraction frame ")
    parser.add_argument("--model_name", type=str, default="ssd-mobilenet-v2", help="Model name")
    parser.add_argument("--debug", type=bool, default=False, help="Debug")
    parser.add_argument("--display", type=bool, default=False, help="Display")
    parser.add_argument("--show_scale", type=int, default=1, help="Show scale")
    parser.add_argument("--metadata", type=str, default="", help="Ground truth file(json)")

    opt = parser.parse_known_args()[0]

    video_path = opt.video
    event_json_dir = opt.event_dir

    decoder_thread = DecoderThread(video_path, opt.fps, 0, False)
    decoder_thread.start()

    object_detector = JIDetector(opt.model_name)
    event_detector = EventDetector()

    count = 0
    cap = cv2.VideoCapture(video_path)
    total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    print("Detection Start")
    loop = True
    event_time = 0
    while loop :
        try :
            frame_info = decoder_thread.getFrameFromFQ()
            od_result = object_detector.detect(frame_info)
            start_event = time.time()
            event_result = event_detector.detect_event(od_result)
            end_event = time.time()

            event_time += (end_event - start_event)

            print("\rframe_num: {:>6}/{} \t| json_count: {:>6}/{}".format(frame_info["frame_num"], total_frame_count, count, int(total_frame_count/opt.fps)), end='')
            count+=1
            if not os.path.isdir(event_json_dir):
                os.mkdir(event_json_dir)
            with open(os.path.join(event_json_dir, "%06d.json"%(count)), "w") as json_file:
                json.dump(event_result, json_file, indent="\t")
                json_file.close()
            if count >= int(total_frame_count/opt.fps) :
                print()
                del decoder_thread
                break

        except:
            pass