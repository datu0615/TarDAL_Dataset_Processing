import os
import shutil

def copy_matching_images(xml_folder, image_folder, destination_folder):
    # XML 파일명 목록 생성
    xml_files = [f for f in os.listdir(xml_folder) if f.endswith('.xml')]
    xml_basenames = [os.path.splitext(f)[0] for f in xml_files]

    # 이미지 파일명 목록 생성
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # 이미지 파일 중 XML 파일명과 일치하는 것만 복사
    for image_file in image_files:
        image_basename = os.path.splitext(image_file)[0]
        if image_basename in xml_basenames:
            shutil.copy(os.path.join(image_folder, image_file), os.path.join(destination_folder, image_file))

# 사용 예:
copy_matching_images("/home/jb/Desktop/cv/multispectral-object-detection/datasets/TarDAL_ori/det/Annotation/train", "/home/jb/Desktop/cv/multispectral-object-detection/datasets/TarDAL_ori/det/Ir", "/home/jb/Desktop/cv/multispectral-object-detection/datasets/TarDAL_ori/images/infrared/train")
