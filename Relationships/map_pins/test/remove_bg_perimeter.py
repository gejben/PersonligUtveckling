from PIL import Image
import os
import sys

# Increase recursion limit just in case, though using iterative approach
sys.setrecursionlimit(100000)

def remove_background_perimeter(image_path, tolerance=30):
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        width, height = img.size
        pixels = img.load()
        
        # We will use a global visited mask to avoid reprocessing
        # In this case, we can verify if pixel is (0,0,0,0) to check visited/processed
        # BUT, we need to distinguish "already transparent" from "needs processing" if we want to be strict.
        # Simpler: just check if pixel alpha is 0.
        
        # Queue for flood fill. Initialize with all border pixels.
        queue = []
        for x in range(width):
            queue.append((x, 0))
            queue.append((x, height - 1))
        for y in range(1, height - 1): # Avoid double counting corners
            queue.append((0, y))
            queue.append((width - 1, y))
            
        print(f"Processing {os.path.basename(image_path)}... Border queue size: {len(queue)}")
        
        processed_count = 0
        
        # We need a way to "flood" a specific color region starting from a border pixel.
        # But since the border might have different colors (checkerboard), we treat each border pixel 
        # as a potential seed for a flood fill of *its specific color*.
        
        # To optimize, we use a visited set so we don't re-flood the same area multiple times.
        visited = set()
        
        # We actually need a nested loop structure? 
        # No, standard BFS:
        # If we pull (x,y) from queue and it hasn't been visited:
        #   Identify its color C.
        #   Kill it (alpha=0).
        #   Mark visited.
        #   Check neighbors. 
        #     If neighbor color is similar to C, add to queue.
        #     Wait, if neighbor is NOT similar to C (e.g. checkerboard switch), we do NOT add to queue 
        #     triggered by C. 
        #     BUT, that neighbor might be on the border later in the list?
        #     Or, if it's internal, it won't be reached unless it matches C.
        
        # PROBLEM: A white square inside the board (not touching edge) next to a gray square (touching edge).
        # Gray square gets removed. It reveals the white square. The white square is NOT similar to Gray.
        # So the flood stops. The white square remains.
        # This approach only works if *all* background components touch the edge.
        # In a checkerboard, ALL squares eventually connect to the edge via diagonals or zig-zags of the same color?
        # Yes, usually checkerboard squares of the same color are connected diagonally, but standard 4-way flood fill won't jump diagonally.
        
        # FIX: We need to be aggressive.
        # If the user says "transparent background", and it's a generated icon.
        # Maybe we should flood fill *anything* that looks like a "background pattern"?
        # Hard to define.
        
        # Backtracking: The user said "it kinda destroyed the images". This usually means it ate INTO the image.
        # This implies parts of the image were similar to the background.
        
        # Let's try the Perimeter approach with 4-way connectivity.
        # It will clear all solid areas touching the border.
        # For checkerboards, it might leave "islands" if they are 4-way isolated.
        # But often checkerboards in these generators are just "noise" or slight texture.
        
        # Let's implement the Queue approach where we propagate similarity.
        # Pop (x,y). Let C = color(x,y).
        # Check neighbors. If neighbor color ~ C, add to queue.
        
        # To handle the "Checkerboard" issue where White touches Gray:
        # This algorithm won't eat the White if we start at Gray.
        # But we start at ALL border pixels. So we start at Gray AND White pixels on the edge.
        # So we run multiple flood fills.
        
        full_queue = list(set(queue)) # Unique border pixels
        
        # Implementation:
        # We can't just have one big queue, because the "reference color" changes.
        # We iterate through the border pixels. If a pixel is not yet visited/transparent:
        #   Start a new Flood Fill from this pixel using its color as target.
        
        processed_mask = set() # (x,y)
        
        for bx, by in full_queue:
            if (bx, by) in processed_mask:
                continue
                
            # Start flood fill for this connected component
            seed_color = pixels[bx, by]
            
            # If it's already transparent, skip
            if seed_color[3] == 0:
                continue
                
            # BFS for this color blob
            blob_queue = [(bx, by)]
            processed_mask.add((bx, by))
            pixels[bx, by] = (0,0,0,0)
            processed_count += 1
            
            idx = 0
            while idx < len(blob_queue):
                cx, cy = blob_queue[idx]
                idx += 1
                
                # Neighbors
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    
                    if 0 <= nx < width and 0 <= ny < height:
                        if (nx, ny) not in processed_mask:
                            n_color = pixels[nx, ny]
                            if is_similar(n_color, seed_color, tolerance):
                                pixels[nx, ny] = (0, 0, 0, 0)
                                processed_mask.add((nx, ny))
                                blob_queue.append((nx, ny))
                                processed_count += 1
                                
        img.save(image_path)
        print(f"Done. Modified {processed_count} pixels.")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def is_similar(p1, p2, tolerance):
    # p1 and p2 are tuples (R, G, B, A)
    # Ignore alpha in comparison if we assume bg is opaque, but let's be safe
    return (abs(p1[0] - p2[0]) <= tolerance and
            abs(p1[1] - p2[1]) <= tolerance and
            abs(p1[2] - p2[2]) <= tolerance)

folder_path = r"c:\Users\ga-fie\personlig\relationships\map_pins\test"

for filename in os.listdir(folder_path):
    if filename.lower().endswith(".png"):
        file_path = os.path.join(folder_path, filename)
        if filename != "remove_bg_smart.py" and filename != "remove_bg_perimeter.py":
            remove_background_perimeter(file_path)
