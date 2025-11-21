import sys
import os

# --- Configuration ---
INPUT_FILE = "tshark_output.txt" # Input text file
OUTPUT_FILE = "output.h264"      # Final H.264 output filename
PADDING_BYTES = b'\x00'          # Padding bytes to remove (0x00)

# List of NAL Unit start codes (SPS, PPS, I-Frame, P-Frame, etc.)
VALID_START_MARKERS = [
    "0000000167", # SPS
    "0000000168", # PPS
    "0000000165", # I-Frame
    "0000000161", # P-Frame
]

def process_tshark_output():
    
    # 1. Path Configuration (Based on script location)
    try:
        script_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)
    except NameError:
        script_path = os.path.abspath(os.getcwd())
    
    script_dir = os.path.dirname(script_path)
    input_path = os.path.join(script_dir, INPUT_FILE)
    output_path = os.path.join(script_dir, OUTPUT_FILE)
    
    print(f"Script Directory: {script_dir}")
    print(f"Input File: {input_path}")

    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: File '{INPUT_FILE}' not found.")
        return
    
    total_bytes_written = 0
    total_packets_skipped = 0
    processed_lines = 0

    # 2. Open file I/O
    # output.h264: binary write ('wb'), tshark_output.txt: text read ('r')
    with open(output_path, 'wb') as outfile, open(input_path, 'r', encoding='utf-8') as infile:
        
        # Process line by line (use enumerate for line numbers)
        for line_num, line in enumerate(infile, 1):
            processed_lines += 1
            
            # Display progress (every 10,000 lines)
            if line_num % 10000 == 0:
                print(f"--- Processing: Line {line_num} ---")

            # Remove whitespace/newlines and convert to pure hex string
            hex_string = "".join(line.split())
            
            if not hex_string:
                # Skip empty lines
                continue
            
            if len(hex_string) >= 24:
                hex_byte_11_str = hex_string[20:22] 
                hex_byte_12_str = hex_string[22:24] 
                
                # Skip if neither the 11th byte nor the 12th byte is "01"
                if hex_byte_11_str != "01" and hex_byte_12_str != "01":
                    total_packets_skipped += 1
                    continue 

            start_indices_found = []
            for marker in VALID_START_MARKERS:
                idx = hex_string.find(marker)
                if idx != -1:
                    start_indices_found.append(idx)
            
            if not start_indices_found:
                total_packets_skipped += 1
                continue
            
            start_index = min(start_indices_found)
                
            hex_data = hex_string[start_index:]
            
            if len(hex_data) % 2 != 0:
                hex_data = hex_data[:-1]
                
            try:
                binary_data = bytes.fromhex(hex_data)
            except ValueError:
                print(f"Error: Line {line_num} contains invalid hex characters.")
                total_packets_skipped += 1
                continue
                
            # Remove 0x00 padding
            processed_data = binary_data.rstrip(PADDING_BYTES)
            
            outfile.write(processed_data)
            total_bytes_written += len(processed_data)

    print("\n--- Processing Complete ---")
    print(f"File created: '{output_path}'")
    print(f"Total lines processed: {processed_lines}")
    print(f"Generated file size: {total_bytes_written} bytes")
    print(f"Skipped packets (Filter/Error): {total_packets_skipped}")

if __name__ == "__main__":
    process_tshark_output()
