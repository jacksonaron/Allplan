"""
Color-Based 3D Model Comparator for Allplan 2026

This script compares 3D models based on their color across all open drawing files in a project.

Perfect for:
- Comparing two sets of models (e.g., existing vs proposed, old vs new)
- When models are spread across multiple drawing files
- When models are distinguished by color

Usage:
1. Open your Allplan project with all relevant drawing files loaded
2. Make sure your models are colored appropriately (e.g., red for existing, green for proposed)
3. Run this script
4. Enter the colors for the two sets you want to compare
5. The script will find all elements of each color across ALL open drawing files
6. Compare them and highlight missing elements
"""

import AllplanBaseElements as abe
import Geometry as geom
import AllplanGeo as ag
from typing import Dict, List, Tuple, Set, Optional, Any
import math


class ColorModelComparator:
    """Compare 3D models based on color across all drawing files in a project."""
    
    def __init__(self, tolerance: float = 0.001):
        """
        Initialize the comparator.
        
        Args:
            tolerance: Tolerance for geometric comparison in meters
        """
        self.tolerance = tolerance
        self.project = abe.Document.GetCurrentProject()
        self.highlight_color = abe.Color(255, 0, 0)  # Red for highlighting
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
            layer_name = "COLOR_COMPARISON_HIGHLIGHT"
            
            # Try to get existing layer
            layer = abe.Layer.Find(layer_name)
            if layer:
                self.highlight_layer = layer
                return True
            
            # Create new layer
            layer = abe.Layer.Create(layer_name)
            if layer:
                layer.SetColor(self.highlight_color)
                layer.SetLineStyle(1)
                layer.SetLineWidth(2)
                layer.SetVisible(True)
                layer.SetLocked(False)
                layer.SetPrintable(True)
                
                self.highlight_layer = layer
                self.created_highlight_layer = True
                return True
                
        except Exception as e:
            print(f"Warning: Could not create highlight layer: {e}")
            try:
                self.highlight_layer = abe.Layer.Find("Standard")
                if self.highlight_layer:
                    return True
            except:
                pass
        
        return False

    def get_all_open_documents(self) -> List[abe.Document]:
        """
        Get all open documents (drawing files) in the current project.
        
        Returns:
            List of open document objects
        """
        open_docs = []
        
        if not self.project:
            print("No active project found.")
            return open_docs
        
        try:
            all_docs = abe.Document.GetAllOpenDocuments()
            for doc in all_docs:
                if doc and doc.GetDocumentType() == abe.DocumentType.Part:
                    open_docs.append(doc)
        except Exception as e:
            print(f"Error getting open documents: {e}")
        
        return open_docs

    def get_all_3d_elements_by_color(self, color: abe.Color, docs: List[abe.Document] = None) -> List[Dict]:
        """
        Get all 3D elements of a specific color across all provided documents.
        
        Args:
            color: The color to filter by
            docs: List of documents to search (defaults to all open documents)
            
        Returns:
            List of dictionaries with element info and their document
        """
        elements = []
        
        if docs is None:
            docs = self.get_all_open_documents()
        
        if not docs:
            return elements
        
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
        
        for doc in docs:
            try:
                all_elements = abe.ModelElementFilter(doc)
                
                for element in all_elements:
                    try:
                        # Check if it's a 3D element type
                        if hasattr(element, 'GetType') and element.GetType() in element_types_3d:
                            # Check the element's color
                            element_color = getattr(element, 'GetColor', lambda: None)()
                            
                            if element_color and self.colors_match(element_color, color):
                                elements.append({
                                    'element': element,
                                    'document': doc,
                                    'color': element_color,
                                    'properties': self.get_element_properties(element)
                                })
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"Error processing document {doc.GetName() if doc else 'Unknown'}: {e}")
                continue
        
        return elements

    def colors_match(self, color1: abe.Color, color2: abe.Color, tolerance: int = 5) -> bool:
        """
        Check if two colors match within a tolerance.
        
        Args:
            color1: First color
            color2: Second color
            tolerance: Tolerance for color component difference (0-255)
            
        Returns:
            True if colors match
        """
        try:
            r1, g1, b1 = color1.Red, color1.Green, color1.Blue
            r2, g2, b2 = color2.Red, color2.Green, color2.Blue
            
            return (abs(r1 - r2) <= tolerance and 
                    abs(g1 - g2) <= tolerance and 
                    abs(b1 - b2) <= tolerance)
        except:
            return False

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
            
            # Volume
            volume = getattr(element, 'GetVolume', lambda: None)()
            if volume is not None:
                props['volume'] = volume
            
            # Area
            area = getattr(element, 'GetArea', lambda: None)()
            if area is not None:
                props['area'] = area
            
            # Name
            name = getattr(element, 'GetName', lambda: None)()
            if name:
                props['name'] = name
            
            # Layer
            layer = getattr(element, 'GetLayer', lambda: None)()
            if layer:
                props['layer'] = str(layer)
            
            # Color
            color = getattr(element, 'GetColor', lambda: None)()
            if color:
                props['color'] = f"R{color.Red}G{color.Green}B{color.Blue}"
            
            # Document name
            doc = getattr(element, 'GetDocument', lambda: None)()
            if doc:
                props['document'] = doc.GetName() if hasattr(doc, 'GetName') else str(doc)
            
        except Exception as e:
            print(f"Warning: Could not extract properties: {e}")
        
        return props

    def create_element_signature(self, element_info: Dict) -> str:
        """
        Create a unique signature for an element based on its geometric properties.
        
        Args:
            element_info: Dictionary with element and properties
            
        Returns:
            String signature for the element
        """
        props = element_info.get('properties', {})
        
        signature_parts = []
        
        # Type
        signature_parts.append(f"type={props.get('type', 'Unknown')}")
        
        # Bounding box center and dimensions
        if 'bbox_center' in props:
            center = props['bbox_center']
            rounded_center = (round(center[0], 6), round(center[1], 6), round(center[2], 6))
            signature_parts.append(f"center={rounded_center[0]:.6f},{rounded_center[1]:.6f},{rounded_center[2]:.6f}")
        
        if 'bbox_dimensions' in props:
            dims = props['bbox_dimensions']
            rounded_dims = (round(dims[0], 6), round(dims[1], 6), round(dims[2], 6))
            signature_parts.append(f"dims={rounded_dims[0]:.6f},{rounded_dims[1]:.6f},{rounded_dims[2]:.6f}")
        
        # Volume if available
        if 'volume' in props:
            signature_parts.append(f"volume={props['volume']:.6f}")
        
        return "|".join(signature_parts)

    def are_elements_similar(self, element_info1: Dict, element_info2: Dict) -> Tuple[bool, float]:
        """
        Compare two elements and return similarity score.
        
        Args:
            element_info1: First element info dict
            element_info2: Second element info dict
            
        Returns:
            Tuple of (is_similar, similarity_score)
        """
        try:
            props1 = element_info1.get('properties', {})
            props2 = element_info2.get('properties', {})
            
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
            
            return True, 1.0
            
        except Exception as e:
            print(f"Warning: Could not compare elements: {e}")
            return False, 0.0

    def highlight_missing_elements(self, missing_elements: List[Dict]) -> int:
        """
        Highlight elements that are missing from the second set.
        Creates visual markers at the positions of missing elements.
        
        Args:
            missing_elements: List of element info that are missing
            
        Returns:
            Number of elements highlighted
        """
        highlighted_count = 0
        
        if not missing_elements:
            return 0
        
        try:
            print(f"\nHighlighting {len(missing_elements)} missing elements...")
            
            for element_info in missing_elements:
                try:
                    props = element_info.get('properties', {})
                    doc = element_info.get('document')
                    
                    if not doc:
                        continue
                    
                    # Create highlight layer in this document if not already done
                    if not self.highlight_layer or self.highlight_layer.GetDocument() != doc:
                        if not self.create_highlight_layer(doc):
                            print(f"Warning: Could not create highlight layer in {doc.GetName()}")
                            continue
                    
                    # Get the position
                    if 'bbox_center' in props:
                        center = props['bbox_center']
                        x, y, z = center[0], center[1], center[2]
                        
                        # Create a sphere marker
                        sphere = abe.Sphere.Create(
                            geom.Point3D(x, y, z),
                            0.1  # 10cm radius
                        )
                        
                        if sphere:
                            if self.highlight_layer:
                                sphere.SetLayer(self.highlight_layer)
                            sphere.SetColor(self.highlight_color)
                            sphere.SetFillColor(self.highlight_color)
                            sphere.SetTransparency(0.5)
                            highlighted_count += 1
                        
                        # Create a text label
                        element_type = props.get('type', 'Unknown')
                        text = f"MISSING"
                        
                        text_element = abe.Text3D.Create(
                            geom.Point3D(x, y, z + 0.2),
                            text,
                            0.1
                        )
                        
                        if text_element:
                            if self.highlight_layer:
                                text_element.SetLayer(self.highlight_layer)
                            text_element.SetColor(self.highlight_color)
                            
                except Exception as e:
                    print(f"Warning: Could not highlight element: {e}")
                    continue
            
            print(f"Successfully highlighted {highlighted_count} missing elements.")
            
        except Exception as e:
            print(f"Error highlighting missing elements: {e}")
            import traceback
            traceback.print_exc()
        
        return highlighted_count

    def compare_color_sets(self, color1: abe.Color, color2: abe.Color, 
                          color1_name: str = "Set 1", color2_name: str = "Set 2") -> Dict:
        """
        Compare all elements of color1 against all elements of color2 across all open documents.
        
        Args:
            color1: First color to compare
            color2: Second color to compare
            color1_name: Name for first color set (for reporting)
            color2_name: Name for second color set (for reporting)
            
        Returns:
            Dictionary containing comparison results
        """
        results = {
            'color1': {'name': color1_name, 'color': color1, 'elements': []},
            'color2': {'name': color2_name, 'color': color2, 'elements': []},
            'common': [],
            'only_in_color1': [],
            'only_in_color2': [],
            'similar_pairs': [],
            'different_pairs': [],
            'missing_in_color2': [],
            'missing_in_color1': [],
            'summary': {}
        }
        
        try:
            # Get all elements of each color
            print(f"Finding all elements with {color1_name} color...")
            elements1 = self.get_all_3d_elements_by_color(color1)
            print(f"Found {len(elements1)} elements with {color1_name} color")
            
            print(f"Finding all elements with {color2_name} color...")
            elements2 = self.get_all_3d_elements_by_color(color2)
            print(f"Found {len(elements2)} elements with {color2_name} color")
            
            # Store element info
            results['color1']['elements'] = [
                {'signature': self.create_element_signature(el), 'info': el} 
                for el in elements1
            ]
            results['color2']['elements'] = [
                {'signature': self.create_element_signature(el), 'info': el} 
                for el in elements2
            ]
            
            # Create signature dictionaries
            signatures1 = {el['signature']: el['info'] for el in results['color1']['elements']}
            signatures2 = {el['signature']: el['info'] for el in results['color2']['elements']}
            
            # Find common, only in 1, only in 2
            common_signatures = set(signatures1.keys()) & set(signatures2.keys())
            only_in_1 = set(signatures1.keys()) - set(signatures2.keys())
            only_in_2 = set(signatures2.keys()) - set(signatures1.keys())
            
            # Store missing elements with their properties
            results['missing_in_color2'] = [
                signatures1[sig] for sig in only_in_1
            ]
            results['missing_in_color1'] = [
                signatures2[sig] for sig in only_in_2
            ]
            
            # Check for similar but not identical elements
            similar_pairs = []
            different_pairs = []
            
            for sig1 in only_in_1:
                for sig2 in only_in_2:
                    el1 = signatures1[sig1]
                    el2 = signatures2[sig2]
                    
                    is_similar, similarity = self.are_elements_similar(el1, el2)
                    if is_similar:
                        similar_pairs.append({
                            'element1': sig1,
                            'element2': sig2,
                            'similarity': similarity
                        })
                    elif similarity > 0.5:
                        similar_pairs.append({
                            'element1': sig1,
                            'element2': sig2,
                            'similarity': similarity
                        })
            
            # Check common signatures for geometric differences
            for sig in common_signatures:
                el1 = signatures1[sig]
                el2 = signatures2[sig]
                
                is_similar, similarity = self.are_elements_similar(el1, el2)
                if not is_similar:
                    different_pairs.append({
                        'element1': sig,
                        'element2': sig,
                        'similarity': similarity
                    })
            
            # Populate results
            results['common'] = list(common_signatures)
            results['only_in_color1'] = list(only_in_1)
            results['only_in_color2'] = list(only_in_2)
            results['similar_pairs'] = similar_pairs
            results['different_pairs'] = different_pairs
            
            # Generate summary
            results['summary'] = {
                'total_color1': len(elements1),
                'total_color2': len(elements2),
                'common_count': len(common_signatures),
                'only_in_color1_count': len(only_in_1),
                'only_in_color2_count': len(only_in_2),
                'similar_pairs_count': len(similar_pairs),
                'different_pairs_count': len(different_pairs),
                'missing_in_color2_count': len(results['missing_in_color2']),
                'missing_in_color1_count': len(results['missing_in_color1'])
            }
            
            # Highlight missing elements
            if len(results['missing_in_color2']) > 0:
                print(f"\nHighlighting elements from {color1_name} that are missing in {color2_name}...")
                highlighted = self.highlight_missing_elements(results['missing_in_color2'])
                results['summary']['highlighted_count'] = highlighted
            
        except Exception as e:
            results['error'] = str(e)
            print(f"Error comparing color sets: {e}")
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
        report.append("ALLPLAN COLOR-BASED MODEL COMPARISON REPORT")
        report.append("Comparing models by color across all open drawing files")
        report.append("=" * 70)
        report.append("")
        
        # Color set information
        color1 = results['color1']
        color2 = results['color2']
        report.append("COLOR SETS:")
        report.append(f"  {color1['name']}: {color1['color']}")
        report.append(f"  {color2['name']}: {color2['color']}")
        report.append("")
        
        # Summary
        summary = results['summary']
        report.append("SUMMARY:")
        report.append(f"  Total elements in {color1['name']}: {summary['total_color1']}")
        report.append(f"  Total elements in {color2['name']}: {summary['total_color2']}")
        report.append(f"  Common elements: {summary['common_count']}")
        report.append(f"  Only in {color1['name']}: {summary['only_in_color1_count']}")
        report.append(f"  Only in {color2['name']}: {summary['only_in_color2_count']}")
        report.append(f"  Similar element pairs: {summary['similar_pairs_count']}")
        report.append(f"  Different element pairs: {summary['different_pairs_count']}")
        report.append("")
        
        # Missing elements
        report.append("MISSING ELEMENTS:")
        report.append(f"  Elements in {color1['name']} missing from {color2['name']}: {summary.get('missing_in_color2_count', 0)}")
        report.append(f"  Elements in {color2['name']} missing from {color1['name']}: {summary.get('missing_in_color1_count', 0)}")
        
        if 'highlighted_count' in summary:
            report.append(f"  Highlighted in documents: {summary['highlighted_count']}")
        report.append("")
        
        # Calculate percentages
        if summary['total_color1'] > 0 or summary['total_color2'] > 0:
            total_all = summary['total_color1'] + summary['total_color2']
            common_pct = (summary['common_count'] * 2 / total_all * 100) if total_all > 0 else 0
            report.append(f"  Match rate: {common_pct:.1f}%")
            report.append("")
        
        # Details - missing from color2
        if summary.get('missing_in_color2_count', 0) > 0:
            report.append(f"ELEMENTS IN {color1['name'].upper()} MISSING FROM {color2['name'].upper()}:")
            for i, item in enumerate(results['missing_in_color2'][:10]):
                props = item.get('properties', {})
                element_type = props.get('type', 'Unknown')
                doc_name = props.get('document', 'Unknown')
                if 'bbox_center' in props:
                    center = props['bbox_center']
                    report.append(f"  {i+1}. {element_type} in {doc_name} at ({center[0]:.2f}, {center[1]:.2f}, {center[2]:.2f})")
                else:
                    report.append(f"  {i+1}. {element_type} in {doc_name}")
            if summary['missing_in_color2_count'] > 10:
                report.append(f"  ... and {summary['missing_in_color2_count'] - 10} more")
            report.append("")
        
        # Details - missing from color1
        if summary.get('missing_in_color1_count', 0) > 0:
            report.append(f"ELEMENTS IN {color2['name'].upper()} MISSING FROM {color1['name'].upper()}:")
            for i, item in enumerate(results['missing_in_color1'][:10]):
                props = item.get('properties', {})
                element_type = props.get('type', 'Unknown')
                doc_name = props.get('document', 'Unknown')
                if 'bbox_center' in props:
                    center = props['bbox_center']
                    report.append(f"  {i+1}. {element_type} in {doc_name} at ({center[0]:.2f}, {center[1]:.2f}, {center[2]:.2f})")
                else:
                    report.append(f"  {i+1}. {element_type} in {doc_name}")
            if summary['missing_in_color1_count'] > 10:
                report.append(f"  ... and {summary['missing_in_color1_count'] - 10} more")
            report.append("")
        
        # Distribution across documents
        report.append("DISTRIBUTION ACROSS DOCUMENTS:")
        
        # Count elements per document for color1
        doc_counts1 = {}
        for item in results['color1']['elements']:
            doc_name = item['info'].get('properties', {}).get('document', 'Unknown')
            doc_counts1[doc_name] = doc_counts1.get(doc_name, 0) + 1
        
        for doc_name, count in sorted(doc_counts1.items()):
            report.append(f"  {color1['name']} in {doc_name}: {count}")
        
        # Count elements per document for color2
        doc_counts2 = {}
        for item in results['color2']['elements']:
            doc_name = item['info'].get('properties', {}).get('document', 'Unknown')
            doc_counts2[doc_name] = doc_counts2.get(doc_name, 0) + 1
        
        for doc_name, count in sorted(doc_counts2.items()):
            report.append(f"  {color2['name']} in {doc_name}: {count}")
        
        report.append("")
        report.append("=" * 70)
        report.append("HIGHLIGHTING:")
        report.append(f"  Elements from {color1['name']} missing in {color2['name']} have been")
        report.append("  highlighted with red spheres and 'MISSING' text labels on the")
        report.append("  'COLOR_COMPARISON_HIGHLIGHT' layer in their respective documents.")
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

    def get_color_from_user(self, prompt: str) -> Optional[abe.Color]:
        """
        Get a color from user input.
        
        Args:
            prompt: The prompt to display
            
        Returns:
            Color object or None
        """
        print(prompt)
        print("Enter color as R,G,B (e.g., 255,0,0 for red)")
        print("Or choose from common colors:")
        print("  1. Red (255,0,0)")
        print("  2. Green (0,255,0)")
        print("  3. Blue (0,0,255)")
        print("  4. Yellow (255,255,0)")
        print("  5. Cyan (0,255,255)")
        print("  6. Magenta (255,0,255)")
        print("  7. White (255,255,255)")
        print("  8. Black (0,0,0)")
        
        choice = input("Enter color choice (1-8) or R,G,B: ").strip()
        
        # Check for preset colors
        presets = {
            '1': (255, 0, 0),
            '2': (0, 255, 0),
            '3': (0, 0, 255),
            '4': (255, 255, 0),
            '5': (0, 255, 255),
            '6': (255, 0, 255),
            '7': (255, 255, 255),
            '8': (0, 0, 0),
        }
        
        if choice in presets:
            r, g, b = presets[choice]
            return abe.Color(r, g, b)
        
        # Parse R,G,B input
        try:
            parts = [x.strip() for x in choice.split(',')]
            if len(parts) == 3:
                r = int(parts[0])
                g = int(parts[1])
                b = int(parts[2])
                return abe.Color(r, g, b)
        except:
            pass
        
        print("Invalid color input.")
        return None


def main():
    """
    Main function to run the color-based comparison.
    """
    print("=" * 70)
    print("ALLPLAN COLOR-BASED 3D MODEL COMPARATOR")
    print("Compare models by color across all open drawing files")
    print("=" * 70)
    print()
    
    try:
        # Create comparator instance
        comparator = ColorModelComparator(tolerance=0.001)
        
        # Get current project
        project = abe.Document.GetCurrentProject()
        if not project:
            print("ERROR: No active project found.")
            print("Please open an Allplan project first.")
            return
        
        print(f"Current project: {project.GetName()}")
        print()
        
        # Get all open documents
        open_docs = comparator.get_all_open_documents()
        
        if len(open_docs) == 0:
            print("ERROR: No open drawing files found.")
            print("Please open at least one drawing file in your project.")
            return
        
        print(f"Found {len(open_docs)} open drawing file(s) in the project:")
        for i, doc in enumerate(open_docs, 1):
            name = doc.GetName() if doc else "Unknown"
            print(f"  {i}. {name}")
        print()
        
        # Get color sets from user
        print("Enter the colors for the two sets of models you want to compare:")
        print()
        
        color1 = comparator.get_color_from_user("First color set (e.g., existing models):")
        if not color1:
            return
        
        color2 = comparator.get_color_from_user("Second color set (e.g., proposed models):")
        if not color2:
            return
        
        color1_name = input("Name for first color set (e.g., 'Existing'): ").strip()
        if not color1_name:
            color1_name = f"Color1 (R{color1.Red}G{color1.Green}B{color1.Blue})"
        
        color2_name = input("Name for second color set (e.g., 'Proposed'): ").strip()
        if not color2_name:
            color2_name = f"Color2 (R{color2.Red}G{color2.Green}B{color2.Blue})"
        
        print()
        print(f"Comparing: {color1_name} vs {color2_name}")
        print("Finding all elements of each color across all open drawing files...")
        print()
        
        # Perform comparison
        results = comparator.compare_color_sets(color1, color2, color1_name, color2_name)
        
        # Generate and display report
        report = comparator.generate_report(results)
        print("\n" + report)
        
        # Ask if user wants to export
        export = input("\nExport report to file? (y/n): ").strip().lower()
        if export == 'y':
            default_filename = f"ColorComparison_{color1_name}_vs_{color2_name}.txt"
            print(f"\nReport will be saved as: {default_filename}")
            success = comparator.export_results_to_file(results, default_filename)
            if success:
                print(f"Report saved successfully!")
            else:
                print("Failed to save report.")
        
        print("\n" + "=" * 70)
        print("COMPARISON COMPLETE")
        print("Check your documents for highlighted missing elements!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
