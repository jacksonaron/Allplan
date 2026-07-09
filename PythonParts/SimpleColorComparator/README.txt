SIMPLE COLOR COMPARATOR
=========================

SIMPLIFIED VERSION - No palette, no BuildingElement, just works!

INSTALLATION:
-------------
1. Copy this ENTIRE folder (SimpleColorComparator) to:
   
   C:\Users\YOUR_USERNAME\Documents\Nemetschek\Allplan 2026\Usr\Local\PythonParts\ 
   
   (Replace YOUR_USERNAME with your actual Windows username)

2. Restart Allplan 2026

3. The PythonPart will appear in:
   Library -> Private -> PythonParts -> Simple Color Comparator

4. DOUBLE-CLICK it to run!


WHAT IT DOES:
-------------
- Compares ALL RED models (color ID=1) vs ALL CYAN models (color ID=3)
- Across ALL open drawing files in your project
- Finds red models that don't have matching cyan models
- Highlights missing models with red spheres and "MISSING" text
- Shows results in the Python console


NO CONFIGURATION NEEDED:
-----------------------
This version uses HARDCODED colors:
- Color 1: RED (ID=1, RGB=255,0,0)
- Color 2: CYAN (ID=3, RGB=0,255,255)

If you need different colors, you'll need to edit the script file.


FILES IN THIS FOLDER:
---------------------
- SimpleColorComparator.pyp  (PythonPart definition)
- SimpleColorComparator.py   (The actual script)
- README.txt                (This file)


TROUBLESHOOTING:
---------------
If nothing happens when you double-click:
1. Make sure you copied BOTH files (pyp + py)
2. Make sure they're in the correct folder
3. Restart Allplan
4. Check the Python console for errors (Tools -> Python -> Python Console)
5. Make sure you have at least one drawing file open
6. Make sure you have models colored RED or CYAN


HOW TO CHANGE COLORS:
---------------------
If you need different colors, edit SimpleColorComparator.py:

Find these lines (around line 10-14):
    ALLPLAN_COLORS = {
        1: (255, 0, 0),     # Red
        3: (0, 255, 255),   # Cyan
    }

And these lines (around line 120-121):
    color_red = AllplanBaseElements.Color(255, 0, 0)    # Red = ID 1
    color_cyan = AllplanBaseElements.Color(0, 255, 255)  # Cyan = ID 3

Change the RGB values to your desired colors.
