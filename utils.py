import ifcopenshell

def extract_materials(model):
    ifc_file = model
    materials = set()
    for material in ifc_file.by_type("IfcMaterial"):
        materials.add(material.Name)
    return materials

def is_material_associated(association, material):
    """Check if the material is associated directly or via a layer set."""
    direct_association = association.RelatingMaterial == material
    layered_association = (association.RelatingMaterial.is_a("IfcMaterialLayerSetUsage") and 
                           association.RelatingMaterial.ForLayerSet == material)
    return direct_association or layered_association

def get_element_location(relatedObject):
    """Determine the spatial structure (location) of an element."""
    if not relatedObject.ContainedInStructure:
        return "Unknown Location"
    
    for rel_contained in relatedObject.ContainedInStructure:
        structure = rel_contained.RelatingStructure
        location = structure.LongName or structure.Name
        if structure.is_a("IfcSpace"):  # More specific space info
            location += f" in {structure.LongName or structure.Name}"
        return location
    return "Undefined Structure"

def find_used_in_elements(ifc_file, material):
    """Find all elements a given material is used in."""
    used_in_elements = set()
    for association in ifc_file.by_type("IfcRelAssociatesMaterial"):
        if is_material_associated(association, material):
            for relatedObject in association.RelatedObjects:
                element_type = relatedObject.is_a()
                element_id = relatedObject.GlobalId
                location = get_element_location(relatedObject)
                used_in_elements.add((element_type, element_id, location))
    return used_in_elements

def extract_material_usage(model):
    ifc_file = model
    material_usage_info = {}

    for material in ifc_file.by_type("IfcMaterial"):
        used_in_elements = find_used_in_elements(ifc_file, material)
        material_usage_info[material.Name] = used_in_elements

    return material_usage_info

def extract_dimensions(ifc_file, material):
    """Extract dimensions from material usage contexts."""
    dimensions = {}
    
    # Handling Material Layer Sets
    layer_sets = ifc_file.by_type("IfcMaterialLayerSet")
    for layer_set in layer_sets:
        for layer in layer_set.MaterialLayers:
            if layer.Material == material:
                dimensions["Layer Thickness"] = layer.LayerThickness or "Not specified"

    # Handling Material Profiles
    profile_sets = ifc_file.by_type("IfcMaterialProfileSet")
    for profile_set in profile_sets:
        for profile in profile_set.MaterialProfiles:
            if profile.Material == material:
                profile_def = profile.Profile
                if profile_def:
                    # Extract dimensions based on profile shape type
                    if profile_def.is_a("IfcRectangleProfileDef"):
                        dimensions["Width"] = profile_def.XDim
                        dimensions["Height"] = profile_def.YDim
                    elif profile_def.is_a("IfcCircleProfileDef"):
                        dimensions["Radius"] = profile_def.Radius
                    elif profile_def.is_a("IfcIProfileDef"):
                        dimensions["Overall Width"] = profile_def.OverallWidth
                        dimensions["Overall Depth"] = profile_def.OverallDepth
                        dimensions["Web Thickness"] = profile_def.WebThickness
                        dimensions["Flange Thickness"] = profile_def.FlangeThickness

    return dimensions
