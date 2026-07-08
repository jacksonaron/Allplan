# Allplan 3D Model Comparator

A collection of Python scripts for Allplan 2026 that detect and compare 3D elements between models.

## Available Scripts

### 1. **Color Model Comparator** ⭐ RECOMMENDED FOR YOUR USE CASE
- **Files**: `ColorModelComparator.pyd` + `ColorModelComparator.py`
- **Purpose**: Compare 3D models **by color** across **all open drawing files** in a project
- **Perfect for**: Comparing two sets of models (e.g., existing vs proposed) when they're distinguished by color and spread across multiple drawing files
- **Features**:
  - Finds all elements of a specific color across ALL open drawing files
  - Compares two color sets against each other
  - Highlights elements from first color set that are missing in the second
  - Shows distribution of models across drawing files

### 2. **Project Model Comparator**
- **Files**: `ProjectModelComparator.pyd` + `ProjectModelComparator.py`
- **Purpose**: Compare 3D elements between **two drawing files already loaded in the same project**
- **Features**:
  - Lists all open drawing files in your current project
  - Lets you select any two to compare
  - Highlights missing elements in the second drawing file

### 3. **Model Comparator (Basic)**
- **Files**: `ModelComparator.pyd` + `ModelComparator.py`
- **Purpose**: Basic comparison of 3D elements between models
- **Use case**: Simple element detection and comparison

### 4. **Model Comparator (Advanced)**
- **Files**: `ModelComparatorAdvanced.pyd` + `ModelComparatorAdvanced.py`
- **Purpose**: Advanced comparison with file selection dialogs
- **Use case**: Comparing separate model files with detailed reporting

## Which Script Should You Use?

| Your Need | Recommended Script |
|-----------|-------------------|
| Compare models by color across multiple drawing files | **Color Model Comparator** |
| Compare two drawing files in the same project | Project Model Comparator |
| Compare two separate model files | Model Comparator (Advanced) |
| Simple model comparison | Model Comparator (Basic) |

## For Your Specific Use Case

Since you want to **compare one set of models to another set, where the models are spread across several drawing files and distinguished by color**, use the **Color Model Comparator**:

### How to Use Color Model Comparator:

1. **Open your Allplan project**
2. **Load all drawing files** that contain the models you want to compare
3. **Color your models appropriately**:
   - For example: Color all "existing" models **red**
   - Color all "proposed" models **green**
4. **Run the script**: Tools → Color Model Comparator
5. **Enter the two colors** you want to compare:
   - First color: The reference set (e.g., red for existing)
   - Second color: The set to check against (e.g., green for proposed)
6. **View the results**:
   - A detailed report showing:
     - How many models of each color were found
     - How many are common to both sets
     - Which models from the first set are missing in the second
     - Distribution across drawing files
   - **Highlighted missing elements**: Red spheres with "MISSING" text at positions where models from the first color set are missing in the second

### Example Workflow:

```
Your Project:
├── Drawing File 1
│   ├── Red model A (existing)
│   ├── Red model B (existing)
│   └── Green model X (proposed)
├── Drawing File 2
│   ├── Red model C (existing)
│   └── Green model Y (proposed)
└── Drawing File 3
    ├── Red model D (existing)
    └── Green model Z (proposed)

Run Color Model Comparator:
- First color: Red (existing models)
- Second color: Green (proposed models)

Result:
- Finds all red models across all 3 drawing files
- Finds all green models across all 3 drawing files
- Compares them
- Highlights any red models that don't have corresponding green models
```

## Features (All Scripts)

- Detects all 3D elements in Allplan models/drawing files
- Compares elements between two sources
- Identifies:
  - Elements that exist in both
  - Elements that exist only in the first
  - Elements that exist only in the second
  - Geometric differences between corresponding elements
- Similarity scoring for partial matches
- Detailed reporting with export capabilities
- **Highlighting of missing elements** (Color Model Comparator and Project Model Comparator)

## Installation

1. **Copy the Scripts folder** to your Allplan Python scripts directory:
   - System-wide: `C:\ProgramData\Nemetschek\Allplan 2026\Scripts\Python\`
   - User-specific: `%APPDATA%\Nemetschek\Allplan 2026\Scripts\Python\`

2. **Folder structure** should look like:
   ```
   Scripts/
   ├── ColorModelComparator.pyd
   ├── ColorModelComparator.py
   ├── ProjectModelComparator.pyd
   ├── ProjectModelComparator.py
   ├── ModelComparator.pyd
   ├── ModelComparator.py
   ├── ModelComparatorAdvanced.pyd
   └── ModelComparatorAdvanced.py
   ```

3. **Restart Allplan** - The scripts will appear in:
   - **Menu**: Tools → [Script Name]
   - **Ribbon**: Add-ins → Model Tools → [Script Name]

## Customization

### Changing the Comparison Tolerance

Edit the `tolerance` parameter when creating the comparator:

```python
# Default tolerance is 0.001 (1mm)
comparator = ColorModelComparator(tolerance=0.01)  # 1cm tolerance
```

### Adding More Element Types

Edit the `get_all_3d_elements_by_color()` function to include additional element types:

```python
# Add more element types to this list
element_types_3d = [
    abe.EType.SmartSymbol3D,
    abe.EType.SmartPart,
    abe.EType.Extrusion,
    # Add your custom types here
    abe.EType.YourCustomType,
]
```

### Changing Highlight Appearance

Modify the `highlight_missing_elements()` method to change:
- Marker size (currently 10cm radius spheres)
- Marker color (currently red)
- Text label content
- Layer name

```python
# Change these values
self.highlight_color = abe.Color(255, 255, 0)  # Yellow instead of red
sphere_radius = 0.15  # 15cm instead of 10cm
```

## Requirements

- Allplan 2026
- Python scripting enabled in Allplan (enabled by default)
- Appropriate permissions to access the project and drawing files

## Files

- **ColorModelComparator.pyd** - Definition file for color-based comparison
- **ColorModelComparator.py** - Main script for comparing models by color
- **ProjectModelComparator.pyd** - Definition file for project comparison
- **ProjectModelComparator.py** - Main script for comparing drawing files in a project
- **ModelComparator.pyd** - Basic definition file
- **ModelComparator.py** - Basic comparison script
- **ModelComparatorAdvanced.pyd** - Advanced definition file
- **ModelComparatorAdvanced.py** - Advanced comparison script with file dialogs

## Troubleshooting

1. **Script not appearing in menu**:
   - Check that both `.pyd` and `.py` files are in the correct Scripts directory
   - Ensure the `.pyd` file has the correct XML structure
   - Restart Allplan

2. **No elements found**:
   - Make sure your models have the colors you specified
   - Check that the drawing files are open
   - Verify the models are 3D elements (not 2D)

3. **Permission errors**:
   - Make sure you have read access to the project
   - Run Allplan as administrator if needed

4. **Element detection issues**:
   - Some custom elements might not be detected
   - Add the element type to the `get_all_3d_elements_by_color()` function

## Support

For issues or questions, please refer to the Allplan Python API documentation or contact Nemetschek support.

## License

This script is provided as-is for educational and professional use.

## Version History

- **1.2** (2024-12-19): Added Color Model Comparator for comparing models by color across multiple drawing files
- **1.1** (2024-12-19): Added Project Model Comparator for comparing drawing files within a project
- **1.0** (2024-12-19): Initial release with basic and advanced model comparators
