import os
# import time
import sys
sys.path.append("/opt/anaconda3/lib/python3.8/site-packages")
sys.path.append('/opt/anaconda3/bin/python')
sys.path.append('/opt/anaconda3/lib/python3.8/site-packages/h5py')
import h5py
import peakutils
import numpy as np
import glob

print("imported statements")

### ATTEMPTED TO MODIFY DAQ TO RAW
### I FORGET HOW IMPORTANT THIS WAS PROBABLY NOT VERY
### DECIDED TO UPLOAD ANYWAYS



def get_event_size(t0_file):
    with open(t0_file, "rb") as file:
        first_header = file.read(2)
        if first_header[1] == 202:
            print('This is a v2 version of Compass')
        file.close()
        
    if first_header[1] == 202:
        with open(t0_file, "rb") as file:
            first_event = file.read(27)
            # first_header_check = first_event[1]
            [num_samples] = np.frombuffer(first_event[23:27], dtype=np.uint32)
        return 25 + 2 * num_samples, True  # number of bytes / 2
        
    else: 
        with open(t0_file, "rb") as file:
            first_event = file.read(24)
            [num_samples] = np.frombuffer(first_event[20:24], dtype=np.uint32)
        return 24 + 2 * num_samples, False  # number of bytes / 2


def get_event(event_data_bytes):

    board = np.frombuffer(event_data_bytes[0:2], dtype=np.uint16)[0]
    channel = np.frombuffer(event_data_bytes[2:4], dtype=np.uint16)[0]
    timestamp = np.frombuffer(event_data_bytes[4:12], dtype=np.uint64)[0]
    energy = np.frombuffer(event_data_bytes[12:14], dtype=np.uint16)[0]
    energy_short = np.frombuffer(event_data_bytes[14:16], dtype=np.uint16)[0]
    flags = np.frombuffer(event_data_bytes[16:20], np.uint32)[0]
    num_samples = np.frombuffer(event_data_bytes[20:24], dtype=np.uint32)[0]
    waveform = np.frombuffer(event_data_bytes[24:], dtype=np.uint16)

    return _assemble_data_row(board, channel, timestamp, energy, energy_short, flags, num_samples, waveform)


def get_event_v2(event_data_bytes): 
    if len(event_data_bytes) < 4:
        print("event_data_bytes is too short")
        print(event_data_bytes)
    elif len(event_data_bytes) < 80:
        print("ran at least once")      # ^ all debugging
        print(event_data_bytes)       
    
    board = np.frombuffer(event_data_bytes[0:2], dtype=np.uint16)[0]
    channel = np.frombuffer(event_data_bytes[2:4], dtype=np.uint16)[0]
    timestamp = np.frombuffer(event_data_bytes[4:12], dtype=np.uint64)[0]
    energy = np.frombuffer(event_data_bytes[12:14], dtype=np.uint16)[0]
    energy_short = np.frombuffer(event_data_bytes[14:16], dtype=np.uint16)[0]
    flags = np.frombuffer(event_data_bytes[16:20], np.uint32)[0]
    
    # code = np.frombuffer(event_data_bytes[20:21], np.uint8)[0]
    
    num_samples = np.frombuffer(event_data_bytes[21:25], dtype=np.uint32)[0]
    waveform = np.frombuffer(event_data_bytes[25:], dtype=np.uint16)

    return _assemble_data_row(board, channel, timestamp, energy, energy_short, flags, num_samples, waveform)


def _assemble_data_row(board, channel, timestamp, energy, energy_short, flags, num_samples, waveform):
    timestamp = timestamp
    energy = energy
    energy_short = energy_short
    flags = flags
    waveform = waveform
    return [timestamp, energy, energy_short, flags], waveform


def _output_to_h5file(data_file, output_name, output_path, events, waveforms, baselines, bias):
    destination = os.path.join(output_path, "t1_"+output_name+"_"+str(bias)+".h5")
    with h5py.File(destination, "w") as output_file:
        output_file.create_dataset("/raw/timetag", data=events.T[0])
        output_file.create_dataset("/raw/energy", data=events.T[1])
        output_file.create_dataset("/raw/waveforms", data=waveforms)
        output_file.create_dataset("/raw/baselines", data=baselines)
        output_file.create_dataset("bias", data=bias)
        output_file.create_dataset("adc_to_v", data=2/(2**14))


def process_metadata(files, bias):

    for file_name in files:
        print("processing file:") 
        print(file_name)
        event_rows = []
        waveform_rows = []
        baseline_rows = []
        event_size, flag = get_event_size(file_name)

        print("event size: ", event_size)       #debugging

        without_extra_slash = os.path.normpath(file_name)
        last_part = os.path.basename(without_extra_slash)
        
        if flag:
            
            with open(file_name, "rb") as metadata_file:
                # file_header = metadata_file.read(2) # read in the header present in v2 Compass...
                event_data_bytes = metadata_file.read(event_size)

                # print("event_data_bytes: ", event_data_bytes)       #debugging 

                while len(event_data_bytes) > 4: #'event_data_bytes != b"" or'
                    # print(len(event_data_bytes))
                    event, waveform = get_event_v2(event_data_bytes)
                    baseline = peakutils.baseline(waveform, deg=2)
                    event_rows.append(event)
                    waveform_rows.append(waveform)
                    baseline_rows.append(baseline)
                    event_data_bytes = metadata_file.read(event_size)
            _output_to_h5file(file_name, last_part, "/home/foresttschirhart/Documents/LEGEND/Silicon Detector Project/processed", np.array(event_rows), np.array(waveform_rows), np.array(baseline_rows),bias)

        if not flag:

            with open(file_name, "rb") as metadata_file:
                event_data_bytes = metadata_file.read(event_size)
                while event_data_bytes != b"":
                    event, waveform = get_event(event_data_bytes)
                    baseline = peakutils.baseline(waveform, deg=2)
                    event_rows.append(event)
                    waveform_rows.append(waveform)
                    baseline_rows.append(baseline)
                    event_data_bytes = metadata_file.read(event_size)
            _output_to_h5file(file_name, last_part, "/home/foresttschirhart/Documents/LEGEND/Silicon Detector Project/processed", np.array(event_rows), np.array(waveform_rows), np.array(baseline_rows),bias)


# just need it to glob together all files in a folder, pass the folder and then take the last part for the file name so that you don't accidentally pass it a path instead of a file name

files = glob.glob("/home/foresttschirhart/Documents/LEGEND/Silicon Detector Project" + '/*.bin')
files_2 = glob.glob("/home/foresttschirhart/Documents/LEGEND/Silicon Detector Project" + '/*.BIN')

if len(files) == 0:
    files = files_2


process_metadata(files,28)
