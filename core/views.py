from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import WaitingUser, Room
import uuid

@login_required
def find_match(request):
    waiting = WaitingUser.objects.exclude(user=request.user).first()
    
    if waiting:
        # Found someone waiting
        room_id = str(uuid.uuid4())[:8]
        room = Room.objects.create(
            room_id=room_id,
            user1=waiting.user,
            user2=request.user
        )
        waiting.delete()
        return redirect(f'/room/{room_id}/')
    else:
        # Join waiting queue
        WaitingUser.objects.create(user=request.user)
        return render(request, 'core/waiting.html')

from django.shortcuts import render
import uuid

def anonymous_login(request):
    # Give each visitor a unique ID stored in session
    if not request.session.get('anonymous_id'):
        request.session['anonymous_id'] = str(uuid.uuid4())[:8]
    
    return render(request, 'core/index.html', {
        'user_id': request.session['anonymous_id']
    })

from django.shortcuts import redirect
from .models import WaitingUser, Room
import uuid

def start_match(request):
    anonymous_id = request.session.get('anonymous_id')
    if not anonymous_id:
        return redirect('/')
    
    # Look for someone waiting
    waiting = WaitingUser.objects.exclude(session_id=anonymous_id).first()
    
    if waiting:
        # Match found! Create room
        room_id = str(uuid.uuid4())[:8]
        Room.objects.create(
            room_id=room_id,
            user1_session=waiting.session_id,
            user2_session=anonymous_id
        )
        waiting.delete()
        return redirect(f'/room/{room_id}/')
    else:
        # No one waiting, add to queue
        WaitingUser.objects.create(session_id=anonymous_id)
        return render(request, 'core/waiting.html')


from django.http import JsonResponse
from .models import Room

def check_match(request):
    anonymous_id = request.session.get('anonymous_id')
    room = Room.objects.filter(user1_session=anonymous_id) | Room.objects.filter(user2_session=anonymous_id)
    room = room.first()
    if room:
        return JsonResponse({'room_id': room.room_id})
    return JsonResponse({'room_id': None})

# Check if match found (for auto-refresh on waiting page)
def check_match(request):
    anonymous_id = request.session.get('anonymous_id')
    if not anonymous_id:
        return JsonResponse({'room_id': None})
    
    room = Room.objects.filter(
        user1_session=anonymous_id
    ) | Room.objects.filter(
        user2_session=anonymous_id
    )
    room = room.first() 

    if room:
        return JsonResponse({'room_id': room.room_id})
    return JsonResponse({'room_id': None})

# The actual chat room
def room_view(request, room_id):
    anonymous_id = request.session.get('anonymous_id')
    
    try:
        room = Room.objects.get(room_id=room_id)
        
        # Check if this user is in this room
        if anonymous_id not in [room.user1_session, room.user2_session]:
            return redirect('/')

        # Get previous messages
        messages = Message.objects.filter(room=room).order_by('created_at')
        
        # Determine if this is user1 or user2 (for styling)
        is_user1 = (anonymous_id == room.user1_session)
        
        # Get the other person's ID (for display)
        other_user = room.user2_session if is_user1 else room.user1_session
        
    except Room.DoesNotExist:
        return redirect('/')

    return render(request, 'core/room.html', {
        'room_id': room_id,
        'messages': messages,
        'is_user1': is_user1,
        'other_user': other_user[:8]  # Show first 8 chars of their ID
    })

# Leave room - clean up
def leave_room(request, room_id):
    anonymous_id = request.session.get('anonymous_id')
    
    try:
        room = Room.objects.get(room_id=room_id)
        
        # Delete the room (or mark as inactive)
        room.delete()
        
        # Also delete any waiting queue entry for this user
        WaitingUser.objects.filter(session_id=anonymous_id).delete()
        
    except Room.DoesNotExist:
        pass
    
    return redirect('/')

# WebSocket endpoint (if using Channels)
def websocket_endpoint(request, room_id):
    # This is handled by consumers.py if using Channels
    # For now, just return 404 if someone tries to GET it
    from django.http import Http404
    raise Http404("WebSocket endpoint")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import RealSelfForm

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = RealSelfForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')  # After profile, go to dashboard
    else:
        form = RealSelfForm(instance=profile)
    
    return render(request, 'core/profile.html', {
        'form': form,
        'profile': profile,
        'is_complete': profile.is_complete()
    })


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models  # ← ADD THIS LINE
from .models import UserProfile, Room, WaitingUser

@login_required
def dashboard(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get recent rooms (past matches)
    recent_rooms = Room.objects.filter(
        models.Q(user1_session=request.user.username) | 
        models.Q(user2_session=request.user.username)
    ).order_by('-created_at')[:5]
    
    # Check if they're currently waiting
    is_waiting = WaitingUser.objects.filter(session_id=request.user.username).exists()
    
    # Get total matches count
    matches_count = Room.objects.filter(
        models.Q(user1_session=request.user.username) | 
        models.Q(user2_session=request.user.username)
    ).count()
    
    context = {
        'user': request.user,
        'profile': profile,
        'recent_rooms': recent_rooms,
        'is_waiting': is_waiting,
        'matches_count': matches_count,
        'profile_complete': profile.is_complete() if hasattr(profile, 'is_complete') else False,
    }
    
    return render(request, 'core/dashboard.html', context)


@login_required
def public_pages(request):
    return render(request, 'core/public_pages.html', {
        'user': request.user
    })