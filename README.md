# Tshark Hex Dump to H.264 Converter

This tool is a Python utility designed to extract and reconstruct raw H.264 video streams from Wireshark/Tshark packet dumps. 

It was specifically developed to analyze video communication packets captured from VR devices (e.g., **Meta Quest 3S**) via USB/Wireless interfaces, but it can be adapted for other RTP/UDP based H.264 stream analysis.

## 📌 Background

When analyzing network traffic containing video streams, tools like Wireshark allow us to inspect packets but often export payload data as unstructured hexadecimal text strings. To visually verify the intercepted video data, these hex dumps must be:
1. Parsed and filtered for valid H.264 NAL Units (SPS, PPS, I-Frame, P-Frame).
2. Stripped of specific protocol headers (RTP/Container headers).
3. Reassembled into a raw binary `.h264` file.

## 🚀 Features

- **NAL Unit Detection**: Automatically identifies key H.264 start codes:
  - SPS (`0000000167`)
  - PPS (`0000000168`)
  - I-Frame (`0000000165`)
  - P-Frame (`0000000161`)
- **Noise Filtering**: Filters out packets that do not match the expected header structure (e.g., checking the 11th/12th bytes for specific flags).
- **Binary Reconstruction**: Converts hex strings to binary and removes trailing null padding (`0x00`).

## 📋 Prerequisites

- **Python 3.x**
- **Wireshark / USBPcap**(To capture USB packets)
- **Tshark**(to generate the input dump file)
- A media player that supports raw H.264 streams (e.g., VLC Media Player, ffplay)

## ⚙️ Usage

### 1. Prepare the Input Data

First, export the packet payload from your capture file using `tshark`. Ensure the output contains only the hexadecimal data string.

```bash
# Example command to extract payload
@echo off
setlocal enabledelayedexpansion

set TSHARK_PATH=C:\Program Files\Wireshark
set CAPTURE_FILE=D:\capture\metaCapture(USB).pcapng
set FILTER=frame contains 00:00:00:01:67 or frame contains 00:00:00:01:68 or frame contains 00:00:00:01:65 or frame contains 00:00:00:01:61
set DATA_FIELD=usb.capdata
set TXT_FILE=__tshark_output.txt

cd /d %~dp0
"%TSHARK_PATH%\tshark.exe" -r "%CAPTURE_FILE%" -Y "%FILTER%" -T fields -e %DATA_FIELD% > "%TXT_FILE%"
```
Note: The script expects the input file to be named tshark_output.txt and placed in the same directory.

### 🧪 Quick Start with Sample Data (Optional)
If you don't have your own packet dump yet, you can use the provided sample file (`sample_input.txt`) to test the script.

> **⚠️ Note**: The original raw dump was over **7GB**. This sample (`sample_input.txt`) is a trimmed version (approx. 20MB) containing only the beginning of the stream. Therefore, **the reconstructed video will only play for a few seconds.**

To use the sample:
1. Open `main.py`.
2. Modify the `INPUT_FILE` variable as follows:

```python
# --- Configuration ---
# INPUT_FILE = "tshark_output.txt"  <-- Comment out the original
INPUT_FILE = "sample_input.txt"     # <-- Change to sample file
```

### 2. Run the Script
Execute the Python script to process the text file and generate the video file.

```bash
python main.py
```

### 3. Verify the Output
The script will generate output.h264. You can play this file using ffplay (part of FFmpeg) or VLC.
![Video](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdna%2FbIaBW9%2FdJMcahpgFMq%2FAAAAAAAAAAAAAAAAAAAAAOxsYJREOeL1FZ0YcSI_iuGW8xP8PnnkM58MMu0bxZ76%2Fimg.png%3Fcredential%3DyqXZFxpELC7KVnFOS48ylbz2pIh7yKj8%26expires%3D1764514799%26allow_ip%3D%26allow_referer%3D%26signature%3DCttrI89XmXpYTSXce8t1yUd5qus%253D)

## 🔍 Code Logic
Input Reading: Reads tshark_output.txt line by line.

Header Validation: Skips packets where the 11th or 12th byte does not match the expected signature (0x01), effectively removing unrelated traffic or control packets.

Start Code Search: Scans for H.264 NAL start markers to identify the beginning of a frame.

Binary Writing: Converts the valid hex string into bytes, removes padding, and appends it to the output file.

## 📝 Reference
This project is part of a digital forensics research study on VR device communication.

Blog Post (Korean): https://ryujm1828.tistory.com/70

## 📜 License
This project is open source and available under the MIT License.
