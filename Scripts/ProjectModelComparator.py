"""
Project Model Comparator for Allplan 2026

This script compares 3D elements between two drawing files (parts) that are already
loaded in the current Allplan project.

Features:
- Compare 3D elements between two drawing files in the same project
- Identify elements that exist in one but not the other
- HIGHLIGHT missing elements in the second drawing file
- Detailed reporting with export capabilities

Usage:
1. Open your Allplan project
2. Make sure both drawing files you want to compare are loaded
3. Run this script
4. Select the two drawing files from the list of open parts
5. Elements missing in the second drawing will be highlighted
"""

import AllplanBaseElements as abe
import Geometry as geom
import AllplanGeo as ag
from typing import Dict, List, Tuple, Set, Optional, Any
import math


class ProjectModelComparator:
    """Compare 3D elements between drawing files in the same project."""
    
    def __init__(self, tolerance: float = 0.001):
        """
        Initialize the comparator.
        
        Args:
            tolerance: Tolerance for geometric comparison in meters
        """
        self.tolerance = tolerance
        self.project = abe.Document.GetCurrentProject()
        self.highlight_color = abe.Color(255, 0, 0)  # Red color for highlighting
        self.highlight_layer = None
        self.created_highlight_layer = False
        
    def create_highlight_layer(self, doc: abe.Document) -> bool:
        """
        Create a special layer for highlighting missing elements.
        
        Args:
            doc: Document to create the layer in
            
        Returns:
            True if layer was created or already exists
        """
        try:
            # Check if layer already exists
            layer_name = "COMPARISON_HIGHLIGHT_MISSING"
            
            # Try to get existing layer
            layer = abe.Layer.Find(layer_name)
            if layer:
                self.highlight_layer = layer
                return True
            
            # Create new layer
            layer = abe.Layer.Create(layer_name)
            if layer:
                # Set layer properties
                layer.SetColor(self.highlight_color)
                layer.SetLineStyle(1)  # Solid line
                layer.SetLineWidth(2)  # Thicker line
                layer.SetVisible(True)
                layer.SetLocked(False)
                layer.SetPrintable(True)
                
                self.highlight_layer = layer
                self.created_highlight_layer = True
                return True
                
        except Exception as e:
            print(f"Warning: Could not create highlight layer: {e}")
            # Fallback: use a standard layer
            try:
                self.highlight_layer = abe.Layer.Find("Standard")
                if self.highlight_layer:
                    return True
            except:
                pass
        
        return False

    def cleanup_highlight_layer(self, doc: abe.Document) -> None:
        """
        Clean up the highlight layer if we created it.
        
        Args:
            doc: Document to clean up
        """
        if self.created_highlight_layer and self.highlight_layer:
            try:
                # Remove all elements on the highlight layer
                elements = abe.ModelElementFilter(doc, abe.ElementFilter.Layer(self.highlight_layer))
                for element in elements:
                    try:
                        element.Delete()
                    except:
                        pass
                
                # Don't delete the layer itself as it might be used elsewhere
                # self.highlight_layer.Delete()
                
                self.created_highlight_layer = False
            except Exception as e:
                print(f"Warning: Could not clean up highlight layer: {e}")

    def get_open_drawing_files(self) -> List[abe.Document]:
        """
        Get all open drawing files (parts) in the current project.
        
        Returns:
            List of open document objects
        """
        open_docs = []
        
        if not self.project:
            print("No active project found.")
            return open_docs
        
        try:
            # Get all open documents in the project
            all_docs = abe.Document.GetAllOpenDocuments()
            
            for doc in all_docs:
                # Filter for drawing files (parts), not layouts or other types
                if doc and doc.GetDocumentType() == abe.DocumentType.Part:
                    open_docs.append(doc)
                    
        except Exception as e:
            print(f"Error getting open documents: {e}")
        
        return open_docs

    def get_all_3d_elements(self, doc: abe.Document) -> List[abe.Element]:
        """
        Get all 3D elements from a drawing file.
        
        Args:
            doc: Allplan document object
            
        Returns:
            List of all 3D elements in the document
        """
        elements = []
        
        if not doc:
            return elements
        
        try:
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
                    # Skip elements we can't process
                    continue
                    
        except Exception as e:
            print(f"Error getting 3D elements: {e}")
        
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
                props['layer'] = str(layer)
            
        except Exception as e:
            print(f"Warning: Could not extract properties for element: {e}")
        
        return props

    def create_element_signature(self, element: abe.Element) -> str:
        """
        Create a unique signature for an element based on its properties.
        Uses geometric properties that should be consistent across drawing files.
        
        Args:
            element: Allplan element
            
        Returns:
            String signature for the element
        """
        props = self.get_element_properties(element)
        
        # Create signature from geometric properties (not IDs, as they differ between files)
        signature_parts = []
        
        # Type is always included
        signature_parts.append(f"type={props.get('type', 'Unknown')}")
        
        # Bounding box center and dimensions (these should be in project coordinates)
        if 'bbox_center' in props:
            center = props['bbox_center']
            # Round to tolerance precision to avoid floating point issues
            rounded_center = (round(center[0], 6), round(center[1], 6), round(center[2], 6))
            signature_parts.append(f"center={rounded_center[0]:.6f},{rounded_center[1]:.6f},{rounded_center[2]:.6f}")
        
        if 'bbox_dimensions' in props:
            dims = props['bbox_dimensions']
            rounded_dims = (round(dims[0], 6), round(dims[1], 6), round(dims[2], 6))
            signature_parts.append(f"dims={rounded_dims[0]:.6f},{rounded_dims[1]:.6f},{rounded_dims[2]:.6f}")
        
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
                max_dim_diff = max(dim_diffs) if dim_diffs else 0
                
                if max_dim_diff > self.tolerance:
                    max_dim = max(max(dims1), max(dims2)) if dims1 and dims2 else self.tolerance
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

    def highlight_missing_elements(self, doc: abe.Document, missing_elements: List[Dict]) -> int:
        """
        Highlight elements that are missing in the second drawing file.
        Creates visual markers at the positions of missing elements.
        
        Args:
            doc: The second document where elements are missing
            missing_elements: List of element info that are missing
            
        Returns:
            Number of elements highlighted
        """
        highlighted_count = 0
        
        if not doc or not missing_elements:
            return 0
        
        try:
            # Create highlight layer
            if not self.create_highlight_layer(doc):
                print("Warning: Could not create highlight layer. Using default layer.")
                # Try to use an existing layer
                try:
                    self.highlight_layer = abe.Layer.Find("Standard")
                except:
                    self.highlight_layer = None
            
            print(f"\nHighlighting {len(missing_elements)} missing elements in: {doc.GetName()}")
            
            # Highlight each missing element
            for element_info in missing_elements:
                try:
                    props = element_info.get('properties', {})
                    
                    # Get the position (use bbox center if available)
                    if 'bbox_center' in props:
                        center = props['bbox_center']
                        x, y, z = center[0], center[1], center[2]
                        
                        # Create a marker at this position
                        # We'll create a small sphere or text marker
                        
                        # Option 1: Create a small sphere
                        sphere = abe.Sphere.Create(
                            geom.Point3D(x, y, z),
                            0.1  # Radius of 10cm
                        )
                        
                        if sphere:
                            # Set sphere properties
                            if self.highlight_layer:
                                sphere.SetLayer(self.highlight_layer)
                            sphere.SetColor(self.highlight_color)
                            sphere.SetFillColor(self.highlight_color)
                            sphere.SetTransparency(0.5)  # Semi-transparent
                            highlighted_count += 1
                        
                        # Option 2: Also create a text label
                        element_type = props.get('type', 'Unknown')
                        text = f"MISSING: {element_type}"
                        
                        text_element = abe.Text3D.Create(
                            geom.Point3D(x, y, z + 0.2),  # Slightly above the sphere
                            text,
                            0.1  # Height
                        )
                        
                        if text_element:
                            if self.highlight_layer:
                                text_element.SetLayer(self.highlight_layer)
                            text_element.SetColor(self.highlight_color)
                            
                    elif 'bbox_min' in props and 'bbox_max' in props:
                        # If we have bbox, create a bounding box representation
                        min_pt = geom.Point3D(props['bbox_min'][0], props['bbox_min'][1], props['bbox_min'][2])
                        max_pt = geom.Point3D(props['bbox_max'][0], props['bbox_max'][1], props['bbox_max'][2])
                        
                        # Create a box at this location
                        # For simplicity, create a sphere at the center
                        center_x = (props['bbox_min'][0] + props['bbox_max'][0]) / 2
                        center_y = (props['bbox_min'][1] + props['bbox_max'][1]) / 2
                        center_z = (props['bbox_min'][2] + props['bbox_max'][2]) / 2
                        
                        sphere = abe.Sphere.Create(
                            geom.Point3D(center_x, center_y, center_z),
                            0.1
                        )
                        
                        if sphere:
                            if self.highlight_layer:
                                sphere.SetLayer(self.highlight_layer)
                            sphere.SetColor(self.highlight_color)
                            sphere.SetFillColor(self.highlight_color)
                            sphere.SetTransparency(0.5)
                            highlighted_count += 1
                            
                except Exception as e:
                    print(f"Warning: Could not highlight element: {e}")
                    continue
            
            print(f"Successfully highlighted {highlighted_count} missing elements.")
            
        except Exception as e:
            print(f"Error highlighting missing elements: {e}")
            import traceback
            traceback.print_exc()
        
        return highlighted_count

    def compare_drawing_files(self, doc1: abe.Document, doc2: abe.Document, highlight_missing: bool = True) -> Dict:
        """
        Compare two drawing files within the same project.
        
        Args:
            doc1: First drawing file document (reference)
            doc2: Second drawing file document (to check against)
            highlight_missing: Whether to highlight missing elements in doc2
            
        Returns:
            Dictionary containing comparison results
        """
        results = {
            'drawing1': {'name': '', 'path': '', 'elements': []},
            'drawing2': {'name': '', 'path': '', 'elements': []},
            'common': [],
            'only_in_drawing1': [],
            'only_in_drawing2': [],
            'similar_pairs': [],
            'different_pairs': [],
            'missing_in_drawing2': [],  # Elements from doc1 missing in doc2
            'missing_in_drawing1': [],  # Elements from doc2 missing in doc1
            'summary': {}
        }
        
        try:
            # Get document names
            name1 = doc1.GetName() if doc1 else "Unknown"
            name2 = doc2.GetName() if doc2 else "Unknown"
            path1 = doc1.GetPath() if doc1 else "Unknown"
            path2 = doc2.GetPath() if doc2 else "Unknown"
            
            results['drawing1']['name'] = name1
            results['drawing1']['path'] = path1
            results['drawing2']['name'] = name2
            results['drawing2']['path'] = path2
            
            # Get elements from both drawing files
            print(f"Getting elements from: {name1}")
            elements1 = self.get_all_3d_elements(doc1)
            print(f"Getting elements from: {name2}")
            elements2 = self.get_all_3d_elements(doc2)
            
            print(f"{name1}: {len(elements1)} 3D elements")
            print(f"{name2}: {len(elements2)} 3D elements")
            
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
            
            # Store missing elements with their properties
            results['missing_in_drawing2'] = [
                {'signature': sig, 'properties': signatures1[sig]['properties']}
                for sig in only_in_1
            ]
            
            results['missing_in_drawing1'] = [
                {'signature': sig, 'properties': signatures2[sig]['properties']}
                for sig in only_in_2
            ]
            
            # Check for similar but not identical elements
            similar_pairs = []
            different_pairs = []
            
            # Check elements that are only in one drawing for potential matches
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
            results['only_in_drawing1'] = list(only_in_1)
            results['only_in_drawing2'] = list(only_in_2)
            results['similar_pairs'] = similar_pairs
            results['different_pairs'] = different_pairs
            
            # Generate summary
            results['summary'] = {
                'total_drawing1': len(elements1),
                'total_drawing2': len(elements2),
                'common_count': len(common_signatures),
                'only_in_drawing1_count': len(only_in_1),
                'only_in_drawing2_count': len(only_in_2),
                'similar_pairs_count': len(similar_pairs),
                'different_pairs_count': len(different_pairs),
                'missing_in_drawing2_count': len(results['missing_in_drawing2']),
                'missing_in_drawing1_count': len(results['missing_in_drawing1'])
            }
            
            # Highlight missing elements if requested
            if highlight_missing and len(results['missing_in_drawing2']) > 0:
                print(f"\nHighlighting {len(results['missing_in_drawing2'])} elements from {name1} that are missing in {name2}...")
                highlighted = self.highlight_missing_elements(doc2, results['missing_in_drawing2'])
                results['summary']['highlighted_count'] = highlighted
            
        except Exception as e:
            results['error'] = str(e)
            print(f"Error comparing drawing files: {e}")
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
        report.append("=" * 70)
        report.append("ALLPLAN PROJECT MODEL COMPARISON REPORT")
        report.append("Comparing Two Drawing Files in the Same Project")
        report.append("=" * 70)
        report.append("")
        
        # Drawing file information
        report.append("DRAWING FILES:")
        report.append(f"  Drawing 1 (Reference): {results['drawing1']['name']}")
        report.append(f"    Path: {results['drawing1']['path']}")
        report.append(f"  Drawing 2 (Compared): {results['drawing2']['name']}")
        report.append(f"    Path: {results['drawing2']['path']}")
        report.append("")
        
        # Summary
        summary = results['summary']
        report.append("SUMMARY:")
        report.append(f"  Total 3D elements in Drawing 1: {summary['total_drawing1']}")
        report.append(f"  Total 3D elements in Drawing 2: {summary['total_drawing2']}")
        report.append(f"  Common elements: {summary['common_count']}")
        report.append(f"  Only in Drawing 1: {summary['only_in_drawing1_count']}")
        report.append(f"  Only in Drawing 2: {summary['only_in_drawing2_count']}")
        report.append(f"  Similar element pairs: {summary['similar_pairs_count']}")
        report.append(f"  Different element pairs: {summary['different_pairs_count']}")
        report.append("")
        
        # Missing elements
        report.append("MISSING ELEMENTS:")
        report.append(f"  Elements in Drawing 1 missing from Drawing 2: {summary.get('missing_in_drawing2_count', 0)}")
        report.append(f"  Elements in Drawing 2 missing from Drawing 1: {summary.get('missing_in_drawing1_count', 0)}")
        
        if 'highlighted_count' in summary:
            report.append(f"  Highlighted in Drawing 2: {summary['highlighted_count']}")
        report.append("")
        
        # Calculate percentages
        if summary['total_drawing1'] > 0 or summary['total_drawing2'] > 0:
            total_all = summary['total_drawing1'] + summary['total_drawing2']
            common_pct = (summary['common_count'] * 2 / total_all * 100) if total_all > 0 else 0
            report.append(f"  Match rate: {common_pct:.1f}%")
            report.append("")
        
        # Details
        if summary.get('missing_in_drawing2_count', 0) > 0:
            report.append("ELEMENTS IN DRAWING 1 MISSING FROM DRAWING 2:")
            for item in results['missing_in_drawing2'][:10]:  # Show first 10
                sig = item['signature']
                props = item.get('properties', {})
                element_type = props.get('type', 'Unknown')
                report.append(f"  - {element_type}: {sig}")
            if summary['missing_in_drawing2_count'] > 10:
                report.append(f"  ... and {summary['missing_in_drawing2_count'] - 10} more")
            report.append("")
        
        if summary.get('missing_in_drawing1_count', 0) > 0:
            report.append("ELEMENTS IN DRAWING 2 MISSING FROM DRAWING 1:")
            for item in results['missing_in_drawing1'][:10]:  # Show first 10
                sig = item['signature']
                props = item.get('properties', {})
                element_type = props.get('type', 'Unknown')
                report.append(f"  - {element_type}: {sig}")
            if summary['missing_in_drawing1_count'] > 10:
                report.append(f"  ... and {summary['missing_in_drawing1_count'] - 10} more")
            report.append("")
        
        if summary['only_in_drawing1_count'] > 0:
            report.append("ELEMENTS ONLY IN DRAWING 1:")
            for sig in results['only_in_drawing1'][:10]:  # Show first 10
                report.append(f"  - {sig}")
            if summary['only_in_drawing1_count'] > 10:
                report.append(f"  ... and {summary['only_in_drawing1_count'] - 10} more")
            report.append("")
        
        if summary['only_in_drawing2_count'] > 0:
            report.append("ELEMENTS ONLY IN DRAWING 2:")
            for sig in results['only_in_drawing2'][:10]:  # Show first 10
                report.append(f"  - {sig}")
            if summary['only_in_drawing2_count'] > 10:
                report.append(f"  ... and {summary['only_in_drawing2_count'] - 10} more")
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
        
        report.append("=" * 70)
        report.append("HIGHLIGHTING:")
        report.append("  Missing elements from Drawing 1 have been highlighted in Drawing 2")
        report.append("  with red spheres and text labels on the 'COMPARISON_HIGHLIGHT_MISSING' layer.")
        report.append("=" * 70)
        report.append("END OF REPORT")
        report.append("=" * 70)
        
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


def main():
    """
    Main function to run the comparison of drawing files within a project.
    """
    print("=" * 70)
    print("ALLPLAN PROJECT MODEL COMPARATOR")
    print("Compare 3D elements between two drawing files in the same project")
    print("Missing elements will be HIGHLIGHTED in the second drawing file")
    print("=" * 70)
    print()
    
    try:
        # Create comparator instance
        comparator = ProjectModelComparator(tolerance=0.001)  # 1mm tolerance
        
        # Get current project
        project = abe.Document.GetCurrentProject()
        if not project:
            print("ERROR: No active project found.")
            print("Please open an Allplan project first.")
            return
        
        print(f"Current project: {project.GetName()}")
        print()
        
        # Get all open drawing files
        open_docs = comparator.get_open_drawing_files()
        
        if len(open_docs) < 2:
            print(f"ERROR: Found only {len(open_docs)} open drawing file(s).")
            print("Please open at least two drawing files in your project.")
            return
        
        # List available drawing files
        print("OPEN DRAWING FILES IN PROJECT:")
        for i, doc in enumerate(open_docs, 1):
            name = doc.GetName() if doc else "Unknown"
            print(f"  {i}. {name}")
        print()
        
        # Let user select two drawing files
        print("Select two drawing files to compare:")
        print("  The first will be the REFERENCE")
        print("  Elements missing from the first will be HIGHLIGHTED in the second")
        print()
        
        try:
            choice1 = int(input(f"Enter number for first drawing (REFERENCE) (1-{len(open_docs)}): ").strip())
            choice2 = int(input(f"Enter number for second drawing (TO CHECK) (1-{len(open_docs)}): ").strip())
        except ValueError:
            print("ERROR: Please enter valid numbers.")
            return
        
        # Validate choices
        if choice1 < 1 or choice1 > len(open_docs) or choice2 < 1 or choice2 > len(open_docs):
            print(f"ERROR: Please enter numbers between 1 and {len(open_docs)}.")
            return
        
        if choice1 == choice2:
            print("ERROR: Please select two different drawing files.")
            return
        
        # Get the selected documents
        doc1 = open_docs[choice1 - 1]
        doc2 = open_docs[choice2 - 1]
        
        name1 = doc1.GetName() if doc1 else "Unknown"
        name2 = doc2.GetName() if doc2 else "Unknown"
        
        print(f"\nComparing: {name1} (REFERENCE) vs {name2} (TO CHECK)")
        print("Missing elements from REFERENCE will be highlighted in TO CHECK")
        print("Please wait...")
        
        # Perform comparison with highlighting enabled
        results = comparator.compare_drawing_files(doc1, doc2, highlight_missing=True)
        
        # Generate and display report
        report = comparator.generate_report(results)
        print("\n" + report)
        
        # Ask if user wants to export
        export = input("\nExport report to file? (y/n): ").strip().lower()
        if export == 'y':
            # Use a simple approach for file export
            default_filename = f"Comparison_{name1}_vs_{name2}.txt"
            print(f"\nReport will be saved as: {default_filename}")
            success = comparator.export_results_to_file(results, default_filename)
            if success:
                print(f"Report saved successfully!")
            else:
                print("Failed to save report.")
        
        print("\n" + "=" * 70)
        print("COMPARISON COMPLETE")
        print("Check the second drawing file for highlighted missing elements!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
