"""
Model 3D Element Comparator for Allplan 2026

This script detects and compares 3D elements between two different Allplan models.
It identifies:
- Elements that exist in both models
- Elements that exist only in the first model
- Elements that exist only in the second model
- Geometric differences between corresponding elements
"""

import AllplanBaseElements as abe
import Geometry as geom
import AllplanGeo as ag
import AllplanBaseElements as abe
from typing import Dict, List, Tuple, Set, Optional
import math


def get_all_3d_elements(doc: abe.Document) -> List[abe.Element]:
    """
    Get all 3D elements from the document.
    
    Args:
        doc: Allplan document object
        
    Returns:
        List of all 3D elements in the document
    """
    elements = []
    
    # Get all elements in the document
    all_elements = abe.ModelElementFilter(doc)
    
    # Filter for 3D elements only
    for element in all_elements:
        if hasattr(element, 'GetType') and element.GetType() in [
            abe.EType.SmartSymbol3D,
            abe.EType.SmartPart,
            abe.EType.Extrusion,
            abe.EType.Revolution,
            abe.EType.Sweep,
            abe.EType.Loft,
            abe.EType.Pyramid,
            abe.EType.Cone,
            abe.EType.Sphere,
            abe.EType.Torus,
            abe.EType.Polyhedron,
            abe.EType.Mesh,
            abe.EType.Text3D,
            abe.EType.Line,
            abe.EType.Polyline3D,
            abe.EType.Spline3D,
            abe.EType.Circle3D,
            abe.EType.Ellipse3D,
            abe.EType.Arc3D
        ]:
            elements.append(element)
    
    return elements


def get_element_identifier(element: abe.Element) -> str:
    """
    Create a unique identifier for an element based on its properties.
    
    Args:
        element: Allplan element
        
    Returns:
        String identifier for the element
    """
    try:
        # Try to get element ID first
        element_id = getattr(element, 'GetElementId', lambda: None)()
        if element_id:
            return f"ID:{element_id}"
        
        # Fallback to type and bounding box
        element_type = element.GetType().name if hasattr(element.GetType(), 'name') else str(element.GetType())
        
        # Get bounding box if available
        bbox = getattr(element, 'GetBoundingBox', lambda: None)()
        if bbox:
            min_point = bbox.Min
            max_point = bbox.Max
            bbox_str = f"{min_point.X},{min_point.Y},{min_point.Z}-{max_point.X},{max_point.Y},{max_point.Z}"
            return f"{element_type}:{bbox_str}"
        
        return f"{element_type}:{id(element)}"
        
    except Exception as e:
        print(f"Warning: Could not create identifier for element: {e}")
        return f"Unknown:{id(element)}"


def get_element_geometric_hash(element: abe.Element) -> Optional[str]:
    """
    Create a geometric hash for an element to detect geometric changes.
    
    Args:
        element: Allplan element
        
    Returns:
        String hash representing the element's geometry, or None if not possible
    """
    try:
        # Get the element's geometry
        geometry = getattr(element, 'GetGeometry', lambda: None)()
        if not geometry:
            return None
        
        # For now, use bounding box as a simple geometric representation
        # In a more advanced version, you could use mesh vertices or other geometric properties
        bbox = getattr(element, 'GetBoundingBox', lambda: None)()
        if bbox:
            min_point = bbox.Min
            max_point = bbox.Max
            center = geom.Point3D(
                (min_point.X + max_point.X) / 2,
                (min_point.Y + max_point.Y) / 2,
                (min_point.Z + max_point.Z) / 2
            )
            dimensions = (
                max_point.X - min_point.X,
                max_point.Y - min_point.Y,
                max_point.Z - min_point.Z
            )
            return f"{center.X},{center.Y},{center.Z}:{dimensions[0]},{dimensions[1]},{dimensions[2]}"
        
        return None
        
    except Exception as e:
        print(f"Warning: Could not create geometric hash for element: {e}")
        return None


def compare_elements_by_geometry(element1: abe.Element, element2: abe.Element, tolerance: float = 0.001) -> bool:
    """
    Compare two elements geometrically.
    
    Args:
        element1: First element
        element2: Second element
        tolerance: Tolerance for geometric comparison
        
    Returns:
        True if elements are geometrically similar within tolerance
    """
    try:
        bbox1 = getattr(element1, 'GetBoundingBox', lambda: None)()
        bbox2 = getattr(element2, 'GetBoundingBox', lambda: None)()
        
        if not bbox1 or not bbox2:
            return False
        
        # Compare bounding boxes
        min1, max1 = bbox1.Min, bbox1.Max
        min2, max2 = bbox2.Min, bbox2.Max
        
        # Compare centers
        center1 = geom.Point3D((min1.X + max1.X) / 2, (min1.Y + max1.Y) / 2, (min1.Z + max1.Z) / 2)
        center2 = geom.Point3D((min2.X + max2.X) / 2, (min2.Y + max2.Y) / 2, (min2.Z + max2.Z) / 2)
        
        distance = math.sqrt(
            (center1.X - center2.X) ** 2 + 
            (center1.Y - center2.Y) ** 2 + 
            (center1.Z - center2.Z) ** 2
        )
        
        if distance > tolerance:
            return False
        
        # Compare dimensions
        dims1 = (max1.X - min1.X, max1.Y - min1.Y, max1.Z - min1.Z)
        dims2 = (max2.X - min2.X, max2.Y - min2.Y, max2.Z - min2.Z)
        
        for d1, d2 in zip(dims1, dims2):
            if abs(d1 - d2) > tolerance:
                return False
        
        return True
        
    except Exception as e:
        print(f"Warning: Could not compare elements geometrically: {e}")
        return False


def compare_models(model1_path: str, model2_path: str, tolerance: float = 0.001) -> Dict:
    """
    Compare two Allplan models and return the differences.
    
    Args:
        model1_path: Path to the first model
        model2_path: Path to the second model
        tolerance: Tolerance for geometric comparison
        
    Returns:
        Dictionary containing comparison results
    """
    from AllplanBaseElements import Document
    
    results = {
        'common_elements': [],
        'only_in_model1': [],
        'only_in_model2': [],
        'geometric_differences': [],
        'summary': {}
    }
    
    try:
        # Open first model
        doc1 = Document.Open(model1_path)
        if not doc1:
            raise Exception(f"Could not open model: {model1_path}")
        
        # Open second model
        doc2 = Document.Open(model2_path)
        if not doc2:
            raise Exception(f"Could not open model: {model2_path}")
        
        # Get all 3D elements from both models
        elements1 = get_all_3d_elements(doc1)
        elements2 = get_all_3d_elements(doc2)
        
        print(f"Model 1: {len(elements1)} 3D elements found")
        print(f"Model 2: {len(elements2)} 3D elements found")
        
        # Create dictionaries for quick lookup
        elements1_dict = {get_element_identifier(el): el for el in elements1}
        elements2_dict = {get_element_identifier(el): el for el in elements2}
        
        # Find common elements
        common_ids = set(elements1_dict.keys()) & set(elements2_dict.keys())
        only_in_1 = set(elements1_dict.keys()) - set(elements2_dict.keys())
        only_in_2 = set(elements2_dict.keys()) - set(elements1_dict.keys())
        
        # Check for geometric differences in common elements
        geometric_diff_pairs = []
        for element_id in common_ids:
            el1 = elements1_dict[element_id]
            el2 = elements2_dict[element_id]
            
            if not compare_elements_by_geometry(el1, el2, tolerance):
                geometric_diff_pairs.append((el1, el2))
        
        results['common_elements'] = list(common_ids)
        results['only_in_model1'] = list(only_in_1)
        results['only_in_model2'] = list(only_in_2)
        results['geometric_differences'] = [
            (get_element_identifier(el1), get_element_identifier(el2)) 
            for el1, el2 in geometric_diff_pairs
        ]
        
        # Generate summary
        results['summary'] = {
            'total_in_model1': len(elements1),
            'total_in_model2': len(elements2),
            'common_count': len(common_ids),
            'only_in_model1_count': len(only_in_1),
            'only_in_model2_count': len(only_in_2),
            'geometric_differences_count': len(geometric_diff_pairs)
        }
        
        # Close documents
        doc1.Close()
        doc2.Close()
        
    except Exception as e:
        results['error'] = str(e)
        print(f"Error comparing models: {e}")
    
    return results


def main():
    """
    Main function to run the model comparison.
    This will be called by Allplan when the script is executed.
    """
    from AllplanBaseElements import Document
    import AllplanBaseElements as abe
    
    print("Allplan 3D Model Comparator")
    print("=" * 40)
    
    try:
        # Get the current document
        doc = Document.GetCurrentDocument()
        if not doc:
            print("No active document found. Please open a model first.")
            return
        
        print(f"Current model: {doc.GetPath()}")
        
        # For now, we'll compare the current document with another one
        # In a real scenario, you might want to use a file dialog
        print("\nThis script compares 3D elements between two models.")
        print("Please ensure you have two models open or provide paths to compare.")
        
        # Get all 3D elements in current document
        elements = get_all_3d_elements(doc)
        print(f"\nFound {len(elements)} 3D elements in current model.")
        
        # Display element types
        element_types = {}
        for element in elements:
            element_type = element.GetType().name if hasattr(element.GetType(), 'name') else str(element.GetType())
            element_types[element_type] = element_types.get(element_type, 0) + 1
        
        print("\nElement types found:")
        for element_type, count in sorted(element_types.items()):
            print(f"  {element_type}: {count}")
        
        # Example: Compare with itself (for demonstration)
        print("\nRunning self-comparison test...")
        current_path = doc.GetPath()
        results = compare_models(current_path, current_path)
        
        print("\nComparison Results:")
        print(f"  Common elements: {results['summary']['common_count']}")
        print(f"  Only in model 1: {results['summary']['only_in_model1_count']}")
        print(f"  Only in model 2: {results['summary']['only_in_model2_count']}")
        print(f"  Geometric differences: {results['summary']['geometric_differences_count']}")
        
        if 'error' in results:
            print(f"\nError: {results['error']}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
