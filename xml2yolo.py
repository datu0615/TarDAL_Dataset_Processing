import os
import xml.etree.ElementTree as ET

def convert_xml_to_yolo(xml_path, class_mapping):
    """
    Convert VOC XML format to YOLO format.
    
    Parameters:
    - xml_path: Path to the XML file.
    - class_mapping: A dictionary mapping class names to class IDs.
    
    Returns:
    - A list of annotations in YOLO format.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Get the size of the image
    size = root.find('size')
    img_width = float(size.find('width').text)
    img_height = float(size.find('height').text)

    yolo_annotations = []

    for obj in root.findall('object'):
        class_name = obj.find('name').text
        if class_name not in class_mapping:
            print(f"Warning: {class_name} not found in class mapping.")
            continue
        
        class_id = class_mapping[class_name]

        # Get the bounding box coordinates
        bndbox = obj.find('bndbox')
        xmin = float(bndbox.find('xmin').text)
        ymin = float(bndbox.find('ymin').text)
        xmax = float(bndbox.find('xmax').text)
        ymax = float(bndbox.find('ymax').text)

        # Convert VOC format (top-left, bottom-right) to YOLO format (center, width, height)
        x_center = (xmin + xmax) / (2 * img_width)
        y_center = (ymin + ymax) / (2 * img_height)
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height

        yolo_annotation = f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        yolo_annotations.append(yolo_annotation)
    
    return yolo_annotations

def save_yolo_annotations_to_txt(output_folder, yolo_outputs):
    """
    Save YOLO annotations to .txt files.
    
    Parameters:
    - output_folder: Directory to save the .txt files.
    - yolo_outputs: Dictionary with XML file paths as keys and YOLO annotations as values.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for xml_path, annotations in yolo_outputs.items():
        txt_filename = os.path.basename(xml_path).replace(".xml", ".txt")
        txt_path = os.path.join(output_folder, txt_filename)
        
        with open(txt_path, 'w') as f:
            for annotation in annotations:
                f.write(annotation + "\n")

# Define class mapping
class_mapping = {
    "Car": 0,
    "Lamp": 1,
    "Truck": 2,
    "People": 3,
    "Bus": 4,
    "Motorcycle": 5
}

# Convert XML files to YOLO format
path = '/home/jb/Desktop/cv/multispectral-object-detection/datasets/TarDAL_ori/det/Annotation/test/'
xml_files = os.listdir('/home/jb/Desktop/cv/multispectral-object-detection/datasets/TarDAL_ori/det/Annotation/test')
yolo_outputs = {}
for xml_file in xml_files:
    xml_file = path + xml_file
    yolo_outputs[xml_file] = convert_xml_to_yolo(xml_file, class_mapping)

# Save YOLO annotations to .txt files
output_folder = "/home/jb/Desktop/cv/multispectral-object-detection/datasets/TarDAL_ori/labels/visible/test"
save_yolo_annotations_to_txt(output_folder, yolo_outputs)
