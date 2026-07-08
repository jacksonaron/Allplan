# Allplan 3D Model Comparator

A Python script for Allplan 2026 that detects and compares 3D elements between two different models.

## Features

- Detects all 3D elements in Allplan models
- Compares elements between two models
- Identifies:
  - Elements that exist in both models
  - Elements that exist only in the first model
  - Elements that exist only in the second model
  - Geometric differences between corresponding elements

## Installation

1. **Copy the files** to your Allplan Python scripts directory:
   - Typically: `C:\ProgramData\Nemetschek\Allplan 2026\Scripts\Python\`
   - Or: `%APPDATA%\Nemetschek\Allplan 2026\Scripts\Python\`

2. **Folder structure** should look like:
   ```
   Scripts/
   ├── ModelComparator.pyd
   └── ModelComparator.py
   ```

3. **Restart Allplan** - The script should appear in the Tools menu or Add-ins ribbon tab.

## Usage

1. Open Allplan 2026
2. The script will be available in:
   - **Menu**: Tools → Model 3D Element Comparator
   - **Ribbon**: Add-ins → Model Tools → Model 3D Element Comparator

3. Run the script to analyze the current model
4. To compare two different models, modify the script to:
   - Use file dialogs to select models
   - Or hardcode the paths to your models

## Customization

### Changing the Comparison Tolerance

Edit the `tolerance` parameter in the `compare_models()` function call:

```python
# Default tolerance is 0.001 (1mm)
results = compare_models(path1, path2, tolerance=0.01)  # 1cm tolerance
```

### Adding More Element Types

The script currently checks for common 3D element types. To add more, edit the `get_all_3d_elements()` function:

```python
# Add more element types to this list
if element.GetType() in [
    abe.EType.SmartSymbol3D,
    abe.EType.SmartPart,
    # Add your custom types here
    abe.EType.YourCustomType,
]:
```

### Advanced Geometric Comparison

For more accurate geometric comparison, you can enhance the `get_element_geometric_hash()` function to:
- Extract mesh vertices
- Compare surface areas
- Compare volumes
- Use more sophisticated geometric algorithms

## Requirements

- Allplan 2026
- Python scripting enabled in Allplan
- Appropriate permissions to access models

## Files

- **ModelComparator.pyd** - Allplan Python Definition file (tells Allplan about the script)
- **ModelComparator.py** - The actual Python script

## Troubleshooting

1. **Script not appearing in menu**:
   - Check that both files are in the correct Scripts directory
   - Ensure the `.pyd` file has the correct XML structure
   - Restart Allplan

2. **Permission errors**:
   - Make sure you have read access to both models
   - Run Allplan as administrator if needed

3. **Element detection issues**:
   - Some custom elements might not be detected
   - Add the element type to the `get_all_3d_elements()` function

## Support

For issues or questions, please refer to the Allplan Python API documentation or contact Nemetschek support.

## License

This script is provided as-is for educational and professional use.

## Version History

- **1.0** (2024-12-19): Initial release
