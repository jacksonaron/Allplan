COLOR MODEL COMPARATOR - PYTHONPART VERSION
==============================================
Uses Allplan Color IDs (1=Red, 2=Yellow, 3=Cyan, 4=Green, etc.)

EASY INSTALLATION - JUST COPY THIS FOLDER!

INSTALLATION:
-------------
1. Copy this ENTIRE folder (ColorModelComparator) to:
   
   C:\Users\YOUR_USERNAME\Documents\Nemetschek\Allplan 2026\Usr\Local\PythonParts\ 
   
   (Replace YOUR_USERNAME with your actual Windows username)

2. Restart Allplan 2026

3. The PythonPart will appear in:
   Library -> Private -> PythonParts -> Color Model Comparator

4. DOUBLE-CLICK it to run!


ALLPLAN COLOR ID REFERENCE:
---------------------------
 1 = Red
 2 = Yellow
 3 = Cyan
 4 = Green
 5 = Magenta
 6 = Blue
 7 = White
 8 = Black
 9 = Gray 1
10 = Gray 2
11 = Dark Red
12 = Dark Yellow
13 = Dark Cyan
14 = Dark Green
15 = Dark Magenta
16 = Dark Blue


HOW TO USE:
-----------
1. Open your Allplan project
2. Load all drawing files containing your models
3. Color your models using Allplan's standard colors
4. Double-click "Color Model Comparator" in the Library
5. A palette will appear with default settings:
   - Color 1 ID: 1 (Red) - named "Existing"
   - Color 2 ID: 3 (Cyan) - named "Proposed"
6. Change the color IDs if needed (use the reference above)
7. The comparison runs automatically and:
   - Finds all elements of each color across ALL open drawing files
   - Compares them
   - Highlights missing elements with red spheres
   - Shows results in the Python console


FILES IN THIS FOLDER:
---------------------
- ColorModelComparator.pyp  (PythonPart definition)
- ColorModelComparator.py   (The actual script)
- BuildingElement.py        (Required for PythonPart framework)
- README.txt                (This file)


FEATURES:
---------
✓ Uses Allplan color IDs (not RGB values)
✓ Compares 3D models by color across ALL open drawing files
✓ Finds elements of first color missing in second color
✓ Highlights missing elements with red spheres and "MISSING" text
✓ Shows detailed comparison report in Python console
✓ Configurable via palette (color IDs, names, tolerance)


TROUBLESHOOTING:
---------------
If nothing happens when you double-click:
1. Make sure you copied the ENTIRE folder (all 4 files)
2. Make sure the folder is in the correct location
3. Restart Allplan
4. Check the Python console for error messages (Tools -> Python -> Python Console)
5. Make sure you have at least one drawing file open
6. Make sure your models are colored with standard Allplan colors


DEFAULT SETTINGS:
----------------
- Color 1 ID: 1 (Red) - named "Existing"
- Color 2 ID: 3 (Cyan) - named "Proposed"
- Tolerance: 0.001 meters (1mm)

You can change these in the palette that appears when you double-click.
