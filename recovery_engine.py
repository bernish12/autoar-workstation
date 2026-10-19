import os

def recover_jpegs(disk_image_path, output_dir):
    """
    A basic File Carver that searches for JPEG signatures (Magic Bytes).
    WARNING: Running this on actual physical drives like \\\\.\\PhysicalDrive0 requires Admin rights.
    For testing, you can pass a normal file or a disk image (.img).
    """
    print(f"[+] Starting scan on: {disk_image_path}")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[+] Created output directory: {output_dir}")

    # JPEG standard headers and footers
    jpeg_start = b'\xff\xd8\xff'
    jpeg_end = b'\xff\xd9'
    
    file_count = 0
    in_file = False
    current_file_data = bytearray()
    
    chunk_size = 512  # Read in small blocks (sector size)
    
    try:
        with open(disk_image_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                # Check if a new JPEG starts in this chunk
                if jpeg_start in chunk:
                    start_index = chunk.find(jpeg_start)
                    in_file = True
                    
                    # If we were already tracking a file, save it (it might be corrupted/incomplete)
                    if len(current_file_data) > 0:
                        save_file(output_dir, file_count, current_file_data)
                        file_count += 1
                        current_file_data = bytearray()
                        
                    # Start collecting new file data
                    current_file_data.extend(chunk[start_index:])
                    
                    # Check if it also ends in this same chunk
                    if jpeg_end in chunk[start_index:]:
                        end_index = chunk.find(jpeg_end, start_index) + 2
                        current_file_data = bytearray(chunk[start_index:end_index])
                        save_file(output_dir, file_count, current_file_data)
                        file_count += 1
                        in_file = False
                        current_file_data = bytearray()
                
                # If we are currently reading a JPEG file
                elif in_file:
                    if jpeg_end in chunk:
                        end_index = chunk.find(jpeg_end) + 2
                        current_file_data.extend(chunk[:end_index])
                        save_file(output_dir, file_count, current_file_data)
                        file_count += 1
                        in_file = False
                        current_file_data = bytearray()
                    else:
                        # Append the whole chunk
                        current_file_data.extend(chunk)
                        
                        # Safety break if file gets too large (e.g., false positive, cap at 10MB)
                        if len(current_file_data) > 10 * 1024 * 1024:
                            print(f"[-] File {file_count} exceeded 10MB, dropping (possible false positive).")
                            in_file = False
                            current_file_data = bytearray()
                            
    except PermissionError:
        print("[-] Error: Run terminal as Administrator to scan physical drives.")
    except Exception as e:
        print(f"[-] Error: {e}")
        
    print(f"[+] Scan Complete. Recovered {file_count} potential files.")

def save_file(output_dir, file_index, data):
    filename = os.path.join(output_dir, f"recovered_{file_index}.jpg")
    with open(filename, "wb") as out_f:
        out_f.write(data)
    print(f"[+] Recovered: {filename}")

if __name__ == "__main__":
    print("=== Antigravity File Recovery ===")
    # For testing, we can create a dummy file with hidden jpeg data, 
    # OR you can replace this with a pendrive path (e.g., '\\\\.\\E:') if running as admin.
    target_disk = input("Enter path to scan (e.g., sample.img or \\\\.\\E:): ")
    output_folder = "./Recovered_Photos"
    
    if os.path.exists(target_disk):
        recover_jpegs(target_disk, output_folder)
    else:
        print("[-] Target path does not exist. Please check the path.")
