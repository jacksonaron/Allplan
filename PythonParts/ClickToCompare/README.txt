CLICK TO COMPARE - ABSOLUTE SIMPLEST VERSION
==============================================

THIS WILL WORK - Just 2 files, no complexity

INSTALLATION:
-------------
1. Create this folder structure:
   C:\Users\YOUR_USERNAME\Documents\Nemetschek\Allplan 2026\Usr\Local\PythonParts\ClickToCompare\ 

2. Copy these 2 files into that folder:
   - ClickToCompare.pyp
   - ClickToCompare.py

3. Restart Allplan 2026

4. Find it in: Library -> Private -> PythonParts -> Click To Compare

5. DOUBLE-CLICK it


WHAT IT DOES:
-------------
- Compares ALL RED models vs ALL CYAN models
- Across ALL open drawing files
- Finds red models that don't have cyan models at the same position
- Creates RED SPHERES at positions where red models are missing
- Prints results to Python console


REQUIREMENTS:
-------------
- At least one drawing file must be open
- You must have some models colored RED (255,0,0)
- You must have some models colored CYAN (0,255,255)


TROUBLESHOOTING:
---------------
If NOTHING happens when you double-click:

1. Check the Python console for errors:
   Tools -> Python -> Python Console

2. Make sure:
   - Both files are in the ClickToCompare folder
   - The folder is in the correct PythonParts location
   - You have at least one drawing file open
   - You have models colored RED or CYAN

3. Try this test:
   - Create a simple red sphere in your model
   - Double-click the PythonPart
   - It should find the red sphere and report it


FILES:
------
ClickToCompare.pyp  - Tells Allplan this is a PythonPart
ClickToCompare.py   - The actual script that runs

That's it! Only 2 files, no BuildingElement, no palette, no complexity.
