from .models import Product, ProductMaterials, MaterialBatch


class MaterialRequirementsCalculator:
    def __init__(self, products_data):
        self.products_data = products_data
        self.result = []
        self.used_batch_ids = []

    def calculate(self):
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
                        self.used_batch_ids.append(material_batch.id)

                        available_qty = material_batch.remainder
                        deducted_qty = min(remaining_qty, available_qty)

                        product_material_data = {
                            "warehouse_id": material_batch.id,
                            "material_name": material.name,
                            "qty": deducted_qty,
                            "price": material_batch.price
                        }
                    else:
                        # If no batch is available, mark the material as unavailable
                        product_material_data = {
                            "warehouse_id": None,
                            "material_name": material.name,
                            "qty": remaining_qty,
                            "price": None
                        }
                        remaining_qty = 0

                    remaining_qty -= deducted_qty
                    product_info["product_materials"].append(product_material_data)

            self.result.append(product_info)

        return self.result