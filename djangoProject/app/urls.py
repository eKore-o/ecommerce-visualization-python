from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard_stats/', views.dashboard_stats, name='dashboard_stats'),

    path('products/', views.get_products, name='products'),
    path('products/export/', views.export_products, name='export_products'),
    path('profile/', views.get_profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('products/filter_options/', views.get_filter_options, name='filter_options'),
    path('part1/data/', views.get_part1_data, name='get_part1_data'),
    path('part1/filtered/', views.get_part1_filtered, name='get_part1_filtered'),
    path('part1/export/', views.export_part1, name='export_part1'),
    path('part3/data/', views.get_part3_data, name='get_part3_data'),
    path('part3/filtered/', views.get_part3_filtered, name='get_part3_filtered'),
    path('part3/export/', views.export_part3, name='export_part3'),
    path('part2/data/', views.get_part2_data, name='get_part2_data'),
    path('part2/filtered/', views.get_part2_filtered, name='get_part2_filtered'),
    path('part2/export/', views.export_part2, name='export_part2'),
    path('part4/data/', views.get_part4_data, name='get_part4_data'),
    path('part4/filtered/', views.get_part4_filtered, name='get_part4_filtered'),
    path('part4/export/', views.export_part4, name='export_part4'),
    path('part5/data/', views.get_part5_data, name='get_part5_data'),
    path('part5/export/', views.export_part5, name='export_part5'),
    path('part6/data/', views.get_part6_data, name='get_part6_data'),
    path('part6/export/', views.export_part6, name='export_part6'),
    path('part7/data/', views.get_part7_data, name='get_part7_data'),
    path('part7/filtered/', views.get_part7_filtered, name='get_part7_filtered'),
    path('part7/export/', views.export_part7, name='export_part7'),
    path('predict_pay_count/', views.predict_pay_count, name='predict_pay_count'),
    path('cluster_analysis/', views.cluster_analysis, name='cluster_analysis'),
    path('products/detail/<int:product_id>/', views.get_product_detail, name='get_product_detail'),
    path('chat/',views.chat_deepseek, name='chat_deepseek'),
]