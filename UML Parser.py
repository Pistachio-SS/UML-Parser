import os
import sys
import xml.etree.ElementTree as ET

class DiagramObject:
    def __init__(self, obj_type, xmin, ymin, xmax, ymax, difficult=False, truncated=False):
        self.obj_type = obj_type
        self.xmin = int(xmin)
        self.ymin = int(ymin)
        self.xmax = int(xmax)
        self.ymax = int(ymax)
        self.difficult = difficult
        self.truncated = truncated

    @property
    def width(self):
        return self.xmax - self.xmin

    @property
    def height(self):
        return self.ymax - self.ymin

    @property
    def area(self):
        return self.width * self.height

    def __str__(self):
        return (f"Type: {self.obj_type}, Bounds: ({self.xmin},{self.ymin}) to ({self.xmax},{self.ymax}), "
                f"Width: {self.width}, Height: {self.height}, Area: {self.area}, "
                f"Difficult: {self.difficult}, Truncated: {self.truncated}")

class Diagram:
    def __init__(self, filename, width, height):
        self.filename = filename
        self.size = (int(width), int(height))
        self.objects = []

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    @property
    def area(self):
        return self.width * self.height

    def add_object(self, obj):
        self.objects.append(obj)

    def __str__(self):
        info = f"Diagram: {self.filename}\nSize: {self.width}x{self.height} (Area: {self.area})\nObjects:\n"
        if not self.objects:
            info += "  (No objects found in this diagram)"
        else:
            info += "\n".join(str(obj) for obj in self.objects)
        return info


def list_current_files(folder_path):
    try:
        files = os.listdir(folder_path)
        xml_files = [f for f in files if f.lower().endswith('.xml')]

        if not xml_files:
            print("No XML files found in the folder.")
        else:
            print("XML Files found:")
            for file in xml_files:
                print(f"- {file}")
    except FileNotFoundError:
        print("Error: Folder not found.")
    except Exception as e:
        print(f"An error occurred while listing fiels: {e}")

def list_loaded_diagrams(diagram_dict):
    if not diagram_dict:
        print("0 diagrams loaded.")
    else:
        diagram_names = list(diagram_dict.keys())
        print(f"{len(diagram_names)} diagram(s) loaded: {', '.join(diagram_names)}")

def parse_xml_file(filepath):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        filename = os.path.splitext(os.path.basename(filepath))[0]

        size_elem = root.find("size")
        width = size_elem.find("width").text
        height = size_elem.find("height").text
        diagram = Diagram(filename, width, height)

        object_list = root.find("objects")
        if object_list is None:
            print("No <objects> section found.")
            return diagram

        for obj in object_list.findall("object"):
            obj_type_elem = obj.find("type")
            boundary_elem = obj.find("boundary")

            if obj_type_elem is None or boundary_elem is None:
                print("Skipping object: missing <type> or <boundary>")
                continue

            obj_type = obj_type_elem.text
            try:
                xmin = boundary_elem.get("xmin")
                xmax = boundary_elem.get("xmax")
                ymin = boundary_elem.get("ymin")
                ymax = boundary_elem.get("ymax")

                difficult = obj.find("difficult")
                truncated = obj.find("truncated")

                difficult_val = difficult.text.strip().lower() == "true" if difficult is not None else False
                truncated_val = truncated.text.strip().lower() == "true" if truncated is not None else False

                new_obj = DiagramObject(obj_type, xmin, ymin, xmax, ymax, difficult_val, truncated_val)
                diagram.add_object(new_obj)

            except Exception as e:
                print(f"Skipping malformed object: {e}")

        return diagram

    except Exception as e:
        print(f"Failed to load diagram: {e}")
        return None

def search_by_type(diagram_dict):
    search_type = input("Enter the diagram type: ").strip().lower()
    if not search_type:
        print("No type entered.")
        return

    matches = []
    for name, diagram in diagram_dict.items():
        for obj in diagram.objects:
            if obj.obj_type.lower() == search_type:
                matches.append(name)
                break

    if matches:
        print(f"Found {len(matches)} diagram(s):")
        for name in matches:
            print(name)
    else:
        print("No diagrams found with that type.")

def parse_bool_filter(value):
    if not value or value.strip().lower() in ("a", "all", ""):
        return None
    elif value.strip().lower() in ("y", "yes", "true"):
        return True
    elif value.strip().lower() in ("n", "no", "false"):
        return False
    else:
        return None

def search_by_dimension(diagram_dict):
    print("Enter search criteria (press Enter to skip a field):")

    try:
        min_w = int(input("Min width: ") or 0)
        max_w = input("Max width: ")
        max_w = int(max_w) if max_w else float('inf')

        min_h = int(input("Min height: ") or 0)
        max_h = input("Max height: ")
        max_h = int(max_h) if max_h else float('inf')

        difficult_filter = parse_bool_filter(input("Difficult (yes/no/all): "))
        truncated_filter = parse_bool_filter(input("Truncated (yes/no/all): "))

        matches = []

        for name, diagram in diagram_dict.items():
            for obj in diagram.objects:
                if (min_w <= obj.width <= max_w and
                    min_h <= obj.height <= max_h and
                    (difficult_filter is None or obj.difficult == difficult_filter) and
                    (truncated_filter is None or obj.truncated == truncated_filter)):
                    matches.append(name)
                    break

        if matches:
            print(f"Found {len(matches)} diagram(s):")
            for name in matches:
                print(name)
        else:
            print("No diagrams found matching the criteria.")

    except ValueError:
        print("Invalid numeric input.")

def show_statistics(diagram_dict):
    if not diagram_dict:
        print("No diagrams loaded.")
        return

    total_diagrams = len(diagram_dict)
    total_objects = 0
    object_types = set()
    diagram_widths = []
    diagram_heights = []
    object_areas = []

    for diagram in diagram_dict.values():
        diagram_widths.append(diagram.width)
        diagram_heights.append(diagram.height)
        for obj in diagram.objects:
            total_objects += 1
            object_types.add(obj.obj_type)
            object_areas.append(obj.area)

    print("--- Statistics ---")
    print(f"Number of loaded diagrams: {total_diagrams}")
    print(f"Total number of objects: {total_objects}")
    print(f"Diagram object types: {', '.join(sorted(object_types)) if object_types else 'None'}")
    if diagram_widths:
        print(f"Minimum diagram width: {min(diagram_widths)}")
        print(f"Maximum diagram width: {max(diagram_widths)}")
    if diagram_heights:
        print(f"Minimum diagram height: {min(diagram_heights)}")
        print(f"Maximum diagram height: {max(diagram_heights)}")
    if object_areas:
        print(f"Minimum object area: {min(object_areas)}")
        print(f"Maximum object area: {max(object_areas)}")


def main_menu():
    print("""\n\n
-------------------------------------
1. List Current Files
2. List Diagrams
3. Load File
4. Display Diagram Info
5. Search
  5.1. Find by type
  5.2. Find by dimension
6. Statistics
7. Exit
""")



def main(folder_path):
    diagrams = {}  

    print("Ready to process diagrams from:", folder_path)

    while True:
        main_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            list_current_files(folder_path)

        elif choice == "2":
            list_loaded_diagrams(diagrams)

        elif choice == "3":
            fname = input("Enter the filename to load: ").strip()
            if not fname.lower().endswith('.xml'):
                print(f"Error loading file '{fname}'. Invalid filename or file not found.")
                continue

            filepath = os.path.join(folder_path, fname)
            diagram_key = os.path.splitext(fname)[0]

            if diagram_key in diagrams:
                print(f"Diagram `{diagram_key}` is already loaded.")
                continue

            if not os.path.exists(filepath):
                print(f"Error loading file '{fname}'. Invalid filename or file not found.")
                continue

            diagram = parse_xml_file(filepath)
            if diagram:
                diagrams[diagram_key] = diagram
                print(f"Diagram `{diagram_key}` was successfully loaded.")
            else:
                print(f"Error loading diagram `{diagram_key}`.")

        elif choice == "4":
            dname = input("Enter diagram name: ").strip()
            dname_key = os.path.splitext(dname)[0]
            diagram = diagrams.get(dname_key)
            if diagram:
                print(diagram)
            else:
                print(f"Diagram '{dname}' not found or not loaded yet.")

        elif choice == "5" or choice == "5.1":
            search_by_type(diagrams)

        elif choice == "5.2":
            search_by_dimension(diagrams)

        elif choice == "6":
            show_statistics(diagrams)

        elif choice == "7":
            confirm = input("Are you sure you want to quit the program (Yes/No)? ").strip().lower()
            if confirm in ("yes", "y"):
                print("Good bye…")
                break
            else:
                continue

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python uml_parser.py </path/to/xml_folder>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a valid folder.")
        sys.exit(1)

    main(path)
