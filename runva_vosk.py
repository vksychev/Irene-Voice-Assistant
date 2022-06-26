import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import traceback
import json

from vacore import VACore

mic_blocked = False

# ------------------- vosk ------------------
if __name__ == "__main__":
    q = queue.Queue()


    def int_or_str(text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text


    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        if not mic_blocked:
            q.put(bytes(indata))


    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        '-f', '--filename', type=str, metavar='FILENAME',
        help='audio file to store recording to')
    parser.add_argument(
        '-m', '--model', type=str, metavar='MODEL_PATH',
        help='Path to the model')
    parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='input device (numeric ID or substring)')
    parser.add_argument(
        '-r', '--samplerate', type=int, help='sampling rate')
    args = parser.parse_args(remaining)

    try:
        if args.model is None:
            args.model = "model"
        if not os.path.exists(args.model):
            print("Please download a model for your language from https://alphacephei.com/vosk/models")
            print("and unpack as 'model' in the current folder.")
            parser.exit(0)
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            args.samplerate = int(device_info['default_samplerate'])

        model = vosk.Model(args.model)

        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None

        with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device, dtype='int16',
                               channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            core = VACore()
            core.init_with_plugins()
            while True:
                print("тут1")
                data = q.get()
                print("тут2")
                if rec.AcceptWaveform(data):
                    recognized_data = rec.Result()
                    recognized_data = json.loads(recognized_data)
                    voice_input_str = recognized_data["text"]
                    print("тут3")
                    if voice_input_str != "":
                        if core.logPolicy == "all":
                            print("Input: ", voice_input_str)
                        try:
                            voice_input = voice_input_str.split(" ")
                            for ind in range(len(voice_input)):
                                callname = voice_input[ind]
                                if callname in core.voiceAssNames:  # найдено имя ассистента
                                    if core.logPolicy == "cmd":
                                        print("Input (cmd): ", voice_input_str)
                                    mic_blocked = True
                                    command_options = " ".join(
                                        [str(input_part) for input_part in voice_input[(ind + 1):len(voice_input)]])
                                    core.execute_next(command_options, None)
                                    break
                        except Exception as err:
                            print(traceback.format_exc())

                        mic_blocked = False
                core._update_timers()
                if dump_fn is not None:
                    dump_fn.write(data)
    except KeyboardInterrupt:
        print('Done')
        parser.exit(0)
    except Exception as e:
        parser.exit(1)
