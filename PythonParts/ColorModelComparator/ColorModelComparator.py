"""
Color Model Comparator - PythonPart Version
Double-click in Library to run. Compares 3D models by color across all open drawing files.
"""

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
from typing import Dict, List, Tuple, Optional, Any
import math


class ColorModelComparatorPart:
    """Main class for the PythonPart version."""
    
    def __init__(self):
        self.tolerance = 0.001  # 1mm tolerance
        self.highlight_color = AllplanBaseElements.Color(255, 0, 0)  # Red
        self.highlight_layer = None
        self.created_highlight_layer = False
        
    def colors_match(self, color1, color2, tolerance=5) -> bool:
        """Check if two colors match within a tolerance."""
        try:
            r1, g1, b1 = color1.Red, color1.Green, color1.Blue
            r2, g2, b2 = color2.Red, color2.Green, color2.Blue
            return (abs(r1 - r2) <= tolerance and 
                    abs(g1 - g2) <= tolerance and 
                    abs(b1 - b2) <= tolerance)
        except:
            return False

    def get_all_open_documents(self) -> List:
        """Get all open drawing files."""
        open_docs = []
        try:
            all_docs = AllplanBaseElements.Document.GetAllOpenDocuments()
            for doc in all_docs:
                if doc and doc.GetDocumentType() == AllplanBaseElements.DocumentType.Part:
                    open_docs.append(doc)
        except Exception as e:
            print(f"Error getting documents: {e}")
        return open_docs

    def get_all_3d_elements_by_color(self, color, docs=None) -> List:
        """Get all 3D elements of a specific color across all documents."""
        elements = []
        
        if docs is None:
            docs = self.get_all_open_documents()
        
        if not docs:
            return elements
        
        element_types_3d = [
            AllplanBaseElements.EType.SmartSymbol3D,
            AllplanBaseElements.EType.SmartPart,
            AllplanBaseElements.EType.Extrusion,
            AllplanBaseElements.EType.Revolution,
            AllplanBaseElements.EType.Sweep,
            AllplanBaseElements.EType.Loft,
            AllplanBaseElements.EType.Pyramid,
            AllplanBaseElements.EType.Cone,
            AllplanBaseElements.EType.Sphere,
            AllplanBaseElements.EType.Torus,
            AllplanBaseElements.EType.Polyhedron,
            AllplanBaseElements.EType.Mesh,
            AllplanBaseElements.EType.Text3D,
            AllplanBaseElements.EType.Line,
            AllplanBaseElements.EType.Polyline3D,
            AllplanBaseElements.EType.Spline3D,
            AllplanBaseElements.EType.Circle3D,
            AllplanBaseElements.EType.Ellipse3D,
            AllplanBaseElements.EType.Arc3D,
            AllplanBaseElements.EType.Reinforcement,
            AllplanBaseElements.EType.EmbeddedElement,
        ]
        
        for doc in docs:
            try:
                all_elements = AllplanBaseElements.ModelElementFilter(doc)
                for element in all_elements:
                    try:
                        if hasattr(element, 'GetType') and element.GetType() in element_types_3d:
                            element_color = getattr(element, 'GetColor', lambda: None)()
                            if element_color and self.colors_match(element_color, color):
                                elements.append({
                                    'element': element,
                                    'document': doc,
                                    'color': element_color,
                                    'properties': self.get_element_properties(element)
                                })
                    except:
                        continue
            except Exception as e:
                print(f"Error processing document: {e}")
                continue
        
        return elements

    def get_element_properties(self, element) -> Dict:
        """Extract properties from an element."""
        props = {}
        try:
            props['type'] = element.GetType().name if hasattr(element.GetType(), 'name') else str(element.GetType())
            
            element_id = getattr(element, 'GetElementId', lambda: None)()
            if element_id:
                props['element_id'] = element_id
            
            bbox = getattr(element, 'GetBoundingBox', lambda: None)()
            if bbox:
                min_point = bbox.Min
                max_point = bbox.Max
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
            
            volume = getattr(element, 'GetVolume', lambda: None)()
            if volume is not None:
                props['volume'] = volume
            
            name = getattr(element, 'GetName', lambda: None)()
            if name:
                props['name'] = name
            
            layer = getattr(element, 'GetLayer', lambda: None)()
            if layer:
                props['layer'] = str(layer)
            
            doc = getattr(element, 'GetDocument', lambda: None)()
            if doc:
                props['document'] = doc.GetName() if hasattr(doc, 'GetName') else str(doc)
                
        except Exception as e:
            print(f"Warning: Could not extract properties: {e}")
        
        return props

    def create_element_signature(self, element_info) -> str:
        """Create a unique signature for an element."""
        props = element_info.get('properties', {})
        signature_parts = []
        
        signature_parts.append(f"type={props.get('type', 'Unknown')}")
        
        if 'bbox_center' in props:
            center = props['bbox_center']
            rounded_center = (round(center[0], 6), round(center[1], 6), round(center[2], 6))
            signature_parts.append(f"center={rounded_center[0]:.6f},{rounded_center[1]:.6f},{rounded_center[2]:.6f}")
        
        if 'bbox_dimensions' in props:
            dims = props['bbox_dimensions']
            rounded_dims = (round(dims[0], 6), round(dims[1], 6), round(dims[2], 6))
            signature_parts.append(f"dims={rounded_dims[0]:.6f},{rounded_dims[1]:.6f},{rounded_dims[2]:.6f}")
        
        if 'volume' in props:
            signature_parts.append(f"volume={props['volume']:.6f}")
        
        return "|".join(signature_parts)

    def are_elements_similar(self, element_info1, element_info2) -> Tuple[bool, float]:
        """Compare two elements and return similarity score."""
        try:
            props1 = element_info1.get('properties', {})
            props2 = element_info2.get('properties', {})
            
            if props1.get('type') != props2.get('type'):
                return False, 0.0
            
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
            
            if 'bbox_dimensions' in props1 and 'bbox_dimensions' in props2:
                dims1 = props1['bbox_dimensions']
                dims2 = props2['bbox_dimensions']
                dim_diffs = [abs(d1 - d2) for d1, d2 in zip(dims1, dims2)]
                max_dim_diff = max(dim_diffs) if dim_diffs else 0
                if max_dim_diff > self.tolerance:
                    max_dim = max(max(dims1), max(dims2)) if dims1 and dims2 else self.tolerance
                    similarity = 1.0 - (max_dim_diff / max(max_dim, self.tolerance))
                    return False, max(0.0, similarity)
            
            return True, 1.0
            
        except Exception as e:
            print(f"Warning: Could not compare elements: {e}")
            return False, 0.0

    def create_highlight_layer(self, doc) -> bool:
        """Create a special layer for highlighting."""
        try:
            layer_name = "COLOR_COMPARISON_HIGHLIGHT"
            layer = AllplanBaseElements.Layer.Find(layer_name)
            if layer:
                self.highlight_layer = layer
                return True
            
            layer = AllplanBaseElements.Layer.Create(layer_name)
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
                self.highlight_layer = AllplanBaseElements.Layer.Find("Standard")
                return True
            except:
                pass
        return False

    def highlight_missing_elements(self, missing_elements) -> int:
        """Highlight elements that are missing."""
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
                    
                    if not self.highlight_layer or self.highlight_layer.GetDocument() != doc:
                        if not self.create_highlight_layer(doc):
                            print(f"Warning: Could not create highlight layer in {doc.GetName()}")
                            continue
                    
                    if 'bbox_center' in props:
                        center = props['bbox_center']
                        x, y, z = center[0], center[1], center[2]
                        
                        sphere = AllplanBaseElements.Sphere.Create(
                            AllplanGeometry.Point3D(x, y, z),
                            0.1
                        )
                        
                        if sphere:
                            if self.highlight_layer:
                                sphere.SetLayer(self.highlight_layer)
                            sphere.SetColor(self.highlight_color)
                            sphere.SetFillColor(self.highlight_color)
                            sphere.SetTransparency(0.5)
                            highlighted_count += 1
                        
                        text = "MISSING"
                        text_element = AllplanBaseElements.Text3D.Create(
                            AllplanGeometry.Point3D(x, y, z + 0.2),
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
            return highlighted_count
            
        except Exception as e:
            print(f"Error highlighting: {e}")
            return 0

    def compare_color_sets(self, color1, color2, color1_name, color2_name):
        """Compare all elements of color1 against all elements of color2."""
        results = {
            'color1': {'name': color1_name, 'color': color1, 'count': 0},
            'color2': {'name': color2_name, 'color': color2, 'count': 0},
            'common': 0,
            'only_in_color1': 0,
            'only_in_color2': 0,
            'missing_in_color2': [],
            'summary': {}
        }
        
        try:
            print(f"Finding all elements with {color1_name} color...")
            elements1 = self.get_all_3d_elements_by_color(color1)
            results['color1']['count'] = len(elements1)
            print(f"Found {len(elements1)} elements with {color1_name} color")
            
            print(f"Finding all elements with {color2_name} color...")
            elements2 = self.get_all_3d_elements_by_color(color2)
            results['color2']['count'] = len(elements2)
            print(f"Found {len(elements2)} elements with {color2_name} color")
            
            if len(elements1) == 0 or len(elements2) == 0:
                print("No elements found for one or both colors. Check your color selection.")
                return results
            
            # Create signatures
            signatures1 = {}
            for el in elements1:
                sig = self.create_element_signature(el)
                signatures1[sig] = el
            
            signatures2 = {}
            for el in elements2:
                sig = self.create_element_signature(el)
                signatures2[sig] = el
            
            # Find common and missing
            common = set(signatures1.keys()) & set(signatures2.keys())
            only_in_1 = set(signatures1.keys()) - set(signatures2.keys())
            only_in_2 = set(signatures2.keys()) - set(signatures1.keys())
            
            results['common'] = len(common)
            results['only_in_color1'] = len(only_in_1)
            results['only_in_color2'] = len(only_in_2)
            
            # Store missing elements
            results['missing_in_color2'] = [signatures1[sig] for sig in only_in_1]
            
            # Highlight missing
            if len(results['missing_in_color2']) > 0:
                print(f"\nHighlighting {len(results['missing_in_color2'])} elements from {color1_name} missing in {color2_name}...")
                highlighted = self.highlight_missing_elements(results['missing_in_color2'])
                results['summary']['highlighted'] = highlighted
            
            # Generate summary
            results['summary'] = {
                'total_color1': len(elements1),
                'total_color2': len(elements2),
                'common': len(common),
                'only_in_color1': len(only_in_1),
                'only_in_color2': len(only_in_2),
                'missing_in_color2': len(results['missing_in_color2'])
            }
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        
        return results

    def show_results(self, results):
        """Display the comparison results."""
        print("\n" + "=" * 70)
        print("COLOR MODEL COMPARISON RESULTS")
        print("=" * 70)
        
        color1 = results['color1']
        color2 = results['color2']
        summary = results['summary']
        
        print(f"\n{color1['name']}: {summary['total_color1']} elements")
        print(f"{color2['name']}: {summary['total_color2']} elements")
        print(f"\nCommon elements: {summary['common']}")
        print(f"Only in {color1['name']}: {summary['only_in_color1']}")
        print(f"Only in {color2['name']}: {summary['only_in_color2']}")
        print(f"Elements from {color1['name']} missing in {color2['name']}: {summary['missing_in_color2']}")
        
        if 'highlighted' in summary:
            print(f"\nHighlighted in documents: {summary['highlighted']}")
        
        print("\n" + "=" * 70)
        print("Check your documents for highlighted missing elements!")
        print("=" * 70)

    def get_color_from_user(self, prompt):
        """Get color input from user."""
        print(f"\n{prompt}")
        print("Enter color as R,G,B (e.g., 255,0,0 for red)")
        print("Or choose from presets:")
        print("  1. Red (255,0,0)")
        print("  2. Green (0,255,0)")
        print("  3. Blue (0,0,255)")
        print("  4. Yellow (255,255,0)")
        print("  5. Cyan (0,255,255)")
        print("  6. Magenta (255,0,255)")
        
        choice = input("Enter choice (1-6) or R,G,B: ").strip()
        
        presets = {
            '1': (255, 0, 0),
            '2': (0, 255, 0),
            '3': (0, 0, 255),
            '4': (255, 255, 0),
            '5': (0, 255, 255),
            '6': (255, 0, 255),
        }
        
        if choice in presets:
            r, g, b = presets[choice]
            return AllplanBaseElements.Color(r, g, b)
        
        try:
            parts = [x.strip() for x in choice.split(',')]
            if len(parts) == 3:
                r = int(parts[0])
                g = int(parts[1])
                b = int(parts[2])
                return AllplanBaseElements.Color(r, g, b)
        except:
            pass
        
        print("Invalid input. Using red as default.")
        return AllplanBaseElements.Color(255, 0, 0)

    def run(self):
        """Main run method."""
        print("=" * 70)
        print("ALLPLAN COLOR MODEL COMPARATOR")
        print("Compare 3D models by color across all open drawing files")
        print("=" * 70)
        
        try:
            # Get current project
            project = AllplanBaseElements.Document.GetCurrentProject()
            if not project:
                print("No active project found. Please open a project first.")
                return
            
            print(f"\nCurrent project: {project.GetName()}")
            
            # Get all open documents
            open_docs = self.get_all_open_documents()
            if len(open_docs) == 0:
                print("No open drawing files found. Please open at least one drawing file.")
                return
            
            print(f"Found {len(open_docs)} open drawing file(s)")
            
            # Get color sets from user
            print("\nEnter the colors for the two sets of models to compare:")
            
            color1 = self.get_color_from_user("First color set (e.g., existing models):")
            color2 = self.get_color_from_user("Second color set (e.g., proposed models):")
            
            color1_name = input("Name for first color set (e.g., 'Existing'): ").strip()
            if not color1_name:
                color1_name = f"Color1 (R{color1.Red}G{color1.Green}B{color1.Blue})"
            
            color2_name = input("Name for second color set (e.g., 'Proposed'): ").strip()
            if not color2_name:
                color2_name = f"Color2 (R{color2.Red}G{color2.Green}B{color2.Blue})"
            
            # Perform comparison
            results = self.compare_color_sets(color1, color2, color1_name, color2_name)
            
            # Show results
            self.show_results(results)
            
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()


# Create and run the comparator when the PythonPart is started
if __name__ == "__main__":
    comparator = ColorModelComparatorPart()
    comparator.run()
