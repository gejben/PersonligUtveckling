from PIL import Image
import os
import sys

# Increase recursion depth just in case for recursion-based floodfill, 
# but we will perform a stack-based floodfill to be safe.
sys.setrecursionlimit(100000)

def remove_background_flood(image_path, tolerance=30):
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        width, height = img.size
        pixels = img.load()
        
        # Get background color from top-left corner
        bg_color = pixels[0, 0]
        
        # Visited set to keep track of processed pixels
        msg = f"Processing {os.path.basename(image_path)}... BG Color: {bg_color}"
        print(msg)

        # Queue for flood fill: (x, y)
        # We start from all four corners to ensure we catch the background
        queue = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
        visited = set(queue)
        
        processed_count = 0
        
        while queue:
            x, y = queue.pop(0)
            current_color = pixels[x, y]
            
            # Check if current pixel is within tolerance of bg_color
            if is_similar(current_color, bg_color, tolerance):
                # Make transparent
                pixels[x, y] = (0, 0, 0, 0)
                processed_count += 1
                
                # Check neighbors
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    
                    if 0 <= nx < width and 0 <= ny < height:
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append((nx, ny))
                            
        img.save(image_path)
        print(f"Done. Modified {processed_count} pixels.")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def is_similar(p1, p2, tolerance):
    # p1 and p2 are tuples (R, G, B, A)
    return (abs(p1[0] - p2[0]) <= tolerance and
            abs(p1[1] - p2[1]) <= tolerance and
            abs(p1[2] - p2[2]) <= tolerance)

folder_path = r"c:\Users\ga-fie\personlig\relationships\map_pins\test"

for filename in os.listdir(folder_path):
    if filename.lower().endswith(".png"):
        file_path = os.path.join(folder_path, filename)
        # Skip the script itself if it's in there
        if filename != "remove_bg_smart.py":
            remove_background_flood(file_path)
