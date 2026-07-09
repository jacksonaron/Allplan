"""
Simple Color Comparator - Minimal PythonPart
Compares Red (ID=1) vs Cyan (ID=3) models across all open drawing files.
No palette, no BuildingElement - just runs immediately when double-clicked.
"""

import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_Geometry as AllplanGeometry


# Allplan color ID to RGB mapping
ALLPLAN_COLORS = {
    1: (255, 0, 0),     # Red
    3: (0, 255, 255),   # Cyan
}


def colors_match(color1, color2, tolerance=5) -> bool:
    """Check if two colors match within a tolerance."""
    try:
        r1, g1, b1 = color1.Red, color1.Green, color1.Blue
        r2, g2, b2 = color2.Red, color2.Green, color2.Blue
        return (abs(r1 - r2) <= tolerance and 
                abs(g1 - g2) <= tolerance and 
                abs(b1 - b2) <= tolerance)
    except:
        return False


def get_all_open_documents() -> list:
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


def get_all_3d_elements_by_color(doc, color) -> list:
    """Get all 3D elements of a specific color in a document."""
    elements = []
    
    if not doc:
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
    
    try:
        all_elements = AllplanBaseElements.ModelElementFilter(doc)
        for element in all_elements:
            try:
                if hasattr(element, 'GetType') and element.GetType() in element_types_3d:
                    element_color = getattr(element, 'GetColor', lambda: None)()
                    if element_color and colors_match(element_color, color):
                        elements.append(element)
            except:
                continue
    except Exception as e:
        print(f"Error processing document: {e}")
    
    return elements


def get_element_signature(element) -> str:
    """Create a unique signature for an element based on its bounding box."""
    try:
        bbox = getattr(element, 'GetBoundingBox', lambda: None)()
        if bbox:
            min_point = bbox.Min
            max_point = bbox.Max
            center = (
                (min_point.X + max_point.X) / 2,
                (min_point.Y + max_point.Y) / 2,
                (min_point.Z + max_point.Z) / 2
            )
            dims = (
                max_point.X - min_point.X,
                max_point.Y - min_point.Y,
                max_point.Z - min_point.Z
            )
            element_type = element.GetType().name if hasattr(element.GetType(), 'name') else str(element.GetType())
            return f"{element_type}|{center[0]:.3f},{center[1]:.3f},{center[2]:.3f}|{dims[0]:.3f},{dims[1]:.3f},{dims[2]:.3f}"
    except:
        return str(id(element))


def create_highlight_layer(doc):
    """Create a special layer for highlighting."""
    try:
        layer_name = "COLOR_COMP_HIGHLIGHT"
        layer = AllplanBaseElements.Layer.Find(layer_name)
        if layer:
            return layer
        
        layer = AllplanBaseElements.Layer.Create(layer_name)
        if layer:
            layer.SetColor(AllplanBaseElements.Color(255, 0, 0))
            layer.SetLineStyle(1)
            layer.SetLineWidth(2)
            layer.SetVisible(True)
            layer.SetLocked(False)
            layer.SetPrintable(True)
            return layer
    except:
        return AllplanBaseElements.Layer.Find("Standard")


def highlight_element(doc, element):
    """Highlight a single element with a sphere."""
    try:
        bbox = getattr(element, 'GetBoundingBox', lambda: None)()
        if bbox:
            min_point = bbox.Min
            max_point = bbox.Max
            center = AllplanGeometry.Point3D(
                (min_point.X + max_point.X) / 2,
                (min_point.Y + max_point.Y) / 2,
                (min_point.Z + max_point.Z) / 2
            )
            
            layer = create_highlight_layer(doc)
            
            # Create sphere
            sphere = AllplanBaseElements.Sphere.Create(center, 0.1)
            if sphere:
                if layer:
                    sphere.SetLayer(layer)
                sphere.SetColor(AllplanBaseElements.Color(255, 0, 0))
                sphere.SetFillColor(AllplanBaseElements.Color(255, 0, 0))
                sphere.SetTransparency(0.5)
            
            # Create text label
            text = AllplanBaseElements.Text3D.Create(
                AllplanGeometry.Point3D(center.X, center.Y, center.Z + 0.2),
                "MISSING",
                0.1
            )
            if text:
                if layer:
                    text.SetLayer(layer)
                text.SetColor(AllplanBaseElements.Color(255, 0, 0))
                
    except Exception as e:
        print(f"Error highlighting: {e}")


def main():
    """Main function - runs when PythonPart is double-clicked."""
    print("=" * 60)
    print("SIMPLE COLOR COMPARATOR")
    print("Comparing Red (ID=1) vs Cyan (ID=3) models")
    print("=" * 60)
    
    try:
        # Get color objects
        color_red = AllplanBaseElements.Color(255, 0, 0)    # Red = ID 1
        color_cyan = AllplanBaseElements.Color(0, 255, 255)  # Cyan = ID 3
        
        # Get all open documents
        open_docs = get_all_open_documents()
        if len(open_docs) == 0:
            print("ERROR: No open drawing files found!")
            print("Please open at least one drawing file and try again.")
            return
        
        print(f"\nFound {len(open_docs)} open drawing file(s)")
        
        # Get all elements of each color
        print("\nFinding all RED elements...")
        all_red_elements = []
        for doc in open_docs:
            all_red_elements.extend(get_all_3d_elements_by_color(doc, color_red))
        print(f"Found {len(all_red_elements)} red elements")
        
        print("Finding all CYAN elements...")
        all_cyan_elements = []
        for doc in open_docs:
            all_cyan_elements.extend(get_all_3d_elements_by_color(doc, color_cyan))
        print(f"Found {len(all_cyan_elements)} cyan elements")
        
        if len(all_red_elements) == 0 or len(all_cyan_elements) == 0:
            print("\nWARNING: No elements found for one or both colors!")
            print("Make sure your models are colored RED or CYAN.")
            return
        
        # Create signatures for comparison
        red_signatures = {}
        for el in all_red_elements:
            sig = get_element_signature(el)
            red_signatures[sig] = el
        
        cyan_signatures = {}
        for el in all_cyan_elements:
            sig = get_element_signature(el)
            cyan_signatures[sig] = el
        
        # Find missing elements (in red but not in cyan)
        red_only = set(red_signatures.keys()) - set(cyan_signatures.keys())
        
        print(f"\nRESULTS:")
        print(f"  Red elements: {len(all_red_elements)}")
        print(f"  Cyan elements: {len(all_cyan_elements)}")
        print(f"  Common: {len(set(red_signatures.keys()) & set(cyan_signatures.keys()))}")
        print(f"  Red elements missing in Cyan: {len(red_only)}")
        
        # Highlight missing elements
        if len(red_only) > 0:
            print(f"\nHighlighting {len(red_only)} red elements that are missing in cyan...")
            for sig in red_only:
                element = red_signatures[sig]
                doc = getattr(element, 'GetDocument', lambda: None)()
                if doc:
                    highlight_element(doc, element)
            print("Done! Check your documents for red spheres marking missing elements.")
        else:
            print("\nNo red elements are missing from cyan!")
        
        print("\n" + "=" * 60)
        print("COMPARISON COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()


# This runs when the PythonPart is started
if __name__ == "__main__":
    main()
