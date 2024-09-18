from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializer import MaterialSerializer
from material.models import Material
from .serializer import OrderSerializer
from order.models import Order
from cart.service import Cart
from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)



# Create your views here.

"""
    API View to handle Material-related requests.
    GET: Retrieve a list of all materials.
    POST: Create a new material entry.
      Handles GET requests to fetch all available materials.
        Serializes the material data and returns it in the response.
 """
        
class MaterialListView(APIView):
    def get(self, request):
        # Extract query parameters
        category = request.query_params.get('category', None)  # Filter by category
        brand = request.query_params.get('brand', None)  # Filter by brand
        min_price = request.query_params.get('min_price', None)  # Minimum price
        max_price = request.query_params.get('max_price', None)  # Maximum price
        sort_by = request.query_params.get('sort', 'price')  # Sorting option (default to price)

        # Start with all materials
        queryset = Material.objects.all()

        # Apply filters
        if category:
            queryset = queryset.filter(category_name=category)
        if brand:
            queryset = queryset.filter(brand_name=brand)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Apply sorting
        if sort_by in ['price', '-price', 'material_name', '-material_name']:
            queryset = queryset.order_by(sort_by)
        else:
            queryset = queryset.order_by('price')  # Default sorting

        # Serialize and return data
        serializer = MaterialSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, *args, **kwargs):
        serializer = MaterialSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class OrderListView(APIView):
    """
    List all orders or create a new order.
    """
    def get(self, request, format=None):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(APIView):
    """
    Retrieve, update or delete a specific order by ID.
    """
    def get(self, request, id, format=None):
        try:
            order = Order.objects.get(order_id=id)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        try:
            order = Order.objects.get(order_id=id)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        try:
            order = Order.objects.get(order_id=id)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CartListView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            cart = Cart(request)
            cart_data = list(cart)  # Ensure you're iterating over the cart correctly
            cart_total = cart.get_total_price()

            return Response({
                "data": cart_data,
                "cart_total_price": cart_total
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, **kwargs):
        cart = Cart(request)

        # Extract material data from request
        material_name = request.data.get('material_name')
        brand_name = request.data.get('brand_name')
        price = request.data.get('price', '0.00')  # Default price if not provided
        quantity = request.data.get('quantity', 1)  # Default quantity if not provided
        override_quantity = request.data.get('override_quantity', False)
        image = request.FILES.get('image')
        homeowner_id = request.data.get('homeowner_id')  # Obtain homeowner_id from request data


        # Ensure both material_name and brand_name are present
        if not material_name or not brand_name:
            logger.error("Missing required fields: 'material_name' or 'brand_name'")
            return Response({"error": "Missing required fields: 'material_name' and 'brand_name'"}, status=status.HTTP_400_BAD_REQUEST)

        # Look up the material by name and brand
        try:
            material_obj = Material.objects.get(material_name=material_name, brand_name=brand_name)
        except Material.DoesNotExist:
            logger.error("Material not found: %s, %s", material_name, brand_name)
            return Response({"error": "Material not found"}, status=status.HTTP_404_NOT_FOUND)
        except Material.MultipleObjectsReturned:
            logger.error("Multiple materials found with the same name and brand: %s, %s", material_name, brand_name)
            return Response({"error": "Multiple materials found with the same name and brand"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Error fetching material: %s", str(e))
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Example: Save the image (if needed)
        if image:
            # Handle image saving logic (e.g., save to a model or file system)
            pass

        # Continue processing the cart update logic
        try:
            cart.add(
                material={'id': material_obj.material_id, 'price': price},
                quantity=quantity,
                override_quantity=override_quantity
            )
            return Response({"message": "Cart updated"}, status=status.HTTP_202_ACCEPTED)

        except KeyError as e:
            logger.error("Missing required field: %s", str(e))
            return Response({"error": f"Missing required field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error("An error occurred while updating the cart: %s", str(e))
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

