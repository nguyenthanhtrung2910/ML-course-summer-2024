import json
import os

def coco_to_yolo(coco_json_path, output_dir):
    # Load COCO annotations
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)
    
    # Create a dictionary to map image IDs to image dimensions
    image_info = {image['id']: (image['width'], image['height']) for image in coco_data['images']}
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process annotations
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        width, height = image_info[image_id]
        
        # Calculate YOLO format bounding box
        x, y, w, h = annotation['bbox']
        x_center = (x + w / 2) / width
        y_center = (y + h / 2) / height
        width = w / width
        height = h / height
        
        # Convert COCO category ID to YOLO class ID (assuming you map them manually or have a mapping)
        class_id = annotation['category_id']
        
        # Prepare YOLO format string
        yolo_format = f"{class_id} {x_center} {y_center} {width} {height}\n"
        
        # Write to corresponding YOLO text file
        image_filename = [img['file_name'] for img in coco_data['images'] if img['id'] == image_id][0]
        yolo_txt_path = os.path.join(output_dir, os.path.splitext(image_filename.split('/')[1])[0] + '.txt')
        
        with open(yolo_txt_path, 'a') as f:
            f.write(yolo_format)

# Example usage
coco_json_path = 'project-1-at-2024-08-29-16-09-b30e1eac/result.json'
output_dir = 'project-1-at-2024-08-29-16-09-b30e1eac/labels'

coco_to_yolo(coco_json_path, output_dir)
