# event_app/urls_api.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, ParticipantViewSet, RegisterViewSet, login_view, logout_view, CouponTypeViewSet, AccessCouponViewSet, ParticipantTypeViewSet, generate_qr_code, redeem_coupon, record_entrance, record_exit

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'participants', ParticipantViewSet)
router.register(r'register', RegisterViewSet),
router.register(r'coupon_types', CouponTypeViewSet),
router.register(r'access_coupons', AccessCouponViewSet),
router.register(r'participant_types', ParticipantTypeViewSet),

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('generate/<uuid:qr_code_reference>/', generate_qr_code, name='generate_qr_code'),
    path('redeem-coupon/<int:coupon_id>/', redeem_coupon, name='redeem-coupon'),
    path('entrance/<int:participant_id>/', record_entrance, name='record-entrance'),
    path('exit/<int:participant_id>/', record_exit, name='record-exit'),

]
