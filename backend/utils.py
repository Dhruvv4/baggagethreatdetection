import xml.etree.ElementTree as ET, os

def fetch_images_from_dir(path: str) -> [str]:
    return [file for file in os.listdir(path) if file.endswith('jpg')]

def fetch_xml_from_dir(path: str) -> [str]:
    return [file for file in os.listdir(path) if file.endswith('xml')]

def get_file_details(filepath=None):
    result = {
        "objects": []
    }
    tree = ET.parse(filepath)
    root = tree.getroot()
    for obj_detector in root.findall('object'):
        obj_data = dict()
        for attr in obj_detector:
            if not attr.tag == "bndbox":
                obj_data[attr.tag] = attr.text
            else:
                obj_data["dimension"] = [int(c.text) for c in attr]
        result["objects"].append(obj_data)
    return result

def validator(files):
    if 0 < len(files) < 2:
        return False
    data = files["imgFile"]
    xmlData = files["xmlFile"]
    if not data.filename.endswith("jpg"):
        return False
    if not xmlData.filename.endswith("xml"):
        return False
    return True

def extract_time(datetime):
    return str(datetime.time()).split('.')[0]

if __name__ == "__main__":
    data = get_file_details("../sample_input_dataset/P00X000-2019092701422.xml")