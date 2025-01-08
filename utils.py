from bs4 import BeautifulSoup
from collections import Counter
import pandas as pd

# soup = BeautifulSoup(open("html_snippet.html", encoding='utf-8'), "html.parser")


def simplize_html(soup: BeautifulSoup):
    
    class_counter = 1

    class_map = {}

    for element in soup.find_all(True):
        class_name = element.get('class')
        if class_name:
            class_name = ' '.join(class_name)
            if class_name not in class_map.keys():
                class_map[class_name] = class_counter
                class_counter += 1
            element['class'] = str(class_map[class_name])
            parent_ids = []
            parent = element.find_parent()
            while parent:
                parent_ids.append(parent.get('class', ''))
                parent = parent.find_parent()
            element['parent_ids'] = ' '.join(parent_ids)
        # Remove all other attributes except 'class'
        for attr in list(element.attrs):
            if attr not in ['class', 'id', 'parent_ids']:
                del element[attr]

    # store the modified html
    with open("html_snippet_modified.html", "w", encoding='utf-8') as file:
        file.write(str(soup))

    return soup

def calculate_frequency(soup: BeautifulSoup) -> Counter:
    div_classes = [element.get('parent_ids') for element in soup.find_all(True)]
    div_class_counts = Counter(div_classes)
    return div_class_counts

def get_leave_classes(df: pd.DataFrame) -> list:
    leave_classes = df['Class'].tolist().copy()
    for cls in df['Class'].tolist():
        if cls is None:
            continue

        for leave_cls in leave_classes:
            if leave_cls is None:
                continue
            if cls == leave_cls:
                continue
            if cls in leave_cls and cls in leave_classes:
                leave_classes.remove(cls)
    return leave_classes