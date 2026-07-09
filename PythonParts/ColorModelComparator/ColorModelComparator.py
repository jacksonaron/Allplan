"""
Color Model Comparator - PythonPart Version
This is a proper PythonPart that can be double-clicked in the Allplan Library.
"""

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeometry
import NemAll_Python_IFW_Input as AllplanIFW
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter
from BuildingElement import BuildingElement
from typing import Dict, List, Tuple, Optional, Any
import math


class ColorModelComparator:
    """Main class for the PythonPart version."""
    
    def __init__(self):
        self.tolerance = 0.001
        self.highlight_color = AllplanBaseElements.Color(255, 0, 0)
        self.highlight_layer = None
        self.created_highlight_layer = False
        
    def check_allplan_version(self, build_ele: BuildingElement, version: float) -> bool:
        """Check if the Allplan version is supported."""
        return True

    def modify_control_properties(self, build_ele: BuildingElement, ctrl_prop_util, value_name: str, event_id: int, doc: AllplanElementAdapter.DocumentAdapter) -> bool:
        """Modify control properties."""
        return False

    def create_element(self, build_ele: BuildingElement, doc: AllplanElementAdapter.DocumentAdapter):
        """Create element - this is called when the PythonPart is run."""
        # Run the comparison when the PythonPart is started
        self.run_comparison(build_ele, doc)
        return None

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

    def run_comparison(self, build_ele: BuildingElement, doc: AllplanElementAdapter.DocumentAdapter):
        """Run the color comparison."""
        print("=" * 70)
        print("ALLPLAN COLOR MODEL COMPARATOR")
        print("Comparing 3D models by color across all open drawing files")
        print("=" * 70)
        
        try:
            # Get color values from building element
            color1 = AllplanBaseElements.Color(
                build_ele.Color1Red.value,
                build_ele.Color1Green.value,
                build_ele.Color1Blue.value
            )
            color2 = AllplanBaseElements.Color(
                build_ele.Color2Red.value,
                build_ele.Color2Green.value,
                build_ele.Color2Blue.value
            )
            color1_name = build_ele.Color1Name.value
            color2_name = build_ele.Color2Name.value
            
            print(f"\nComparing: {color1_name} (R{color1.Red}G{color1.Green}B{color1.Blue})")
            print(f"         vs {color2_name} (R{color2.Red}G{color2.Green}B{color2.Blue})")
            
            # Get all open documents
            open_docs = self.get_all_open_documents()
            if len(open_docs) == 0:
                print("No open drawing files found. Please open at least one drawing file.")
                return
            
            print(f"Found {len(open_docs)} open drawing file(s)")
            
            # Get elements by color
            print(f"\nFinding all elements with {color1_name} color...")
            elements1 = self.get_all_3d_elements_by_color(color1, open_docs)
            print(f"Found {len(elements1)} elements with {color1_name} color")
            
            print(f"Finding all elements with {color2_name} color...")
            elements2 = self.get_all_3d_elements_by_color(color2, open_docs)
            print(f"Found {len(elements2)} elements with {color2_name} color")
            
            if len(elements1) == 0 or len(elements2) == 0:
                print("No elements found for one or both colors. Check your color selection.")
                return
            
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
            
            # Store missing elements
            missing_in_color2 = [signatures1[sig] for sig in only_in_1]
            
            # Highlight missing
            if len(missing_in_color2) > 0:
                print(f"\nHighlighting {len(missing_in_color2)} elements from {color1_name} missing in {color2_name}...")
                highlighted = self.highlight_missing_elements(missing_in_color2)
                print(f"Highlighted {highlighted} elements")
            
            # Show results
            print("\n" + "=" * 70)
            print("RESULTS:")
            print(f"  {color1_name}: {len(elements1)} elements")
            print(f"  {color2_name}: {len(elements2)} elements")
            print(f"  Common: {len(common)}")
            print(f"  Only in {color1_name}: {len(only_in_1)}")
            print(f"  Only in {color2_name}: {len(only_in_2)}")
            print(f"  Missing from {color2_name}: {len(missing_in_color2)}")
            print("=" * 70)
            print("Check your documents for highlighted missing elements!")
            print("=" * 70)
            
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()


# This is required for PythonPart
ColorModelComparatorInstance = ColorModelComparator()
