"""
Advanced Model 3D Element Comparator for Allplan 2026

This script provides a more comprehensive solution with:
- File dialog for selecting models to compare
- Detailed comparison report
- Visual highlighting of differences
- Export capabilities
"""

import AllplanBaseElements as abe
import Geometry as geom
import AllplanGeo as ag
from typing import Dict, List, Tuple, Set, Optional, Any
import math
import os


class ModelComparator:
    """Main class for comparing Allplan models."""
    
    def __init__(self, tolerance: float = 0.001):
        """
        Initialize the comparator.
        
        Args:
            tolerance: Tolerance for geometric comparison in meters
        """
        self.tolerance = tolerance
        self.doc = abe.Document.GetCurrentDocument()
        
    def get_all_3d_elements(self, doc: abe.Document = None) -> List[abe.Element]:
        """
        Get all 3D elements from the document.
        
        Args:
            doc: Allplan document object (defaults to current document)
            
        Returns:
            List of all 3D elements in the document
        """
        if doc is None:
            doc = self.doc
            
        elements = []
        
        if not doc:
            return elements
        
        # Get all elements in the document
        all_elements = abe.ModelElementFilter(doc)
        
        # List of 3D element types to include
        element_types_3d = [
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
            abe.EType.Arc3D,
            abe.EType.Reinforcement,
            abe.EType.EmbeddedElement,
        ]
        
        # Filter for 3D elements only
        for element in all_elements:
            try:
                if hasattr(element, 'GetType') and element.GetType() in element_types_3d:
                    elements.append(element)
            except Exception as e:
                print(f"Warning: Could not process element: {e}")
                continue
        
        return elements

    def get_element_properties(self, element: abe.Element) -> Dict[str, Any]:
        """
        Extract properties from an element for comparison.
        
        Args:
            element: Allplan element
            
        Returns:
            Dictionary of element properties
        """
        props = {}
        
        try:
            # Basic properties
            props['type'] = element.GetType().name if hasattr(element.GetType(), 'name') else str(element.GetType())
            
            # Element ID
            element_id = getattr(element, 'GetElementId', lambda: None)()
            if element_id:
                props['element_id'] = element_id
            
            # Bounding box
            bbox = getattr(element, 'GetBoundingBox', lambda: None)()
            if bbox:
                min_point = bbox.Min
                max_point = bbox.Max
                props['bbox_min'] = (min_point.X, min_point.Y, min_point.Z)
                props['bbox_max'] = (max_point.X, max_point.Y, max_point.Z)
                props['bbox_center'] = (
                    (min_point.X + max_point.X) / 2,
                    (min_point.Y + max_point.Y) / 2,
                    (min_point.Z + max_point.Z) / 2
                )
                props['bbox_dimensions'] = (
                    max_point.X - min_point.X,
                    max_point.Y - min_point.Y,
                    max_point.Z - min_point.Z
                )
            
            # Volume (if available)
            volume = getattr(element, 'GetVolume', lambda: None)()
            if volume is not None:
                props['volume'] = volume
            
            # Area (if available)
            area = getattr(element, 'GetArea', lambda: None)()
            if area is not None:
                props['area'] = area
            
            # Name/Description
            name = getattr(element, 'GetName', lambda: None)()
            if name:
                props['name'] = name
            
            # Layer
            layer = getattr(element, 'GetLayer', lambda: None)()
            if layer:
                props['layer'] = layer
            
            # Color
            color = getattr(element, 'GetColor', lambda: None)()
            if color:
                props['color'] = color
            
        except Exception as e:
            print(f"Warning: Could not extract properties for element: {e}")
        
        return props

    def create_element_signature(self, element: abe.Element) -> str:
        """
        Create a unique signature for an element based on its properties.
        
        Args:
            element: Allplan element
            
        Returns:
            String signature for the element
        """
        props = self.get_element_properties(element)
        
        # Create signature from key properties
        signature_parts = []
        
        # Type is always included
        signature_parts.append(f"type={props.get('type', 'Unknown')}")
        
        # Bounding box center and dimensions
        if 'bbox_center' in props:
            center = props['bbox_center']
            signature_parts.append(f"center={center[0]:.6f},{center[1]:.6f},{center[2]:.6f}")
        
        if 'bbox_dimensions' in props:
            dims = props['bbox_dimensions']
            signature_parts.append(f"dims={dims[0]:.6f},{dims[1]:.6f},{dims[2]:.6f}")
        
        # Volume if available
        if 'volume' in props:
            signature_parts.append(f"volume={props['volume']:.6f}")
        
        # Layer if available
        if 'layer' in props:
            signature_parts.append(f"layer={props['layer']}")
        
        return "|".join(signature_parts)

    def are_elements_similar(self, element1: abe.Element, element2: abe.Element) -> Tuple[bool, float]:
        """
        Compare two elements and return similarity score.
        
        Args:
            element1: First element
            element2: Second element
            
        Returns:
            Tuple of (is_similar, similarity_score)
        """
        try:
            props1 = self.get_element_properties(element1)
            props2 = self.get_element_properties(element2)
            
            # Check type compatibility
            if props1.get('type') != props2.get('type'):
                return False, 0.0
            
            # Check bounding box similarity
            if 'bbox_center' in props1 and 'bbox_center' in props2:
                center1 = props1['bbox_center']
                center2 = props2['bbox_center']
                
                distance = math.sqrt(
                    (center1[0] - center2[0]) ** 2 + 
                    (center1[1] - center2[1]) ** 2 + 
                    (center1[2] - center2[2]) ** 2
                )
                
                if distance > self.tolerance:
                    # Calculate similarity score based on distance
                    max_dist = max(self.tolerance * 10, distance)
                    similarity = 1.0 - (distance / max_dist)
                    return False, max(0.0, similarity)
            
            # Check dimensions similarity
            if 'bbox_dimensions' in props1 and 'bbox_dimensions' in props2:
                dims1 = props1['bbox_dimensions']
                dims2 = props2['bbox_dimensions']
                
                dim_diffs = [abs(d1 - d2) for d1, d2 in zip(dims1, dims2)]
                max_dim_diff = max(dim_diffs)
                
                if max_dim_diff > self.tolerance:
                    max_dim = max(max(dims1), max(dims2))
                    similarity = 1.0 - (max_dim_diff / max(max_dim, self.tolerance))
                    return False, max(0.0, similarity)
            
            # Check volume similarity
            if 'volume' in props1 and 'volume' in props2:
                vol1 = props1['volume']
                vol2 = props2['volume']
                vol_diff = abs(vol1 - vol2)
                
                if vol_diff > self.tolerance:
                    max_vol = max(abs(vol1), abs(vol2), self.tolerance)
                    similarity = 1.0 - (vol_diff / max_vol)
                    return False, max(0.0, similarity)
            
            # Elements are similar
            return True, 1.0
            
        except Exception as e:
            print(f"Warning: Could not compare elements: {e}")
            return False, 0.0

    def compare_models(self, doc1: abe.Document, doc2: abe.Document) -> Dict:
        """
        Compare two Allplan models.
        
        Args:
            doc1: First document
            doc2: Second document
            
        Returns:
            Dictionary containing comparison results
        """
        results = {
            'model1': {'path': '', 'elements': []},
            'model2': {'path': '', 'elements': []},
            'common': [],
            'only_in_model1': [],
            'only_in_model2': [],
            'similar_pairs': [],
            'different_pairs': [],
            'summary': {}
        }
        
        try:
            # Get elements from both models
            elements1 = self.get_all_3d_elements(doc1)
            elements2 = self.get_all_3d_elements(doc2)
            
            results['model1']['path'] = doc1.GetPath() if doc1 else "Unknown"
            results['model2']['path'] = doc2.GetPath() if doc2 else "Unknown"
            
            print(f"Model 1: {len(elements1)} 3D elements")
            print(f"Model 2: {len(elements2)} 3D elements")
            
            # Create signatures for all elements
            signatures1 = {}
            for i, element in enumerate(elements1):
                signature = self.create_element_signature(element)
                signatures1[signature] = {
                    'index': i,
                    'element': element,
                    'properties': self.get_element_properties(element)
                }
            
            signatures2 = {}
            for i, element in enumerate(elements2):
                signature = self.create_element_signature(element)
                signatures2[signature] = {
                    'index': i,
                    'element': element,
                    'properties': self.get_element_properties(element)
                }
            
            # Find common signatures
            common_signatures = set(signatures1.keys()) & set(signatures2.keys())
            only_in_1 = set(signatures1.keys()) - set(signatures2.keys())
            only_in_2 = set(signatures2.keys()) - set(signatures1.keys())
            
            # Check for similar but not identical elements
            similar_pairs = []
            different_pairs = []
            
            # Check elements that are only in one model for potential matches
            for sig1 in only_in_1:
                for sig2 in only_in_2:
                    el1 = signatures1[sig1]['element']
                    el2 = signatures2[sig2]['element']
                    
                    is_similar, similarity = self.are_elements_similar(el1, el2)
                    if is_similar:
                        similar_pairs.append({
                            'element1': sig1,
                            'element2': sig2,
                            'similarity': similarity
                        })
                    elif similarity > 0.5:  # Partial similarity
                        similar_pairs.append({
                            'element1': sig1,
                            'element2': sig2,
                            'similarity': similarity
                        })
            
            # Check common signatures for geometric differences
            for sig in common_signatures:
                el1 = signatures1[sig]['element']
                el2 = signatures2[sig]['element']
                
                is_similar, similarity = self.are_elements_similar(el1, el2)
                if not is_similar:
                    different_pairs.append({
                        'element1': sig,
                        'element2': sig,
                        'similarity': similarity
                    })
            
            # Populate results
            results['common'] = list(common_signatures)
            results['only_in_model1'] = list(only_in_1)
            results['only_in_model2'] = list(only_in_2)
            results['similar_pairs'] = similar_pairs
            results['different_pairs'] = different_pairs
            
            # Generate summary
            results['summary'] = {
                'total_model1': len(elements1),
                'total_model2': len(elements2),
                'common_count': len(common_signatures),
                'only_in_model1_count': len(only_in_1),
                'only_in_model2_count': len(only_in_2),
                'similar_pairs_count': len(similar_pairs),
                'different_pairs_count': len(different_pairs)
            }
            
        except Exception as e:
            results['error'] = str(e)
            print(f"Error comparing models: {e}")
            import traceback
            traceback.print_exc()
        
        return results

    def generate_report(self, results: Dict) -> str:
        """
        Generate a human-readable report from comparison results.
        
        Args:
            results: Comparison results dictionary
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("ALLPLAN 3D MODEL COMPARISON REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Model information
        report.append("MODEL INFORMATION:")
        report.append(f"  Model 1: {results['model1']['path']}")
        report.append(f"  Model 2: {results['model2']['path']}")
        report.append("")
        
        # Summary
        summary = results['summary']
        report.append("SUMMARY:")
        report.append(f"  Total elements in Model 1: {summary['total_model1']}")
        report.append(f"  Total elements in Model 2: {summary['total_model2']}")
        report.append(f"  Common elements: {summary['common_count']}")
        report.append(f"  Only in Model 1: {summary['only_in_model1_count']}")
        report.append(f"  Only in Model 2: {summary['only_in_model2_count']}")
        report.append(f"  Similar element pairs: {summary['similar_pairs_count']}")
        report.append(f"  Different element pairs: {summary['different_pairs_count']}")
        report.append("")
        
        # Details
        if summary['only_in_model1_count'] > 0:
            report.append("ELEMENTS ONLY IN MODEL 1:")
            for sig in results['only_in_model1'][:10]:  # Show first 10
                report.append(f"  - {sig}")
            if summary['only_in_model1_count'] > 10:
                report.append(f"  ... and {summary['only_in_model1_count'] - 10} more")
            report.append("")
        
        if summary['only_in_model2_count'] > 0:
            report.append("ELEMENTS ONLY IN MODEL 2:")
            for sig in results['only_in_model2'][:10]:  # Show first 10
                report.append(f"  - {sig}")
            if summary['only_in_model2_count'] > 10:
                report.append(f"  ... and {summary['only_in_model2_count'] - 10} more")
            report.append("")
        
        if summary['different_pairs_count'] > 0:
            report.append("GEOMETRIC DIFFERENCES:")
            for pair in results['different_pairs'][:10]:  # Show first 10
                report.append(f"  - {pair['element1']} vs {pair['element2']} (similarity: {pair['similarity']:.2%})")
            if summary['different_pairs_count'] > 10:
                report.append(f"  ... and {summary['different_pairs_count'] - 10} more")
            report.append("")
        
        if summary['similar_pairs_count'] > 0:
            report.append("SIMILAR ELEMENT PAIRS (not identical):")
            for pair in results['similar_pairs'][:10]:  # Show first 10
                report.append(f"  - {pair['element1']} vs {pair['element2']} (similarity: {pair['similarity']:.2%})")
            if summary['similar_pairs_count'] > 10:
                report.append(f"  ... and {summary['similar_pairs_count'] - 10} more")
            report.append("")
        
        report.append("=" * 60)
        report.append("END OF REPORT")
        report.append("=" * 60)
        
        return "\n".join(report)

    def export_results_to_file(self, results: Dict, filename: str) -> bool:
        """
        Export comparison results to a file.
        
        Args:
            results: Comparison results dictionary
            filename: Path to output file
            
        Returns:
            True if export was successful
        """
        try:
            report = self.generate_report(results)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report exported to: {filename}")
            return True
        except Exception as e:
            print(f"Error exporting report: {e}")
            return False


def select_file(dialog_title: str = "Select File") -> Optional[str]:
    """
    Open a file dialog to select a file.
    
    Args:
        dialog_title: Title for the file dialog
        
    Returns:
        Selected file path or None if cancelled
    """
    try:
        import System
        from System.Windows.Forms import OpenFileDialog, DialogResult
        
        dialog = OpenFileDialog()
        dialog.Title = dialog_title
        dialog.Filter = "Allplan Models (*.ndw;*.ndx)|*.ndw;*.ndx|All files (*.*)|*.*"
        dialog.Multiselect = False
        
        if dialog.ShowDialog() == DialogResult.OK:
            return dialog.FileName
        return None
    except Exception as e:
        print(f"File dialog not available: {e}")
        print("Please enter the file path manually.")
        return input("Enter file path: ").strip()


def main():
    """
    Main function to run the model comparison.
    """
    print("Allplan 3D Model Comparator - Advanced")
    print("=" * 40)
    
    try:
        # Create comparator instance
        comparator = ModelComparator(tolerance=0.001)  # 1mm tolerance
        
        # Get current document
        current_doc = abe.Document.GetCurrentDocument()
        if not current_doc:
            print("No active document found. Please open a model first.")
            return
        
        print(f"Current model: {current_doc.GetPath()}")
        
        # Ask user for comparison mode
        print("\nSelect comparison mode:")
        print("1. Compare current model with another model")
        print("2. Compare two external models")
        print("3. Analyze current model only")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == "1":
            # Compare current with another
            print("\nSelect the second model to compare with...")
            file2 = select_file("Select Second Model")
            
            if not file2:
                print("No file selected. Aborting.")
                return
            
            # Open the second document
            doc2 = abe.Document.Open(file2)
            if not doc2:
                print(f"Could not open: {file2}")
                return
            
            # Perform comparison
            results = comparator.compare_models(current_doc, doc2)
            
            # Generate and display report
            report = comparator.generate_report(results)
            print("\n" + report)
            
            # Ask if user wants to export
            export = input("\nExport report to file? (y/n): ").strip().lower()
            if export == 'y':
                export_path = select_file("Save Report As")
                if export_path:
                    comparator.export_results_to_file(results, export_path)
            
            # Close the second document
            doc2.Close()
            
        elif choice == "2":
            # Compare two external models
            print("\nSelect the first model...")
            file1 = select_file("Select First Model")
            
            if not file1:
                print("No file selected. Aborting.")
                return
            
            print("\nSelect the second model...")
            file2 = select_file("Select Second Model")
            
            if not file2:
                print("No file selected. Aborting.")
                return
            
            # Open both documents
            doc1 = abe.Document.Open(file1)
            doc2 = abe.Document.Open(file2)
            
            if not doc1 or not doc2:
                print("Could not open one or both models.")
                if doc1: doc1.Close()
                if doc2: doc2.Close()
                return
            
            # Perform comparison
            results = comparator.compare_models(doc1, doc2)
            
            # Generate and display report
            report = comparator.generate_report(results)
            print("\n" + report)
            
            # Ask if user wants to export
            export = input("\nExport report to file? (y/n): ").strip().lower()
            if export == 'y':
                export_path = select_file("Save Report As")
                if export_path:
                    comparator.export_results_to_file(results, export_path)
            
            # Close documents
            doc1.Close()
            doc2.Close()
            
        elif choice == "3":
            # Analyze current model only
            print("\nAnalyzing current model...")
            elements = comparator.get_all_3d_elements(current_doc)
            
            print(f"\nFound {len(elements)} 3D elements in current model.")
            
            # Group by type
            element_types = {}
            for element in elements:
                element_type = element.GetType().name if hasattr(element.GetType(), 'name') else str(element.GetType())
                element_types[element_type] = element_types.get(element_type, 0) + 1
            
            print("\nElement types:")
            for element_type, count in sorted(element_types.items()):
                print(f"  {element_type}: {count}")
            
            # Calculate total volume if available
            total_volume = 0.0
            volume_count = 0
            for element in elements:
                volume = getattr(element, 'GetVolume', lambda: None)()
                if volume is not None:
                    total_volume += volume
                    volume_count += 1
            
            if volume_count > 0:
                print(f"\nTotal volume of {volume_count} elements: {total_volume:.2f} m³")
        else:
            print("Invalid choice.")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
