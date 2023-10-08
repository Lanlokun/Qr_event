# event_app/views.py

from rest_framework import viewsets
from .models import Event, Participant, AccessCoupon, CouponType, ParticipantType
from .serializers import EventSerializer, ParticipantSerializer, AccessCouponSerializer, CouponTypeSerializer, ParticipantTypeSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import UserRateThrottle
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import qrcode
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils import timezone



class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [IsAuthenticated]  # Ensure authentication

class AccessCouponViewSet(viewsets.ModelViewSet):
    queryset = AccessCoupon.objects.all()
    serializer_class = AccessCouponSerializer
    # permission_classes = [IsAuthenticated]  # Ensure authentication

class CouponTypeViewSet(viewsets.ModelViewSet):
    queryset = CouponType.objects.all()
    serializer_class = CouponTypeSerializer
    # permission_classes = [IsAuthenticated]  # Ensure authentication

class ParticipantTypeViewSet(viewsets.ModelViewSet):
    queryset = ParticipantType.objects.all()
    serializer_class = ParticipantTypeSerializer
    # permission_classes = [IsAuthenticated]  # Ensure authentication


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    # permission_classes = [IsAuthenticated]  # Ensure authentication

class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    


@throttle_classes([UserRateThrottle])
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.pk,
            'username': user.username,
            'token': token.key
        })
    else:
        # No backend authenticated the credentials
        return Response({
            'error': 'Invalid Credentials'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.auth.delete()  # 'auth' contains the token for DRF's TokenAuthentication
    return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def record_entrance(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    if not participant.in_event:
        participant.in_event = True
        participant.time_in = timezone.now()
        participant.save()
        return Response({'message': 'Entrance recorded successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Entrance has already been recorded.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def record_exit(request, participant_id):
    participant = get_object_or_404(Participant, pk=participant_id)
    if participant.in_event:
        participant.in_event = False
        participant.save()
        return Response({'message': 'Exit recorded successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Exit cannot be recorded. Ensure entrance is recorded first.'}, status=status.HTTP_400_BAD_REQUEST)


def generate_qr(data):
    print(data)
    """
    Generate a QR code image from the provided data.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img

def generate_qr_code(request, qr_code_reference):
    # Retrieve the participant based on the qr_code_reference
    participant = get_object_or_404(Participant, qr_code_reference=qr_code_reference)
    
    # Generate the QR code using the participant's UUID or qr_code_reference
    qr_img = generate_qr(str(participant.qr_code_reference))  # or participant.qr_code_reference, depending on how you generate QR codes
    
    # Prepare the QR code image as a response
    response = HttpResponse(content_type='image/png')
    qr_img.save(response, 'PNG')
    
    return response


def redeem_coupon(request, coupon_id):
    # Retrieve the coupon based on coupon_id
    coupon = get_object_or_404(AccessCoupon, pk=coupon_id)
    
    # Check if the coupon is already redeemed
    if coupon.redeemed:
        return JsonResponse({'message': 'Coupon has already been redeemed.'}, status=400)
    
    # Mark the coupon as redeemed and set the redeemed_at timestamp
    coupon.redeemed = True
    coupon.redeemed_at = timezone.now()
    coupon.save()
    
    return JsonResponse({'message': 'Coupon redeemed successfully.'})