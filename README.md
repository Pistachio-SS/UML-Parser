In terms of your task, it is fairly easy to describe. It is as follows:
1. You are provided with some XML files [1]. The XML files
represent some handwritten UML diagrams. A sample XML diagram may be found at
Kaggle [4] (see Document 6_1.xml under “images with annotations”).
2. Each XML file contains the information about the objects inside a UML diagram. A UML
diagram corresponds to a file. The filename and the path may be found in the XML
document. See Fig 1.
Fig 1. A sample XML file
3. Each diagram may contain several objects of various types (i.e. class attributes, inheritance,
association, etc.). Each diagram has a size, and each object as a boundary represented by
2
xmin, xmax, ymin, and ymax. Each object has two Boolean attributes indicating whether it is
difficult, truncated, or not.
4. Each XML contains other information that may be ignored.
Processing XML files in python is fairly straight forward. You may use XPath [2] and etree library in
python [3].
WHAT TO DO?
Write a python program to read and process the XML files in a folder.
Upon user’s action your program reads information of a diagram from an XML file and loads it into
memory.
Define appropriate classes to maintain the diagram information. You may create a class for Diagram,
and another class for DiagramObject. You may use tuples and lists to store the attributes. For example,
sizes may be stored in tuples and list of objects may be stored in a python list.
Use a dictionary to store all loaded objects. Use diagram filename (without extension) for the key.
Your program should run by providing the path to a folder which the XML files are stored, as an input
argument. The code should run from the command line using the following command:
Python3 <your_code.py> </…/test_path_to_xml_folder/>
Upon execution, the program should display a simple menu option to the user, like the following:
1. List Current Files
2. List Diagrams
3. Load File
4. Display Diagram Info
5. Search
5.1. Find by type
5.2. Find by dimension
6. Statistics
7. Exit
1) List Current Files: lists all XML files in the current directory. It is assumed that your current folder
may contain files of other types. Only display XML files.
2) List Diagrams: lists currently loaded objects in memory (the dictionary). Upon start, the list is empty.
Example 1:
0 diagrams loaded.
3
Example 2:
2 diagrams loaded: ‘Document 6_1’, ‘Document 6_2’.
3) Load File: prompts the user for the file name. Upon entering the filename, the content of the XML is
loaded into the Diagram class and added to the dictionary. Note that in case the user enters an invalid
filename or perhaps tries to load an invalid file, a proper error message must be displayed to the user.
Example 1:
Enter the filename to load: Document 6_12.TXT
Error loading file ‘Document 6_12.TXT’. Invalid filename or file not found.
Example 2:
Enter the filename to load: Document 6_1.XML
Diagram `Document 6_1’ was successfully loaded.
Note that a diagram may not be reloaded. If the user tries to load a diagram that is already loaded, the
program must prompt the user with appropriate error.
4) Display Diagram Info: upon entering the diagram name, the program displays the diagram info and
all its details. Use __str__() to implement the stringification in both Diagram and Diagram Objects.
Simply print() the Diagram object.
In addition to all attributes, make sure the area of the diagram (height * width under the size tag), the
height and width, as well as the area of each diagram object is calculated and displayed. Use
@property to implement them as readonly attributes.
For Example, the area of the diagram object in the above example is 1217628; and the height, width,
and the area of the first diagram object are: 644, 860, and 553840, respectively.
5) Search: The search menu option contains two submenus.
The first submenu lets the user to select the object type and simply lists the diagrams that contain the
type.
Example:
Enter the diagram type: class attributes
Found 2 diagram(s):
Document 6_1
Document 6_2
The second submenu lets the user to enter the dimension and properties and then lists all diagrams that
match the criteria.
Example:
Min width (enter blank for zero): 10
Max width (enter blank for max):
4
Min height (enter blank for zero): …
Max height (enter blank for max): …
Difficult (yes/no/All): …
Truncated (yes/no/All): …
Found 2 diagram(s):
Document 6_1
Document 6_2
Note that each of the above criteria is optional. Entering nothing (or blank) means the default. For
difficult and truncated attributes, the user may enter y or yes, n or no, a or all, or nothing or blank.
Ignore case in string comparison. The default is all.
Note: Since the difficult and truncated properties are defined in the object level, use the following rules
to determine whether a diagram is difficult or truncated.
A diagram is difficult if it has at least one difficulty object (having a non-zero value in the difficult tag
//object/difficult). If all objects are not difficult, the diagram is not difficult.
Similarly, a diagram is considered truncated if it has at least one truncated object (having a non-zero
value in the truncated tag //object/difficult).
6) Statistics: This may option shows the following statistics:
• Number of loaded diagrams
• Total number of total objects
• Diagram Object Types (list names)
• Minimum and Maximum heights and widths (of diagrams).
• Minimum and Maximum object areas (globally among all objects of all diagrams).
7) Exit: Asks the user to confirm the exit and exits the program. Upon entering y or yes the program
terminates successfully. Ignore case in string comparison.
Example:
Are you sure you want to quit the program (yes/No)? Y
Good bye…
