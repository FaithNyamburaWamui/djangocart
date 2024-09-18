from django.shortcuts import render

# Create your views here.

# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework.response import Response
# from .service import Cart
# from material.models import Material  # Ensure you import the correct model
# from api.serializer import MaterialSerializer  # Ensure you import the correct serializer

# class CartAPI(APIView):
#     """
#     Single API to handle cart operations
#     """
#     def get(self, request, format=None):
#         cart = Cart(request)
#         cart_items = []
#         for item in cart:
#             material = item.get("product")
#             if material:
#                 # Serialize the material data
#                 serializer = MaterialSerializer(material)
#                 item["product"] = serializer.data
#             cart_items.append(item)
#         return Response(
#             {"data": cart_items,
#              "cart_total_price": cart.get_total_price()},
#             status=status.HTTP_200_OK
#         )

#     def post(self, request, **kwargs):
#         cart = Cart(request)
#         action = request.data.get("action")
#         material_id = request.data.get("id")
#         quantity = request.data.get("quantity", 1)
#         overide_quantity = request.data.get("overide_quantity", False)

#         try:
#             material = Material.objects.get(id=material_id)
#         except Material.DoesNotExist:
#             return Response(
#                 {"error": "Material not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         if action == "remove":
#             cart.remove(material)
#         elif action == "clear":
#             cart.clear()
#         else:  # Default action is to add the item to the cart
#             cart.add(
#                 material=material,
#                 quantity=quantity,
#                 overide_quantity=overide_quantity
#             )
        
#         return Response(
#             {"message": "cart updated"},
#             status=status.HTTP_202_ACCEPTED
#         )