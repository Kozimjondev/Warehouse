from .models import Product, ProductMaterials, MaterialBatch


class MaterialRequirementsCalculator:
    def __init__(self, products_data):
        self.products_data = products_data
        self.result = []
        self.used_batch_ids = []

    def calculate(self):
        warehouse_quantities = {}  # Dictionary to track quantities used in each warehouse

        for product_data in self.products_data:
            product_id = product_data.get('product_id')
            product_qty = product_data.get('product_qty')

            product = Product.objects.filter(id=product_id).first()
            if not product:
                raise ValueError(f"Product with ID {product_id} not found")

            product_materials = ProductMaterials.objects.filter(product=product)
            product_info = {
                "product_name": product.name,
                "product_qty": product_qty,
                "product_materials": []
            }

            # Calculate required quantity for each material in the product
            for product_material in product_materials:
                material = product_material.material
                required_material_qty = product_qty * product_material.quantity
                remaining_qty = required_material_qty

                while remaining_qty > 0:
                    material_batch = MaterialBatch.objects.filter(material=material).exclude(
                        id__in=self.used_batch_ids
                    ).first()

                    if material_batch:
                        available_qty = material_batch.remainder

                        # Check if warehouse ID is used in the previous product
                        if material_batch.id in warehouse_quantities:
                            available_qty -= warehouse_quantities[material_batch.id]

                        deducted_qty = min(remaining_qty, available_qty)

                        product_material_data = {
                            "warehouse_id": material_batch.id,
                            "material_name": material.name,
                            "qty": int(deducted_qty),
                            "price": material_batch.price
                        }

                        # Append the material data to product_materials
                        product_info["product_materials"].append(product_material_data)

                        # Update remaining quantity
                        remaining_qty -= deducted_qty

                        # Add the batch ID to used_batch_ids
                        self.used_batch_ids.append(material_batch.id)
                        print(self.used_batch_ids)
                        # Update warehouse quantities
                        if material_batch.id in warehouse_quantities:
                            warehouse_quantities[material_batch.id] += deducted_qty
                        else:
                            warehouse_quantities[material_batch.id] = deducted_qty
                        # print(warehouse_quantities)
                    else:
                        # If no batch is available, mark the material as unavailable
                        product_material_data = {
                            "warehouse_id": None,
                            "material_name": material.name,
                            "qty": int(remaining_qty),
                            "price": None
                        }

                        # Append the material data to product_materials
                        product_info["product_materials"].append(product_material_data)

                        # Set remaining quantity to 0
                        remaining_qty = 0

            self.result.append(product_info)
            for product in self.result:
                product['product_materials'] = [material for material in product["product_materials"]
                                                if not (
                        material.get("qty") == 0
                )]

            # Reset used_batch_ids for the next product
            self.used_batch_ids = []

        return self.result
