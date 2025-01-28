from django.contrib import admin
from .models import UserProfile, Category, Product, Wishlist, Order, OrderItem, Review, Rating, Requisites, Delivery, \
    Payment


# Register the UserProfile model
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date')
    search_fields = ('user__username', 'phone')


# Register the Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'parent')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


# Register the Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'discount', 'category', 'is_active', 'created', 'updated')
    search_fields = ('name', 'slug', 'description')
    list_filter = ('category', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


# Register the Wishlist model
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key')
    search_fields = ('user__username', 'session_key')


# Register the Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'status')
    search_fields = ('user__username', 'status')
    list_filter = ('status', 'order_date')


# Register the OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'product', 'quantity')
    search_fields = ('user__username', 'product__name')


# Register the Review model
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'comment', 'review_date')
    search_fields = ('user__username', 'product__name', 'comment')
    list_filter = ('rating', 'review_date')


# Register the Rating model
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'value', 'created_time', 'ip_address')
    search_fields = ('user__username', 'product__name', 'ip_address')
    list_filter = ('value', 'created_time')


# Register the Requisites model
@admin.register(Requisites)
class RequisitesAdmin(admin.ModelAdmin):
    list_display = ('user', 'number')
    search_fields = ('user__username',)


# Register the Delivery model
@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')
    search_fields = ('user__username', 'address')


# Register the Payment model
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_date', 'status', 'requisite', 'address')
    search_fields = ('order__user__username', 'status')
    list_filter = ('status', 'payment_date')
