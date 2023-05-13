import xml.etree.ElementTree as ET
import requests
import shutil

def get_badge():
    tree = ET.parse('coverage.xml')
    percentage = float(tree.getroot().attrib['line-rate']) * 100
    badge_url = f"https://img.shields.io/badge/coverage-{percentage}%25-green?style=for-the-badge"

    response = requests.get(badge_url, stream=True)

    if response.status_code == 200:
        with open("img/coverage.svg", "wb") as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)


if __name__ == "__main__":
    get_badge()

