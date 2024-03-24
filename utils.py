import ifcopenshell

def get_materials(model):
    materials = model.by_type("IfcMaterial")

    return materials

def get_material_layer_sets(model):
    material_layer_sets = model.by_type("IfcMaterialLayerSet")

    return material_layer_sets

def get_material_layer_set_usages(model):
    material_layer_set_usages = model.by_type("IfcMaterialLayerSetUsage")

    return material_layer_set_usages

def get_material_lists(model):
    material_list = model.by_type("IfcMaterialList")

    return material_list