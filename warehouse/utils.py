def adjust_material_quantities(products_data):
    for i in range(len(products_data)):
        for j in range(i + 1, len(products_data)):
            for material in products_data[i]["product_materials"]:
                for other_material in products_data[j]["product_materials"]:
                    if material["material_name"] == other_material["material_name"]:
                        if material["qty"] > other_material["qty"]:
                            material["qty"] -= other_material["qty"]
                            other_material["qty"] = 0
                        else:
                            other_material["qty"] -= material["qty"]
                            material["qty"] = 0
    return products_data
