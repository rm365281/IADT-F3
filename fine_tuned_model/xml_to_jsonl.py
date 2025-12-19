import os
import json
import xml.etree.ElementTree as ET

DATA_DIR = "data"
OUTPUT_FILE = "dataset/dataset_alpaca.jsonl"

def parse_xml_file(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    qapairs = []
    for qapair in root.findall(".//QAPair"):
        question = qapair.findtext("Question", "").strip()
        answer = qapair.findtext("Answer", "").strip()
        qapairs.append({
            "instruction": question,
            "input": "",
            "output": answer
        })
    return qapairs

def main():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
        for filename in os.listdir(DATA_DIR):
            if filename.endswith(".xml"):
                filepath = os.path.join(DATA_DIR, filename)
                qapairs = parse_xml_file(filepath)
                for qa in qapairs:
                    out_f.write(json.dumps(qa, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
