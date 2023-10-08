import os
import xml.etree.ElementTree as ET

def extract_classes_from_xmls(folder_path):
    """
    Extract all unique classes from XML files in the given folder.
    
    Parameters:
    - folder_path: path to the folder containing XML files
    
    Returns:
    Set of unique class names.
    """
    unique_classes = set()
    xml_files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]
    
    for xml_file in xml_files:
        tree = ET.parse(os.path.join(folder_path, xml_file))
        root = tree.getroot()
        for obj in root.findall(".//object"):
            class_name = obj.findtext("name")
            unique_classes.add(class_name)
    
    return unique_classes

# Extract unique classes from the XML files in the uploaded folder
unique_classes = extract_classes_from_xmls("/home/jb/Desktop/cv/multispectral-object-detection/datasets/TarDAL_ori/det/Annotation")
print(unique_classes)

def count_classes_in_xmls(folder_path):
    """
    Count the occurrences of each class in XML files in the given folder.
    
    Parameters:
    - folder_path: path to the folder containing XML files
    
    Returns:
    Dictionary with class names as keys and their counts as values.
    """
    class_counts = {}
    xml_files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]
    
    for xml_file in xml_files:
        tree = ET.parse(os.path.join(folder_path, xml_file))
        root = tree.getroot()
        for obj in root.findall(".//object"):
            class_name = obj.findtext("name")
            if class_name in class_counts:
                class_counts[class_name] += 1
            else:
                class_counts[class_name] = 1
    
    return class_counts

# Count the occurrences of each class in the XML files in the uploaded folder
class_counts = count_classes_in_xmls("/home/jb/Desktop/cv/multispectral-object-detection/datasets/TarDAL_ori/det/Annotation")
print(class_counts)