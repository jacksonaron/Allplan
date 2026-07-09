COLOR MODEL COMPARATOR - PYTHONPART VERSION
==============================================

INSTALLATION:
-------------
1. Copy this ENTIRE folder (ColorModelComparator) to:
   
   C:\ProgramData\Nemetschek\Allplan 2026\Lib\PythonParts\Local\ 
   
   OR (if the above doesn't exist)
   
   C:\Users\YOUR_USERNAME\Documents\Nemetschek\Allplan 2026\Usr\Local\PythonParts\ 

2. Restart Allplan 2026

3. The PythonPart will appear in:
   Library -> Private -> PythonParts -> Color Model Comparator

4. Double-click it to run!


USAGE:
------
1. Open your Allplan project
2. Load all drawing files containing your models
3. Color your models (e.g., red for existing, green for proposed)
4. Double-click "Color Model Comparator" in the Library
5. Enter the two colors to compare
6. View results and highlighted missing elements


FILES IN THIS FOLDER:
---------------------
- ColorModelComparator.pyp  (PythonPart definition)
- ColorModelComparator.py   (The actual script)
- README.txt                (This file)


FEATURES:
---------
- Compares 3D models by color across ALL open drawing files
- Finds elements of first color missing in second color
- Highlights missing elements with red spheres
- Shows detailed comparison report
- Works with any color (presets or custom R,G,B values)
