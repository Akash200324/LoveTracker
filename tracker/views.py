import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Q
from django.views.decorators.http import require_POST
import random
from django.core.mail import send_mail

from .utils import send_push_message
import threading
from .models import (
    User, Couple, Activity, MovieTracker,MovieReview, SongMemory,
    Memory, MemoryPhoto, BucketList, StatusUpdate, CoupleImage,Profile,YourMoodEntry, DashboardSnap, Milestone,
    EmailVerificationOTP, PeriodCycle, SymptomLog, PushSubscription
)

from .forms import (
    RegisterForm, LoginForm, CoupleStartDateForm, JoinCoupleForm,
    MovieForm,MovieReviewForm, SongForm, MemoryForm, MemoryPhotoForm, YourMoodForm, BucketListForm, StatusForm
)


# ─── HELPERS ─────────────────────────────────────────────

def get_couple(user):
    # .filter().first() returns None if nothing is found,
    # and the first object if multiple are found. No more crashes.
    return Couple.objects.filter(
        Q(user1=user) | Q(user2=user)
    ).first()
from functools import wraps

def partner_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        couple = get_couple(request.user)
        if not couple or not couple.is_complete:
            return render(request, 'tracker/no_partner.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
def no_partner_view(request):
    return render(request, 'tracker/no_partner.html')


def notify_partner_background(partner, title, body, url):
    if not partner: return
    def _send():
        subs = partner.push_subscriptions.all()
        for sub in subs:
            send_push_message(sub, title, body, url)
    threading.Thread(target=_send).start()


def get_partner(user, couple):
    if not couple:
        return None
    # If the current user is user1, the partner must be user2 (and vice versa)
    return couple.user2 if couple.user1 == user else couple.user1
def log_activity(couple, user, activity_type, reference_id, title, description=''):
    Activity.objects.create(
        couple=couple,
        user=user,
        activity_type=activity_type,
        reference_id=reference_id,
        title=title,
        description=description
    )


# ─── AUTH ────────────────────────────────────────────────
def register_view(request):
    # If already logged in, just go to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return render(request, 'tracker/register.html', {'form': form})
            
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        
        # Save OTP to database
        EmailVerificationOTP.objects.create(email=email, otp=otp)
        
        # Send Email
        try:
            send_mail(
                'LoveTracker - Verify Your Email',
                f'Your verification code is: {otp}\n\nThis code will expire in 10 minutes.',
                'noreply@lovetracker.com',
                [email],
                fail_silently=False,
            )
        except Exception as e:
            # Delete OTP and show error if email fails
            EmailVerificationOTP.objects.filter(email=email).delete()
            messages.error(request, f"Failed to send email. Please check the EMAIL_HOST_PASSWORD in settings.py! Error: {e}")
            return render(request, 'tracker/register.html', {'form': form})
        
        # Store registration data in session temporarily
        request.session['reg_data'] = {
            'name': form.cleaned_data['name'],
            'email': email,
            'password': form.cleaned_data['password']
        }
        
        messages.success(request, f"We've sent a 6-digit code to {email}.")
        return redirect('verify_email')

    return render(request, 'tracker/register.html', {'form': form})

def verify_email_view(request):
    reg_data = request.session.get('reg_data')
    if not reg_data:
        messages.error(request, "Session expired. Please register again.")
        return redirect('register')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        email = reg_data['email']

        # Get latest valid OTP for this email
        otp_record = EmailVerificationOTP.objects.filter(email=email).order_by('-created_at').first()

        if otp_record and otp_record.is_valid() and otp_record.otp == entered_otp:
            # OTP is correct! Create the user.
            user = User.objects.create_user(
                username=email, 
                email=email, 
                name=reg_data['name']
            )
            user.set_password(reg_data['password'])
            user.save()

            # Clean up
            del request.session['reg_data']
            EmailVerificationOTP.objects.filter(email=email).delete()

            login(request, user)
            messages.success(request, f"Welcome to Love Tracker, {user.name}! 🎉")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid or expired code. Please try again.")

    return render(request, 'tracker/verify_email.html', {'email': reg_data.get('email')})

def resend_otp_view(request):
    reg_data = request.session.get('reg_data')
    if not reg_data:
        return JsonResponse({'status': 'error', 'message': 'Session expired.'}, status=400)

    email = reg_data['email']
    
    # Check if they requested an OTP in the last 60 seconds
    last_otp = EmailVerificationOTP.objects.filter(email=email).order_by('-created_at').first()
    if last_otp:
        time_diff = timezone.now() - last_otp.created_at
        if time_diff.total_seconds() < 60:
            return JsonResponse({
                'status': 'error', 
                'message': f'Please wait {int(60 - time_diff.total_seconds())}s before requesting again.'
            }, status=429)

    # Generate new OTP
    otp = str(random.randint(100000, 999999))
    EmailVerificationOTP.objects.create(email=email, otp=otp)
    
    try:
        send_mail(
            'LoveTracker - Your New Verification Code',
            f'Your new verification code is: {otp}\n\nThis code will expire in 10 minutes.',
            'noreply@lovetracker.com',
            [email],
            fail_silently=False,
        )
    except Exception as e:
        EmailVerificationOTP.objects.filter(otp=otp).delete()
        return JsonResponse({'status': 'error', 'message': f'Failed to send email. Please check your App Password.'}, status=500)
    
    return JsonResponse({'status': 'success', 'message': 'A new code has been sent!'})

def login_view(request):
    # If already logged in, just go to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # Using email as username for authentication
        user = authenticate(
            request,
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )

        if user:
            login(request, user)
            # ✅ Always redirect to dashboard; the dashboard logic handles couple status
            return redirect('dashboard')

        messages.error(request, 'Invalid email or password.')

    return render(request, 'tracker/login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login')

import json
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

@require_POST
def google_login_view(request):
    token = request.POST.get('credential')
    try:
        # NOTE: Replace with your actual Google Client ID from Google Cloud Console
        CLIENT_ID = '525174801876-jub4aj46k5pi50ceai2snjr6ut34mo9k.apps.googleusercontent.com'
        # Verification might fail if CLIENT_ID is invalid, but structurally this is correct
        try:
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), CLIENT_ID)
        except Exception as verify_err:
            return JsonResponse({'success': False, 'error': f'Token verification failed: {str(verify_err)}. Please set your real Google Client ID.'})

        email = idinfo['email']
        name = idinfo.get('name', email.split('@')[0])
        
        user = User.objects.filter(email=email).first()
        is_new = False
        if not user:
            user = User.objects.create_user(username=email, email=email, name=name)
            is_new = True
            
        login(request, user)
        if is_new:
            request.session['first_login'] = True
            
        return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Invalid token'})

# ─── COUPLE SETUP ────────────────────────────────────────

@login_required
def create_couple(request):
    # Check if user is already in a couple using the safe helper
    existing_couple = get_couple(request.user)
    if existing_couple:
        return redirect('dashboard')

    # Create the new couple
    couple = Couple.objects.create(user1=request.user)
    
    # Redirect back to where they clicked it from (profile or dashboard)
    return redirect(request.META.get('HTTP_REFERER', 'profile'))

# Updated join_couple to handle duplicates and self-linking
@login_required
def join_couple(request):
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()

        # 1. Use .filter().first() instead of .get() to prevent MultipleObjectsReturned crash
        couple = Couple.objects.filter(invite_code=code).first()

        if not couple:
            return HttpResponse("Invalid Code ❌")

        # 2. Check if the couple is already full
        if couple.user2:
            return HttpResponse("This couple is already full ❌")

        # 3. Prevent a user from joining their own invite code
        if couple.user1 == request.user:
            return HttpResponse("You cannot join yourself! Share the code with your partner. ❌")

        # 4. Check if the current user is ALREADY in a different couple
        user_couple = get_couple(request.user)
        if user_couple and user_couple.user2 is not None:
            return HttpResponse("You are already linked to someone else! ❌")
            
        # If they have an empty solo couple row, delete it so they can properly join
        if user_couple and user_couple.user2 is None:
            user_couple.delete()

        # Success: Link them
        couple.user2 = request.user
        couple.save()

        return redirect('dashboard')

    return render(request, 'tracker/join_couple.html')


# ─── DASHBOARD ───────────────────────────────────────────

from django.urls import reverse  # Import this at the top


@login_required
def dashboard(request):
    couple = get_couple(request.user)
    print("CURRENT USER:", request.user)

    # Define the movie tracker path once
    movie_tracker_path = reverse('movie_tracker')

    show_welcome_message = request.session.pop('first_login', False)

    # ───── IF NO COUPLE ─────
    if not couple:
        stats = {
            'movies': 0,
            'songs': 0,
            'memories': 0,
            'bucket_total': 0,
            'bucket_done': 0,
            'movie_url': movie_tracker_path,  # Path added here
        }

        return render(request, 'tracker/dashboard.html', {
            'couple': None,
            'partner': None,
            'today_mood': None,
            'partner_mood': None,
            'activities': [],
            'my_status': None,
            'partner_status': None,
            'stats': stats,
            'images': [],
            'show_welcome_message': show_welcome_message,
            'vapid_public_key': getattr(settings, 'VAPID_PUBLIC_KEY', ''),
        })

    # ───── MAIN DATA ─────
    partner = get_partner(request.user, couple)
    today = timezone.now().date()

    # Moods and Statuses
    today_mood = YourMoodEntry.objects.filter(user=request.user, date=today).first()
    partner_mood = YourMoodEntry.objects.filter(user=partner, date=today).first() if partner else None
    
    def get_mood_completion(mood_entry):
        if not mood_entry:
            return 0
        filled = 0
        total = 6
        if getattr(mood_entry, 'sleep_hours', 0) > 0: filled += 1
        if getattr(mood_entry, 'energy_percent', 0) > 0: filled += 1
        if getattr(mood_entry, 'naughty_percent', 0) > 0: filled += 1
        if getattr(mood_entry, 'stress_percent', 0) > 0: filled += 1
        if getattr(mood_entry, 'mood_type', ''): filled += 1
        if getattr(mood_entry, 'journal_text', '').strip(): filled += 1
        return int((filled / total) * 100)

    my_mood_completion = get_mood_completion(today_mood)
    partner_mood_completion = get_mood_completion(partner_mood)

    activities = Activity.objects.filter(couple=couple).select_related('user')[:20]
    my_status = StatusUpdate.objects.filter(user=request.user, is_active=True).select_related('user').first()
    partner_status = StatusUpdate.objects.filter(user=partner, is_active=True).select_related('user').first() if partner else None

    # Calculate Stats
    all_movies = MovieTracker.objects.filter(couple=couple)
    stats = {
        'movies': all_movies.exclude(status='dropped').count(),
        'movie_url': movie_tracker_path,  # ✅ Added the path here
        'songs': SongMemory.objects.filter(couple=couple).count(),
        'memories': Memory.objects.filter(couple=couple).count(),
        'bucket_total': BucketList.objects.filter(couple=couple).count(),
        'bucket_done': BucketList.objects.filter(couple=couple, is_completed=True).count(),
        # Added calculation for your progress bar logic
        'movie_progress': (all_movies.filter(
            status__in=['watching', 'completed']).count() / all_movies.count() * 100) if all_movies.count() > 0 else 0
    }

    images = couple.images.all() if couple else []

    recent_memories = DashboardSnap.objects.filter(couple=couple).select_related('couple').order_by('-added_at')[:30]

    bucket_items = BucketList.objects.filter(couple=couple)
    milestones = Milestone.objects.filter(couple=couple).order_by('date')
    
    current_phase = "Track Cycles"
    from .models import PeriodCycle
    cycles = PeriodCycle.objects.filter(couple=couple).order_by('-start_date')
    if cycles.exists():
        current_cycle = cycles.first()
        delta_days = (today - current_cycle.start_date).days
        cycle_len = current_cycle.cycle_length or 28
        period_len = current_cycle.period_length or 5
        if delta_days >= cycle_len:
            current_phase = "Late"
        else:
            current_day = (delta_days % cycle_len) + 1
            if current_day <= period_len:
                current_phase = "Menstrual"
            elif current_day <= cycle_len - 15:
                current_phase = "Follicular"
            elif current_day <= cycle_len - 12:
                current_phase = "Ovulation"
            else:
                current_phase = "Luteal"

    return render(request, 'tracker/dashboard.html', {
        'couple': couple,
        'partner': partner,
        'today_mood': today_mood,
        'partner_mood': partner_mood,
        'activities': activities,
        'my_status': my_status,
        'partner_status': partner_status,
        'stats': stats,
        'current_phase': current_phase,
        'images': images,
        'recent_memories': recent_memories,
        'bucket_items': bucket_items,
        'milestones': milestones,
        'my_mood_completion': my_mood_completion,
        'partner_mood_completion': partner_mood_completion,
        'show_welcome_message': show_welcome_message,
            'vapid_public_key': getattr(settings, 'VAPID_PUBLIC_KEY', ''),
        'total': all_movies.count(),
        'completed': all_movies.filter(status='completed'),
        'watching': all_movies.filter(status='watching'),
    })

@login_required
@require_POST
def add_milestone(request):
    couple = get_couple(request.user)
    if not couple:
        return redirect('dashboard')
    
    date_str = request.POST.get('date')
    title = request.POST.get('title')
    description = request.POST.get('description', '')
    icon = request.POST.get('icon', '💞')
    
    if date_str and title:
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            Milestone.objects.create(
                couple=couple,
                added_by=request.user,
                title=title,
                description=description,
                date=date_obj,
                icon=icon[:10]
            )
        except ValueError:
            pass # Invalid date
            
    return redirect('dashboard')

@login_required
@require_POST
def edit_milestone(request, milestone_id):
    couple = get_couple(request.user)
    if not couple:
        return redirect('dashboard')
    
    milestone = get_object_or_404(Milestone, id=milestone_id, couple=couple)
    
    date_str = request.POST.get('date')
    title = request.POST.get('title')
    description = request.POST.get('description', '')
    icon = request.POST.get('icon', '💞')
    
    if date_str and title:
        try:
            milestone.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            milestone.title = title
            milestone.description = description
            milestone.icon = icon[:10]
            milestone.save()
        except ValueError:
            pass
            
    return redirect('dashboard')

@login_required
@require_POST
def delete_milestone(request, milestone_id):
    couple = get_couple(request.user)
    if couple:
        milestone = get_object_or_404(Milestone, id=milestone_id, couple=couple)
        milestone.delete()
    return redirect('dashboard')
@login_required
def update_couple_date(request):
    if request.method == "POST":
        new_date = request.POST.get('start_date')
        name1 = request.POST.get('name1')
        name2 = request.POST.get('name2')

        couple = Couple.objects.filter(Q(user1=request.user) | Q(user2=request.user)).first()

        if couple:
            if new_date:
                try:
                    couple.start_date = datetime.strptime(new_date, "%Y-%m-%d").date()
                except ValueError:
                    return JsonResponse({'status': 'error', 'message': 'Invalid date format'}, status=400)
            
            if name1:
                couple.user1.name = name1.strip()
                couple.user1.save()
            if name2 and couple.user2:
                couple.user2.name = name2.strip()
                couple.user2.save()
            
            couple.save()
            return JsonResponse({
                'status': 'success', 
                'new_date': str(couple.start_date) if couple.start_date else '',
                'name1': couple.user1.name,
                'name2': couple.user2.name if couple.user2 else 'Partner'
            })

        return JsonResponse({'status': 'error', 'message': 'Couple not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Only POST allowed'}, status=405)

@login_required
def upload_couple_image(request):
    if request.method == "POST":
        couple = get_couple(request.user)

        if not couple:
            return JsonResponse({"error": "No couple"}, status=400)

        files = request.FILES.getlist('images')

        for file in files:
            CoupleImage.objects.create(
                couple=couple,
                image=file
            )

        return JsonResponse({"success": True})

@login_required
def delete_couple_image(request, image_id):
    couple = get_couple(request.user)
    if not couple:
        return JsonResponse({"success": False, "error": "No couple found"}, status=400)
    image = get_object_or_404(CoupleImage, id=image_id, couple=couple)
    image.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.accepts('application/json'):
        return JsonResponse({"success": True})
    return redirect('dashboard')

@login_required
def dashboard_snap_upload(request):
    couple = get_couple(request.user)
    if not couple:
        return JsonResponse({'status': 'error', 'message': 'No couple found'}, status=400)
    
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        captions = request.POST.getlist('captions')
        
        for i, f in enumerate(files):
            cap = captions[i] if i < len(captions) else ''
            DashboardSnap.objects.create(couple=couple, image=f, caption=cap)
            
        notify_partner_background(get_partner(request.user, couple), f"{request.user.username} added a memory! 📸", "Check out the new memory in the gallery.", "/dashboard/#memories")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def dashboard_snap_delete(request, snap_id):
    couple = get_couple(request.user)
    snap = get_object_or_404(DashboardSnap, pk=snap_id, couple=couple)
    snap.delete()
    return JsonResponse({'status': 'success'})

# ─── profile ──────────────────────────────────────────────

@login_required
def profile_view(request):
    # Get or create the profile safely
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Use your helper to find the couple
    couple = get_couple(request.user)
    partner = get_partner(request.user, couple)

    context = {
        'profile': profile,
        'couple': couple,
        'partner': partner,

        }
    return render(request, 'tracker/profile.html', context)
@login_required
def update_profile(request):
    if request.method == 'POST':
        # Use get_or_create to ensure the profile exists before updating
        profile, created = Profile.objects.get_or_create(user=request.user)

        full_name = request.POST.get('full_name', '')
        if full_name:
            # The custom user model uses the 'name' field
            request.user.name = full_name
            # Also update first_name/last_name for standard Django admin compatibility
            names = full_name.split(' ')
            request.user.first_name = names[0]
            request.user.last_name = " ".join(names[1:]) if len(names) > 1 else ""
            request.user.save()

        age_val = request.POST.get('age')
        profile.age = age_val if age_val else None
        
        profile.bio = request.POST.get('bio')
        profile.gender = request.POST.get('gender')

        if 'profile_pic' in request.FILES:
            profile.image = request.FILES['profile_pic']

        profile.save()
        return redirect('profile')

@login_required
def remove_photo(request):
    profile = request.user.profile
    profile.image.delete()
    return redirect('profile')

@login_required
def update_photo(request):
    if request.method == 'POST' and request.FILES.get('profile_pic'):
        profile = request.user.profile
        profile.image = request.FILES['profile_pic']
        profile.save()
    return redirect('profile')

# ─── MoodTracker ──────────────────────────────────────────────
@login_required
@partner_required
def yourmoodtracker(request): # Renamed from mood_dashboard
    history = YourMoodEntry.objects.filter(user=request.user).order_by('-date')[:7]
    history = reversed(list(history))

    today_entry = YourMoodEntry.objects.filter(
        user=request.user,
        date=timezone.now().date()
    ).first()

    context = {
        'history': history,
        'today_entry': today_entry,
    }
    return render(request, 'tracker/Ymood_tracker.html', context)


@login_required
def save_mood(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            user_couple = getattr(request.user, 'couple', None)
            if not user_couple:
                user_couple = Couple.objects.filter(Q(user1=request.user) | Q(user2=request.user)).first()

            entry, created = YourMoodEntry.objects.update_or_create(
                user=request.user,
                date=timezone.now().date(),
                defaults={
                    'couple': user_couple,
                    'mood_type': data.get('mood_type', 'calm'),
                    'energy_percent': data.get('energy_percent', 70),
                    'naughty_percent': data.get('naughty_percent', 20),
                    'stress_percent': data.get('stress_percent', 20),
                    'sleep_hours': data.get('sleep_hours', 0.0),
                    'bedtime': data.get('bedtime', '11:00 PM'),
                    'wake_time': data.get('wake_time', '06:30 AM'),
                    'journal_text': data.get('journal_text', ''),
                }
            )
            return JsonResponse({'status': 'success', 'message': 'Mood saved! ✨'})

        except Exception as e:
            print(f"ERROR SAVING MOOD: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
@partner_required
def partner_mood_tracker(request):
    # 1. Identify the partner using your existing logic
    user = request.user
    couple = Couple.objects.filter(Q(user1=user) | Q(user2=user)).first()

    partner = None
    if couple:
        partner = couple.user2 if couple.user1 == user else couple.user1

    # 2. Get Partner's Mood Data
    history = []
    today_entry = None

    if partner:
        # Get last 7 days of partner's history
        history_query = YourMoodEntry.objects.filter(user=partner).order_by('-date')[:7]
        history = reversed(list(history_query))

        # Get partner's entry for today
        today_entry = YourMoodEntry.objects.filter(
            user=partner,
            date=timezone.now().date()
        ).first()

    context = {
        'partner': partner,
        'history': history,
        'today_entry': today_entry,
        'today': timezone.now().date(),
    }
    return render(request, 'tracker/Pmood_tracker.html', context)


# ─── MOVIES ──────────────────────────────────────────────

@login_required
@partner_required
def movie_tracker(request):
    # FIX: Use your helper instead of request.user.couple
    couple = get_couple(request.user)

    partner = get_partner(request.user, couple)

    form = MovieForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        movie = form.save(commit=False)
        movie.couple = couple  # This is now the object found by the helper
        movie.added_by = request.user
        movie.save()

        messages.success(request, f'"{movie.title}" added!')
        return redirect('movie_tracker')

    all_movies = MovieTracker.objects.filter(couple=couple).prefetch_related('movie_reviews__user')

    context = {
        'form': form,
        'partner': partner,
        'movies': all_movies.filter(movie_type='movie'),
        'series': all_movies.filter(movie_type__in=['tv', 'anime']),
        'watching': all_movies.filter(status='watching'),
        'watchlist': all_movies.filter(status='watchlist'),
        'completed': all_movies.filter(status='completed'),
        'dropped': all_movies.filter(status='dropped'),
        'total': all_movies.count(),
    }
    return render(request, 'tracker/movies.html', context)


@login_required
def add_movie(request):
    if request.method == "POST":
        try:
            couple = get_couple(request.user)  # Assuming this helper exists in your utils
            if not couple:
                return JsonResponse({'status': 'error', 'message': 'No couple found'}, status=400)

            data = json.loads(request.body)
            tmdb_id = data.get('tmdb_id')
            
            # Check for duplicates
            if tmdb_id and MovieTracker.objects.filter(couple=couple, tmdb_id=tmdb_id).exists():
                return JsonResponse({'status': 'error', 'message': 'Already added'})

            movie = MovieTracker.objects.create(
                couple=couple,
                added_by=request.user,
                title=data.get('title'),
                tmdb_id=tmdb_id,
                poster_url=data.get('poster_url'),
                year=data.get('year', ''),
                genre=data.get('genre', 'General'),
                imdb_rating=float(data.get('imdb_rating', 0.0) if data.get('imdb_rating') != 'N/A' else 0.0),
                movie_type=data.get('movie_type', 'movie'),
                status=data.get('status', 'watching')
            )
            return JsonResponse({'status': 'success', 'message': 'Added!', 'id': movie.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
@require_POST
def movie_update(request, pk):
    try:
        couple = get_couple(request.user)
        movie = get_object_or_404(MovieTracker, pk=pk, couple=couple)

        data = json.loads(request.body)
        new_status = data.get('status')

        if new_status in ['watching', 'completed', 'watchlist', 'dropped']:
            # If moving to "watching", make sure all other movies are moved back to watchlist
            if new_status == 'watching':
                MovieTracker.objects.filter(couple=couple, status='watching').update(status='watchlist')

            movie.status = new_status
            movie.save()
            return JsonResponse({'status': 'success', 'title': movie.title})

        return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
@require_POST
def movie_delete(request, pk):
    """Permanently delete a movie from the database."""
    try:
        couple = get_couple(request.user)
        movie = get_object_or_404(MovieTracker, pk=pk, couple=couple)
        title = movie.title
        movie.delete()
        return JsonResponse({'status': 'success', 'message': f'"{title}" deleted.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def movie_review_detail(request, movie_id):
    # 1. Fetch the movie or return 404
    movie = get_object_or_404(MovieTracker, id=movie_id)

    # 2. Check if the current user has already reviewed this movie
    user_review = MovieReview.objects.filter(movie=movie, user=request.user).first()

    # ─── HANDLE FORM SUBMISSION (POST) ───
    if request.method == 'POST':
        # instance=user_review allows updating an existing review instead of creating duplicates
        form = MovieReviewForm(request.POST, instance=user_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    # ─── RETURN JSON FOR MODAL (GET) ───
    partner_review = MovieReview.objects.filter(
        movie=movie,
        movie__couple=movie.couple
    ).exclude(user=request.user).first()

    partner = get_partner(request.user, movie.couple)
    partner_name = partner.name if partner else 'Partner'
    return JsonResponse({
        'status': 'success',
        'user_review': {
            'rating': user_review.rating if user_review else 0,
            'review_text': user_review.text if user_review else '',
        },
        'partner_review': {
            'rating': partner_review.rating if partner_review else 0,
            'review_text': partner_review.text if partner_review else '',
            'user_name': partner_name
        }
    })

# --- SONGS ---

from .models import Playlist
import re
import json
from django.conf import settings
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

def fetch_oembed_data(url):
    try:
        safe_url = quote(url, safe='')
        if 'youtube.com' in url or 'youtu.be' in url:
            resp = requests.get(f"https://www.youtube.com/oembed?url={safe_url}&format=json", timeout=5)
            if resp.status_code == 200:
                d = resp.json()
                return d.get('title', ''), d.get('author_name', ''), d.get('thumbnail_url', '')
        elif 'spotify.com' in url:
            resp = requests.get(f"https://open.spotify.com/oembed?url={safe_url}", timeout=5)
            if resp.status_code == 200:
                d = resp.json()
                return d.get('title', ''), 'Spotify', d.get('thumbnail_url', '')
    except Exception:
        pass
    return '', '', ''

@login_required
@partner_required
def songs(request):
    couple = get_couple(request.user)
    partner = get_partner(request.user, couple)
    all_songs = SongMemory.objects.filter(couple=couple).select_related('added_by')
    all_playlists = Playlist.objects.filter(couple=couple)
    return render(request, 'tracker/song_tracker.html', {'songs': all_songs, 'playlists': all_playlists, 'partner': partner})

@login_required
def create_playlist(request):
    couple = get_couple(request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        cover_image = request.FILES.get('cover_image')
        if name:
            playlist = Playlist.objects.create(
                couple=couple, 
                created_by=request.user, 
                name=name,
                cover_image=cover_image
            )
            return JsonResponse({
                'status': 'success', 
                'id': playlist.id, 
                'name': playlist.name,
                'cover_url': playlist.cover_image.url if playlist.cover_image else ''
            })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def edit_playlist(request, pk):
    couple = get_couple(request.user)
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, pk=pk, couple=couple)
        name = request.POST.get('name')
        cover_image = request.FILES.get('cover_image')
        
        if name:
            playlist.name = name
            
        if cover_image:
            playlist.cover_image = cover_image
            
        playlist.save()
        return JsonResponse({
            'status': 'success', 
            'id': playlist.id, 
            'name': playlist.name,
            'cover_url': playlist.cover_image.url if playlist.cover_image else playlist.cover_url
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def add_song_api(request):
    couple = get_couple(request.user)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            link = data.get('link', '')
            playlist_id = data.get('playlist_id')
            force_add = data.get('force_add', False)
            
            # Identify platform and type
            platform = ''
            track_id = ''
            item_type = 'song' # song or playlist
            
            if 'spotify.com/playlist/' in link:
                platform = 'spotify'
                item_type = 'playlist'
                match = re.search(r'playlist/([a-zA-Z0-9]+)', link)
                if match: track_id = match.group(1)
            elif 'youtube.com/playlist' in link:
                platform = 'youtube'
                item_type = 'playlist'
                match = re.search(r'list=([a-zA-Z0-9_-]+)', link)
                if match: track_id = match.group(1)
            elif 'spotify.com/track/' in link:
                platform = 'spotify'
                match = re.search(r'track/([a-zA-Z0-9]+)', link)
                if match: track_id = match.group(1)
            elif 'youtube.com/watch' in link or 'youtu.be/' in link:
                platform = 'youtube'
                if 'youtu.be/' in link:
                    match = re.search(r'youtu\.be/([a-zA-Z0-9_-]+)', link)
                else:
                    match = re.search(r'v=([a-zA-Z0-9_-]+)', link)
                if match: track_id = match.group(1)
                
            if not track_id:
                return JsonResponse({'status': 'error', 'message': 'Invalid Spotify or YouTube link'})
                
            # Fetch metadata
            title, artist, cover_url = fetch_oembed_data(link)
            if not title and not cover_url:
                return JsonResponse({'status': 'error', 'message': 'Could not access this link! Make sure the playlist or song is Public, not Private.'})
            if not title: title = 'Unknown Title'
            if not artist: artist = 'Unknown Artist'

            if item_type == 'playlist':
                if not playlist_id:
                    # Save as New Playlist
                    playlist = Playlist.objects.create(
                        couple=couple,
                        created_by=request.user,
                        name=title,
                        cover_url=cover_url,
                        is_external=(platform != 'spotify'), # If it's Spotify, we'll extract the tracks so it's internal!
                        platform=platform,
                        external_id=track_id
                    )
                else:
                    # Target an existing playlist
                    playlist = Playlist.objects.filter(id=playlist_id, couple=couple).first()
                    if not playlist:
                        return JsonResponse({'status': 'error', 'message': 'Invalid playlist'})
                
                # Auto-import tracks for Spotify playlists
                if platform == 'spotify':
                    try:
                        resp = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
                        if resp.status_code == 200:
                            soup = BeautifulSoup(resp.text, 'html.parser')
                            rows = soup.find_all('div', {'data-testid': 'track-row'})
                            for row in rows:
                                a_tag = row.find('a', href=re.compile(r'^/track/'))
                                if not a_tag: continue
                                t_id = a_tag['href'].replace('/track/', '')
                                title_elem = row.find('p', {'data-encore-id': 'listRowTitle'})
                                t_title = title_elem.text.strip() if title_elem else "Unknown Title"
                                artist_elem = row.find('p', {'data-encore-id': 'listRowDetails'})
                                t_artist = artist_elem.text.strip() if artist_elem else "Unknown Artist"
                                img_elem = row.find('img')
                                t_cover_url = img_elem['src'] if img_elem and 'src' in img_elem.attrs else ""
                                
                                song, created = SongMemory.objects.get_or_create(
                                    track_id=t_id,
                                    platform="spotify",
                                    defaults={
                                        'title': t_title,
                                        'artist': t_artist,
                                        'cover_url': t_cover_url,
                                        'added_by': request.user,
                                        'couple': couple
                                    }
                                )
                                song.playlists.add(playlist)
                    except Exception as e:
                        print("Error parsing spotify playlist:", e)

                return JsonResponse({'status': 'success', 'type': 'reload'})
            else:
                # Save as single Song
                save_track_id = track_id

                existing_song = SongMemory.objects.filter(couple=couple, track_id=save_track_id).first()
                
                if existing_song and not force_add:
                    return JsonResponse({'status': 'exists', 'message': 'This item is already in your tracker! Add it to this playlist anyway?', 'song_id': existing_song.id})
                    
                if existing_song and force_add:
                    song = existing_song
                else:
                    song = SongMemory.objects.create(
                        couple=couple,
                        added_by=request.user,
                        title=title,
                        artist=artist,
                        link=link,
                        platform=platform,
                        track_id=save_track_id,
                        cover_url=cover_url
                    )
                    
                if playlist_id:
                    playlist = Playlist.objects.filter(id=playlist_id, couple=couple).first()
                    if playlist:
                        song.playlists.add(playlist)
                        
                return JsonResponse({
                    'status': 'success',
                    'type': 'song',
                    'id': song.id,
                    'title': song.title,
                    'artist': song.artist,
                    'platform': song.platform,
                    'track_id': song.track_id,
                    'date': song.date_added.strftime('%b %d, %Y'),
                    'cover_url': song.cover_url
                })
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def song_delete(request, pk):
    couple = get_couple(request.user)
    song = get_object_or_404(SongMemory, pk=pk, couple=couple)
    song.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    messages.success(request, 'Song removed!')
    return redirect('songs')

@login_required
def playlist_delete(request, pk):
    couple = get_couple(request.user)
    playlist = get_object_or_404(Playlist, pk=pk, couple=couple)
    playlist.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    messages.success(request, 'Playlist removed!')
    return redirect('songs')



# --- MEMORIES ---

@login_required
@partner_required
def memories(request):
    couple = get_couple(request.user)
    if request.method == 'POST':
        form = MemoryForm(request.POST)
        if form.is_valid():
            memory = form.save(commit=False)
            memory.couple = couple
            memory.added_by = request.user
            memory.save()
            images = request.FILES.getlist('images')
            captions = request.POST.getlist('captions')
            for i, img in enumerate(images):
                cap = captions[i] if i < len(captions) else ''
                MemoryPhoto.objects.create(memory=memory, image=img, caption=cap)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                first_photo = memory.photos.first()
                return JsonResponse({'status': 'success', 'id': memory.pk, 'title': memory.title, 'date': memory.date.strftime('%B %d, %Y'), 'photo_count': memory.photos.count(), 'cover': first_photo.image.url if first_photo else ''})
            return redirect('memories')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    all_memories = Memory.objects.filter(couple=couple).select_related('added_by').prefetch_related('photos')
    return render(request, 'tracker/memory_tracker.html', {'memories': all_memories})

@login_required
def memory_get(request, pk):
    couple = get_couple(request.user)
    memory = get_object_or_404(Memory, pk=pk, couple=couple)
    photos = [{'id': p.pk, 'url': p.image.url, 'caption': p.caption} for p in memory.photos.all()]
    return JsonResponse({'status': 'success', 'id': memory.pk, 'title': memory.title, 'description': memory.description, 'date': memory.date.strftime('%B %d, %Y'), 'photos': photos})

@login_required
def memory_add_photo(request, pk):
    couple = get_couple(request.user)
    memory = get_object_or_404(Memory, pk=pk, couple=couple)
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        captions = request.POST.getlist('captions')
        created = []
        for i, img in enumerate(images):
            cap = captions[i] if i < len(captions) else ''
            photo = MemoryPhoto.objects.create(memory=memory, image=img, caption=cap)
            created.append({'id': photo.pk, 'url': photo.image.url, 'caption': photo.caption})
        return JsonResponse({'status': 'success', 'photos': created})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def memory_delete(request, pk):
    couple = get_couple(request.user)
    memory = get_object_or_404(Memory, pk=pk, couple=couple)
    memory.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    messages.success(request, 'Memory removed.')
    return redirect('memories')

@login_required
def memory_photo_delete(request, photo_pk):
    """Delete a single MemoryPhoto if it belongs to the current couple."""
    couple = get_couple(request.user)
    photo = get_object_or_404(MemoryPhoto, pk=photo_pk, memory__couple=couple)
    if request.method == 'POST':
        photo.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        return redirect('memories')
    return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)


# ─── BUCKET LIST ─────────────────────────────────────────

@login_required
@partner_required
def bucket_list(request):
    couple = get_couple(request.user)

    form = BucketListForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.couple = couple
        item.added_by = request.user
        item.save()
        return redirect('bucket_list')

    items = BucketList.objects.filter(couple=couple)

    return render(request, 'tracker/bucket_list.html', {
        'form': form,
        'items': items
    })
@login_required
def bucket_toggle(request, pk):
    item = get_object_or_404(BucketList, pk=pk, couple=request.user.couple)
    item.is_completed = not item.is_completed
    item.completed_date = timezone.now().date() if item.is_completed else None
    item.save()
    if item.is_completed:
        log_activity(request.user.couple, request.user, 'bucket', item.id,
                     f"✅ Completed: {item.title}")
        messages.success(request, f'"{item.title}" completed! 🎉')
    return redirect('bucket_list')


@login_required
def bucket_delete(request, pk):
    item = get_object_or_404(BucketList, pk=pk, couple=request.user.couple)
    item.delete()
    messages.success(request, 'Item removed.')
    return redirect('bucket_list')



# --- BUCKET LIST AJAX ---

@login_required
@require_POST
def bucket_add(request):
    couple = get_couple(request.user)
    if not couple:
        return JsonResponse({'status': 'error', 'message': 'No couple'}, status=400)
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        if not title:
            return JsonResponse({'status': 'error', 'message': 'Title required'}, status=400)
        item = BucketList.objects.create(
            couple=couple, added_by=request.user,
            title=title, priority=data.get('priority', 'medium'),
            target_date=data.get('target_date') or None,
        )
        return JsonResponse({'status': 'success', 'id': item.id, 'title': item.title, 'priority': item.priority, 'is_completed': False})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
@require_POST
def bucket_toggle_ajax(request, pk):
    couple = get_couple(request.user)
    item = get_object_or_404(BucketList, pk=pk, couple=couple)
    item.is_completed = not item.is_completed
    item.completed_date = timezone.now().date() if item.is_completed else None
    item.save()
    return JsonResponse({'status': 'success', 'is_completed': item.is_completed, 'id': item.id})


@login_required
@require_POST
def bucket_delete_ajax(request, pk):
    couple = get_couple(request.user)
    item = get_object_or_404(BucketList, pk=pk, couple=couple)
    item.delete()
    return JsonResponse({'status': 'success', 'id': pk})


def get_daily_message(day, phase, is_female, days_late=0, cycle_length=28):
    if phase == "Late":
        if days_late <= 2:
            return "Is your period delayed, or did you forget to log your new start date?"
        else:
            return f"Your period is delayed by {days_late} days. If you haven't logged it, consider taking a pregnancy test."
            
    ovulation_day = cycle_length - 14
    
    # Override for exact ovulation day or window
    if phase == "Ovulation":
        if day == ovulation_day:
            if is_female:
                return "Ovulation Day! High chance to get pregnant. This is the time for unprotected sex if trying for a baby. Otherwise, strictly use protection!"
            else:
                return "Ovulation Day! High chance of pregnancy. Have unprotected sex if trying for a baby, or strictly use protection if not!"
        elif day < ovulation_day:
            if is_female:
                return "Ovulation is approaching! High chance to get pregnant. Use protection if you aren't trying to conceive."
            else:
                return "Ovulation is approaching! High chance of pregnancy. Use protection if you aren't trying to conceive."
        else:
            if is_female:
                return "The fertile window is closing. An egg was likely released. Still a chance for pregnancy, so use protection if needed."
            else:
                return "The fertile window is closing. Still a high chance of pregnancy. Use protection if not trying to conceive."
                
    if phase == "Follicular" and day == 6:
        if is_female:
            return "Your period is over! Energy is returning. Pregnancy chance is low—have unprotected sex if you wish, or use protection to be safe."
        else:
            return "Her period is over and energy is returning! Pregnancy chance is low—have unprotected sex if you wish, or use protection."
            
    if phase == "Luteal" and day == cycle_length:
        if is_female:
            return "The final day of your cycle. Prepare for your period to start tomorrow."
        else:
            return "Final day of her cycle. Be her rock and prepare for tomorrow."

    # Female messages
    if is_female:
        female_msgs = {
            1: "Day 1: Your period has started. Your estrogen is low, so rest up and stay hydrated.",
            2: "Day 2: Flow might be heaviest today. Take it easy and use a heating pad for cramps.",
            3: "Day 3: You might start feeling a bit more energetic as your body adjusts.",
            4: "Day 4: Your period is winding down. Keep drinking plenty of water.",
            5: "Day 5: Flow is very light or ending. Your estrogen is beginning to slowly rise.",
            
            7: "Day 7: Estrogen is rising. You're likely feeling more outgoing and positive today.",
            8: "Day 8: Your skin might be glowing! A great day to be active.",
            9: "Day 9: Your testosterone is also rising. You might feel more confident and assertive.",
            10: "Day 10: Energy is peaking. A perfect time for a date night or hitting the gym.",
            11: "Day 11: Nearing your fertile window. If you aren't trying for a baby, be cautious with unprotected sex.",
            12: "Day 12: You are entering your fertile window. Pregnancy chances are increasing.",
            13: "Day 13: Your body is preparing to release an egg. Estrogen is at its peak!",
            
            17: "Day 17: Progesterone is rising, which can make you feel a bit sleepy or relaxed.",
            18: "Day 18: You might start experiencing food cravings. Listen to your body.",
            19: "Day 19: Energy levels might dip slightly as your body prepares for the next phase.",
            20: "Day 20: PMS symptoms might slowly begin to surface. Practice self-care.",
            21: "Day 21: Progesterone peaks. You might feel a bit bloated or sensitive.",
            22: "Day 22: Mood swings are normal today. Be gentle with yourself.",
            23: "Day 23: Your body is working hard. Get plenty of sleep tonight.",
            24: "Day 24: If you're feeling irritable, try some light yoga or a warm bath.",
            25: "Day 25: Nearing the end of the cycle. Skin might break out due to hormone shifts.",
            26: "Day 26: Energy is typically at its lowest. It's okay to cancel plans and rest.",
            27: "Day 27: Your period is just around the corner. Keep a pad or tampon handy.",
            28: "Day 28: The final day of your cycle. Prepare for your period to start tomorrow."
        }
        return female_msgs.get(day, "Your period is approaching. Listen to your body today and take care of yourself.")
    else:
        male_msgs = {
            1: "Day 1: Her period has started. Bring her some chocolate and offer a warm hug.",
            2: "Day 2: Cramps might be worst today. Offer to give her a gentle massage.",
            3: "Day 3: She might be feeling a bit better. Ask if she needs anything.",
            4: "Day 4: Her period is ending. A simple compliment goes a long way today.",
            5: "Day 5: Flow is ending. Plan a relaxing evening for both of you.",
            
            7: "Day 7: Her mood is likely lifting. A great day to spend quality time together.",
            8: "Day 8: She might be feeling extra confident. Plan a fun surprise for her.",
            9: "Day 9: Her energy is rising. Suggest an outdoor activity or workout together.",
            10: "Day 10: Energy is peaking! Take her out on a romantic date tonight.",
            11: "Day 11: She's nearing her fertile window. Be mindful of protection if you aren't trying for a baby.",
            12: "Day 12: She's entering her fertile window. Pregnancy chances are increasing.",
            13: "Day 13: Her estrogen is at its peak. Tell her she looks beautiful today.",
            
            17: "Day 17: Her progesterone is rising, making her sleepy. Let her rest if she needs it.",
            18: "Day 18: She might have food cravings. Surprise her with her favorite snack!",
            19: "Day 19: Her energy might dip today. Offer to help out with extra chores.",
            20: "Day 20: PMS might kick in soon. Be extra patient and understanding.",
            21: "Day 21: She might feel bloated or sensitive. Reassure her and be supportive.",
            22: "Day 22: Mood swings are normal today. A warm hug can fix a lot.",
            23: "Day 23: Her body is preparing for the next cycle. Make sure she gets good sleep.",
            24: "Day 24: She might be irritable. Give her space if she needs it, or offer a back rub.",
            25: "Day 25: Nearing her period. Bring home her favorite comfort food.",
            26: "Day 26: Her energy is lowest. Suggest a cozy movie night in.",
            27: "Day 27: Her period is almost here. Be ready with heating pads and snacks.",
            28: "Day 28: Final day of her cycle. Be her rock and prepare for tomorrow."
        }
        return male_msgs.get(day, "Be supportive and offer a warm hug today.")

@login_required
@partner_required
def period_tracker(request):
    couple = get_couple(request.user)
    
    # Ensure only female partner can submit data
    if request.method == 'POST' and request.user.profile.gender == 'Female':
        action = request.POST.get('action')
        
        if action == 'log_period':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            cycle_id = request.POST.get('cycle_id')
            cycle_length_str = request.POST.get('cycle_length')
            
            if start_date_str:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
                cycle_len = int(cycle_length_str) if cycle_length_str else 28
                
                if cycle_id:
                    cycle = PeriodCycle.objects.get(id=cycle_id, couple=couple)
                    cycle.start_date = start_date
                    cycle.end_date = end_date
                    cycle.cycle_length = cycle_len
                    if end_date:
                        cycle.period_length = (end_date - start_date).days + 1
                    cycle.save()
                else:
                    PeriodCycle.objects.create(
                        couple=couple,
                        start_date=start_date,
                        end_date=end_date,
                        cycle_length=cycle_len,
                        period_length=(end_date - start_date).days + 1 if end_date else 5
                    )
        elif action == 'log_symptom':
            cycle_id = request.POST.get('cycle_id')
            date_str = request.POST.get('date')
            if cycle_id and date_str:
                date_val = datetime.strptime(date_str, '%Y-%m-%d').date()
                cycle = PeriodCycle.objects.get(id=cycle_id, couple=couple)
                log, created = SymptomLog.objects.get_or_create(cycle=cycle, date=date_val)
                log.flow = request.POST.get('flow', log.flow)
                log.mood = request.POST.get('mood', log.mood)
                log.symptoms = request.POST.get('symptoms', log.symptoms)
                log.save()
                
        return redirect('period_tracker')

    # GET logic
    cycles = PeriodCycle.objects.filter(couple=couple).order_by('-start_date')
    current_cycle = cycles.first() if cycles.exists() else None
    
    today = timezone.localdate()
    current_phase = "Unknown"
    current_day = 0
    message = ""
    
    is_female = request.user.profile.gender == 'Female'

    if current_cycle:
        delta_days = (today - current_cycle.start_date).days
        cycle_len = current_cycle.cycle_length
        period_len = current_cycle.period_length
        
        # Check if they are late
        if delta_days >= cycle_len:
            days_late = delta_days - cycle_len + 1
            current_day = delta_days + 1
            current_phase = "Late"
            message = get_daily_message(current_day, current_phase, is_female, days_late=days_late)
        else:
            # Modulo math to find exact day in cycle (handles future start dates)
            # e.g., if delta_days is -18 (entered future date) and cycle_len is 28:
            # -18 % 28 = 10 -> current_day = 11
            current_day = (delta_days % cycle_len) + 1
            
            if current_day <= period_len:
                current_phase = "Menstrual"
            elif current_day <= cycle_len - 15:
                current_phase = "Follicular"
            elif current_day <= cycle_len - 12:
                current_phase = "Ovulation"
            else:
                current_phase = "Luteal"
                
            message = get_daily_message(current_day, current_phase, is_female, cycle_length=cycle_len)
            
    # Fetch symptom logs for the calendar
    symptoms = SymptomLog.objects.filter(cycle__couple=couple)
    symptoms_dict = {str(s.date): {'flow': s.flow, 'mood': s.mood, 'symptoms': s.symptoms} for s in symptoms}
    
    context = {
        'current_cycle': current_cycle,
        'current_phase': current_phase,
        'current_day': current_day,
        'daily_message': message,
        'is_female': is_female,
        'symptoms_json': json.dumps(symptoms_dict),
        'cycle_length': current_cycle.cycle_length if current_cycle else 28,
        'period_length': current_cycle.period_length if current_cycle else 5,
        'start_date_str': current_cycle.start_date.isoformat() if current_cycle else None,
    }
    
    return render(request, 'tracker/period_tracker.html', context)


from django.core.management import call_command

def auto_migrate(request):
    try:
        call_command('migrate')
        return HttpResponse("Database migrated successfully! You can now visit the homepage.")
    except Exception as e:
        return HttpResponse(f"Migration failed: {e}")

@login_required
@require_POST
def mark_tutorial_seen(request):
    try:
        profile = request.user.profile
        profile.has_seen_tutorial = True
        profile.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

from django.contrib.auth import logout
from django.contrib import messages

@login_required
@require_POST
def delete_account(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, 'Your account has been permanently deleted.')
    return redirect('login')

from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
@login_required
@require_POST
def save_push_subscription(request):
    try:
        data = json.loads(request.body)
        endpoint = data.get('endpoint')
        keys = data.get('keys', {})
        p256dh = keys.get('p256dh')
        auth = keys.get('auth')
        if not endpoint or not p256dh or not auth:
            return JsonResponse({'error': 'Invalid subscription data'}, status=400)
        
        PushSubscription.objects.update_or_create(
            user=request.user,
            endpoint=endpoint,
            defaults={'p256dh': p256dh, 'auth': auth}
        )
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def cron_inactivity_reminders(request):
    if getattr(settings, "CRON_SECRET", None) and request.headers.get("Authorization") != f"Bearer {settings.CRON_SECRET}":
        return HttpResponse("Unauthorized", status=401)
    
    now = timezone.now()
    subs = PushSubscription.objects.all()
    users_notified = 0
    for sub in subs:
        user = sub.user
        last_mood = YourMoodEntry.objects.filter(user=user).order_by("-date").first()
        if not last_mood or last_mood.date < now.date():
            send_push_message(
                sub, 
                "Missing You! 🥺", 
                "Hey, did you forget to add how your day was today? Your partner might be waiting to know!", 
                "/yourmoodtracker/"
            )
            users_notified += 1
            
    return JsonResponse({"status": "success", "notified": users_notified})
