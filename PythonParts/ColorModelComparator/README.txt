COLOR MODEL COMPARATOR - PYTHONPART VERSION
==============================================

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


HOW TO USE:
-----------
1. Open your Allplan project
2. Load all drawing files containing your models
3. Color your models:
   - Set A models = Red (default)
   - Set B models = Green (default)
4. Double-click "Color Model Comparator" in the Library
5. A palette will appear - you can:
   - Change the colors (R,G,B values)
   - Change the color names (e.g., "Existing" vs "Proposed")
   - Adjust the tolerance
6. The comparison runs automatically and:
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
✓ Compares 3D models by color across ALL open drawing files
✓ Finds elements of first color missing in second color
✓ Highlights missing elements with red spheres and "MISSING" text
✓ Shows detailed comparison report in Python console
✓ Configurable via palette (colors, names, tolerance)
✓ Works with any color (change R,G,B values)


TROUBLESHOOTING:
---------------
If nothing happens when you double-click:
1. Make sure you copied the ENTIRE folder (all 4 files)
2. Make sure the folder is in the correct location
3. Restart Allplan
4. Check the Python console for error messages (Tools -> Python -> Python Console)
5. Make sure you have at least one drawing file open


DEFAULT SETTINGS:
----------------
- First color: Red (255,0,0) - named "Existing"
- Second color: Green (0,255,0) - named "Proposed"
- Tolerance: 0.001 meters (1mm)

You can change these in the palette that appears when you double-click.
