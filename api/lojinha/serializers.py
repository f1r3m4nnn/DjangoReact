import json

from rest_framework_json_api import serializers

from .models import Customer, Item, Order, OrderDetail, Seller



class SellerSerializer(serializers.ModelSerializer):
    commission = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['id', 'image', 'name', 'phone', 'email', 'commission', 'created', 'modified']

    def get_commission(self, obj):
        return obj.calcCommission()



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'image', 'name', 'phone', 'email']



class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'title', 'stock', 'price', 'image', 'commission_rate']



class OrderDetailSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()
    item_id = serializers.PrimaryKeyRelatedField(source='item', queryset=Item.objects.all())
    quantity = serializers.IntegerField()


    class Meta:
        model = OrderDetail
        fields = ['id', 'item_id', 'item', 'quantity', 'price_at_sale', 'commission', 'discount', 'tax']



class OrderSerializer(serializers.ModelSerializer):

    details = OrderDetailSerializer(many=True, required=False)

    document_date = serializers.DateField()

    customer_name = serializers.SerializerMethodField(read_only=True)
    seller_name = serializers.SerializerMethodField(read_only=True)
   
    customer = serializers.SlugRelatedField(slug_field='name', queryset=Customer.objects.all(), write_only=True)
    seller = serializers.SlugRelatedField(slug_field='name', queryset=Seller.objects.all(), write_only=True)

    def get_customer_name(self, obj):
        return obj.customer.name if obj.customer else None
    

    def get_seller_name(self, obj):
        return obj.seller.name if obj.seller else None


    class Meta:
        model = Order
        fields = ('id',
                  'invoice_number',
                  'customer',
                  'document_date',
                  'customer_name',
                  'seller',
                  'seller_name',
                  'details'
        )


    def create(self, validated_data):
        print(validated_data, 'validated_data')
        details_data = validated_data.pop('details')
        order = Order.objects.create(**validated_data)
        for detail_data in details_data:
            OrderDetail.objects.create(order=order, **detail_data)
        return order


    def update(self, instance, validated_data):
        if 'details' in validated_data:
            new_details = validated_data.pop('details')
            old_details = (instance.details).all()

            for detail_data in new_details:
                detail, created = OrderDetail.objects.get_or_create(
                    id=detail_data.get('id', None),
                    defaults={
                        'order': instance,
                        'item': detail_data.get('item', None),
                        'quantity': detail_data.get('quantity', None),
                    }
                )
                if not created:
                    detail.item = detail_data.get('item', detail.item)
                    detail.quantity = detail_data.get('quantity', detail.quantity)
                    detail.save()

            # Remove os detalhes que não estão mais na lista
            for old_detail in old_details:
                if not any([old_detail.id == new_detail.get('id', None) for new_detail in new_details]):
                    old_detail.delete()

        instance.invoice_number = validated_data.get('invoice_number', instance.invoice_number)
        instance.document_date = validated_data.get('document_date', instance.document_date) 
        instance.customer = validated_data.get('customer', instance.customer)
        instance.seller = validated_data.get('seller', instance.seller)
        instance.save()

        return instance