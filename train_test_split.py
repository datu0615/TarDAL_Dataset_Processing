import xml.etree.ElementTree as ET
from os import listdir, makedirs
from os.path import join, exists
from sklearn.model_selection import train_test_split
import shutil

# Count the occurrences of each class in XML files
def count_classes_in_xmls(folder_path):
    class_counts = {}
    xml_files = [f for f in listdir(folder_path) if f.endswith('.xml')]
    
    for xml_file in xml_files:
        tree = ET.parse(join(folder_path, xml_file))
        root = tree.getroot()
        for obj in root.findall(".//object"):
            class_name = obj.findtext("name")
            if class_name in class_counts:
                class_counts[class_name] += 1
            else:
                class_counts[class_name] = 1
    
    return class_counts

# Split XML files into train and test sets in a balanced manner
def split_train_test_balanced_final(folder_path, default_test_size=0.2):
    xml_files = [f for f in listdir(folder_path) if f.endswith('.xml')]
    
    file_class_mapping = {}
    for xml_file in xml_files:
        tree = ET.parse(join(folder_path, xml_file))
        root = tree.getroot()
        file_labels = [obj.findtext("name") for obj in root.findall(".//object")]
        if file_labels:
            file_class_mapping[xml_file] = file_labels[0]
    
    train_files_combined = []
    test_files_combined = []
    class_counts_updated = count_classes_in_xmls(folder_path)
    for unique_class in class_counts_updated.keys():
        class_files = [f for f, c in file_class_mapping.items() if c == unique_class]
        
        if len(class_files) < 5:
            train_files = class_files
            test_files = []
        else:
            test_size = default_test_size
            train_files, test_files = train_test_split(class_files, test_size=test_size, random_state=42)
        
        train_files_combined.extend(train_files)
        test_files_combined.extend(test_files)
    
    return train_files_combined, test_files_combined

# Copy train and test XML files to separate folders
def copy_files_to_folders(src_folder, train_files, test_files):
    train_folder = join(src_folder, "train")
    test_folder = join(src_folder, "test")
    
    if not exists(train_folder):
        makedirs(train_folder)
    if not exists(test_folder):
        makedirs(test_folder)
    
    for train_file in train_files:
        shutil.copy2(join(src_folder, train_file), join(train_folder, train_file))
    
    for test_file in test_files:
        shutil.copy2(join(src_folder, test_file), join(test_folder, test_file))
    
    return train_folder, test_folder

# Execute the functions
folder_path = "/home/jb/Desktop/cv/multispectral-object-detection/datasets/TarDAL_ori/det/Annotation"
train_files, test_files = split_train_test_balanced_final(folder_path)
train_folder_path, test_folder_path = copy_files_to_folders(folder_path, train_files, test_files)
