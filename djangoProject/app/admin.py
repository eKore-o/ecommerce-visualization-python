from django.contrib import admin
from app.models import User, Data, LoginStatistics


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display   = ('id', 'username', 'email', 'user_text_short')
    search_fields  = ('username', 'email')
    list_per_page  = 20
    ordering       = ('id',)
    fields         = ('username', 'email', 'password', 'user_text')

    def user_text_short(self, obj):
        return (obj.user_text or '')[:40] + ('...' if obj.user_text and len(obj.user_text) > 40 else '')
    user_text_short.short_description = '个人简介'


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display   = ('id', 'title_short', 'shop', 'price', 'pay_count', 'ship_address', 'product_brand')
    search_fields  = ('title', 'shop', 'product_brand')
    list_filter    = ('ship_address', 'product_brand')
    list_per_page  = 20
    ordering       = ('-id',)
    readonly_fields = ('detail_url', 'image_url')
    fields         = (
        'title', 'shop', 'price', 'pay_count',
        'ship_address', 'product_brand',
        'selling_points', 'features',
        'detail_url', 'image_url',
    )

    def title_short(self, obj):
        return (obj.title or '')[:50] + ('...' if obj.title and len(obj.title) > 50 else '')
    title_short.short_description = '商品标题'


@admin.register(LoginStatistics)
class LoginStatisticsAdmin(admin.ModelAdmin):
    list_display  = ('id', 'date', 'login_count')
    ordering      = ('-date',)
    list_per_page = 30
