# Allplan 3D Model Comparator

A collection of Python scripts for Allplan 2026 that detect and compare 3D elements between models.

## Available Scripts

### 1. **Project Model Comparator** ⭐ RECOMMENDED FOR YOUR USE CASE
- **Files**: `ProjectModelComparator.pyd` + `ProjectModelComparator.py`
- **Purpose**: Compare 3D elements between **two drawing files already loaded in the same Allplan project**
- **Perfect for**: Comparing two parts/drawing files within one project

### 2. **Model Comparator (Basic)**
- **Files**: `ModelComparator.pyd` + `ModelComparator.py`
- **Purpose**: Basic comparison of 3D elements between models
- **Use case**: Simple element detection and comparison

### 3. **Model Comparator (Advanced)**
- **Files**: `ModelComparatorAdvanced.pyd` + `ModelComparatorAdvanced.py`
- **Purpose**: Advanced comparison with file selection dialogs
- **Use case**: Comparing separate model files with detailed reporting

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

## Installation

1. **Copy the Scripts folder** to your Allplan Python scripts directory:
   - System-wide: `C:\ProgramData\Nemetschek\Allplan 2026\Scripts\Python\`
   - User-specific: `%APPDATA%\Nemetschek\Allplan 2026\Scripts\Python\`

2. **Folder structure** should look like:
   ```
   Scripts/
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

## For Your Specific Use Case

Since you want to **compare two drawing files already loaded in the same project**, use the **Project Model Comparator**:

### How to Use Project Model Comparator:

1. **Open your Allplan project**
2. **Load both drawing files** (parts) that you want to compare
   - Make sure both are open in the project
3. **Run the script**: Tools → Project Model Comparator
4. **Select the two drawing files** from the list shown
5. **View the comparison results**

### What It Does:
- Lists all open drawing files in your current project
- Lets you select any two to compare
- Compares all 3D elements between them
- Shows you:
  - How many elements are in each drawing file
  - How many elements are common to both
  - Which elements are only in the first drawing
  - Which elements are only in the second drawing
  - Geometric differences between similar elements
- Option to export a detailed report to a text file

## Customization

### Changing the Comparison Tolerance

Edit the `tolerance` parameter when creating the comparator:

```python
# Default tolerance is 0.001 (1mm)
comparator = ProjectModelComparator(tolerance=0.01)  # 1cm tolerance
```

### Adding More Element Types

Edit the `get_all_3d_elements()` function to include additional element types:

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

### Advanced Geometric Comparison

For more accurate geometric comparison, enhance the `create_element_signature()` function to:
- Extract mesh vertices
- Compare surface areas
- Compare volumes
- Use more sophisticated geometric algorithms

## Requirements

- Allplan 2026
- Python scripting enabled in Allplan (enabled by default)
- Appropriate permissions to access the project and drawing files

## Files

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

2. **No drawing files found**:
   - Make sure you have opened an Allplan project
   - Make sure at least two drawing files (parts) are loaded in the project
   - The script only sees drawing files that are currently open

3. **Permission errors**:
   - Make sure you have read access to the project
   - Run Allplan as administrator if needed

4. **Element detection issues**:
   - Some custom elements might not be detected
   - Add the element type to the `get_all_3d_elements()` function

## Support

For issues or questions, please refer to the Allplan Python API documentation or contact Nemetschek support.

## License

This script is provided as-is for educational and professional use.

## Version History

- **1.1** (2024-12-19): Added Project Model Comparator for comparing drawing files within a project
- **1.0** (2024-12-19): Initial release with basic and advanced model comparators
