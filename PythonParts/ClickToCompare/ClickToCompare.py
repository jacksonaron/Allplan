"""
Absolute simplest PythonPart - just runs when double-clicked
Compares Red vs Cyan models across all open drawing files
"""

# Import only what we absolutely need
import NemAll_Python_BaseElements as abe
import NemAll_Python_Geometry as geom

print("ClickToCompare script starting...")

# Define the two colors we want to compare
RED = abe.Color(255, 0, 0)    # Color ID 1
CYAN = abe.Color(0, 255, 255)  # Color ID 3

def colors_match(c1, c2, tol=5):
    """Check if two colors match"""
    try:
        return (abs(c1.Red - c2.Red) <= tol and 
                abs(c1.Green - c2.Green) <= tol and 
                abs(c1.Blue - c2.Blue) <= tol)
    except:
        return False

def get_open_docs():
    """Get all open drawing files"""
    docs = []
    try:
        all_docs = abe.Document.GetAllOpenDocuments()
        for d in all_docs:
            if d and d.GetDocumentType() == abe.DocumentType.Part:
                docs.append(d)
    except Exception as e:
        print(f"Error getting docs: {e}")
    return docs

def get_elements_by_color(doc, color):
    """Get all 3D elements of a specific color in a document"""
    elements = []
    if not doc:
        return elements
    
    try:
        # Get all elements
        all_els = abe.ModelElementFilter(doc)
        
        # Filter for 3D elements of the right color
        for el in all_els:
            try:
                el_color = getattr(el, 'GetColor', lambda: None)()
                if el_color and colors_match(el_color, color):
                    elements.append(el)
            except:
                pass
    except Exception as e:
        print(f"Error in doc {doc.GetName() if doc else '?'}: {e}")
    
    return elements

def get_bbox_center(el):
    """Get the center of an element's bounding box"""
    try:
        bbox = getattr(el, 'GetBoundingBox', lambda: None)()
        if bbox:
            min_p = bbox.Min
            max_p = bbox.Max
            return geom.Point3D(
                (min_p.X + max_p.X) / 2,
                (min_p.Y + max_p.Y) / 2,
                (min_p.Z + max_p.Z) / 2
            )
    except:
        pass
    return None

def create_marker(doc, point):
    """Create a red sphere marker"""
    try:
        sphere = abe.Sphere.Create(point, 0.1)
        if sphere:
            sphere.SetColor(abe.Color(255, 0, 0))
            sphere.SetFillColor(abe.Color(255, 0, 0))
    except Exception as e:
        print(f"Error creating marker: {e}")

def main():
    """Main function"""
    print("\n" + "="*50)
    print("CLICK TO COMPARE - Running...")
    print("="*50)
    
    # Get all open documents
    docs = get_open_docs()
    print(f"\nFound {len(docs)} open drawing file(s)")
    
    if len(docs) == 0:
        print("ERROR: No drawing files open! Open some and try again.")
        return
    
    # Collect all red and cyan elements
    all_red = []
    all_cyan = []
    
    for doc in docs:
        print(f"  Scanning: {doc.GetName() if hasattr(doc, 'GetName') else 'Unknown'}")
        all_red.extend(get_elements_by_color(doc, RED))
        all_cyan.extend(get_elements_by_color(doc, CYAN))
    
    print(f"\nFound {len(all_red)} RED elements")
    print(f"Found {len(all_cyan)} CYAN elements")
    
    if len(all_red) == 0 or len(all_cyan) == 0:
        print("\nWARNING: No elements found for one or both colors!")
        print("Make sure you have models colored RED or CYAN.")
        return
    
    # Simple comparison: find red elements without matching cyan
    # For simplicity, just compare by bounding box center (rounded to 3 decimals)
    red_positions = set()
    for el in all_red:
        center = get_bbox_center(el)
        if center:
            red_positions.add((round(center.X, 3), round(center.Y, 3), round(center.Z, 3)))
    
    cyan_positions = set()
    for el in all_cyan:
        center = get_bbox_center(el)
        if center:
            cyan_positions.add((round(center.X, 3), round(center.Y, 3), round(center.Z, 3)))
    
    # Find red positions not in cyan
    missing_positions = red_positions - cyan_positions
    
    print(f"\nRed elements missing in Cyan: {len(missing_positions)}")
    
    # Highlight missing positions
    if len(missing_positions) > 0:
        print("Highlighting missing elements...")
        for pos in missing_positions:
            # Find the document that contains this position
            # For simplicity, just use the first document
            if docs:
                create_marker(docs[0], geom.Point3D(pos[0], pos[1], pos[2]))
        print(f"Created {len(missing_positions)} markers")
    
    print("\n" + "="*50)
    print("DONE! Check for red spheres marking missing elements.")
    print("="*50 + "\n")

# Run when double-clicked
if __name__ == "__main__":
    main()
