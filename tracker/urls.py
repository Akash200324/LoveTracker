from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Auth
    path('', views.login_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('google-login/', views.google_login_view, name='google_login'),
    path('verify-email/', views.verify_email_view, name='verify_email'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
    path('logout/', views.logout_view, name='logout'),

    # Password Reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             html_email_template_name='registration/password_reset_email_html.html'
         ), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),

    # Couple
    path('upload-images/', views.upload_couple_image, name='upload_images'),
    path('create-couple/', views.create_couple, name='create_couple'),
    path('join-couple/', views.join_couple, name='join_couple'),
    path('delete-image/<int:image_id>/', views.delete_couple_image, name='delete_couple_image'),


    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('no-partner/', views.no_partner_view, name='no_partner'),
    path('upload-image/', views.upload_couple_image, name='upload_couple_image'),
    path('update-date/', views.update_couple_date, name='update_couple_date'),
    path('dashboard/snap/upload/', views.dashboard_snap_upload, name='dashboard_snap_upload'),
    path('dashboard/snap/delete/<int:snap_id>/', views.dashboard_snap_delete, name='dashboard_snap_delete'),
    path('dashboard/milestone/add/', views.add_milestone, name='add_milestone'),
    path('dashboard/milestone/edit/<int:milestone_id>/', views.edit_milestone, name='edit_milestone'),
    path('dashboard/milestone/delete/<int:milestone_id>/', views.delete_milestone, name='delete_milestone'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/photo/', views.update_photo, name='update_photo'),
    path('profile/photo/remove/', views.remove_photo, name='remove_photo'),

    # MoodTracker
    path('mood/', views.yourmoodtracker, name='moodtracker'),
    path('mood/save/', views.save_mood, name='save_ajax'),
    path('partner-mood/', views.partner_mood_tracker, name='partner_mood'),

    # Movies
    path('movies/', views.movie_tracker, name='movie_tracker'),
    path('movies/add/', views.add_movie, name='add_movie'),
    path('movies/update/<int:pk>/', views.movie_update, name='movie_update'),
    path('movies/delete/<int:pk>/', views.movie_delete, name='movie_delete'),
    path('movies/<int:movie_id>/reviews/', views.movie_review_detail, name='movie_detail'),
    path('movies/<int:movie_id>/reviews/submit/', views.movie_review_detail, name='submit_review'),

    # Songs
    path('songs/', views.songs, name='songs'),
    path('songs/delete/<int:pk>/', views.song_delete, name='song_delete'),
    path('songs/playlist/delete/<int:pk>/', views.playlist_delete, name='playlist_delete'),
    path('songs/api/create-playlist/', views.create_playlist, name='create_playlist'),
    path('songs/api/edit-playlist/<int:pk>/', views.edit_playlist, name='edit_playlist'),
    path('songs/api/add-song/', views.add_song_api, name='add_song_api'),

    # Memories
    path('memories/', views.memories, name='memories'),
    path('memories/delete/<int:pk>/', views.memory_delete, name='memory_delete'),
    path('memories/<int:pk>/get/', views.memory_get, name='memory_get'),
    path('memories/<int:pk>/add-photo/', views.memory_add_photo, name='memory_add_photo'),
    path('memories/photo/delete/<int:photo_pk>/', views.memory_photo_delete, name='memory_photo_delete'),

    # Bucket List
    path('bucket/', views.bucket_list, name='bucket_list'),
    path('bucket/add/', views.bucket_add, name='bucket_add'),
    path('bucket/toggle/<int:pk>/', views.bucket_toggle_ajax, name='bucket_toggle_ajax'),
    path('bucket/delete/<int:pk>/', views.bucket_delete_ajax, name='bucket_delete_ajax'),
    path('bucket/toggle-page/<int:pk>/', views.bucket_toggle, name='bucket_toggle'),
    path('bucket/delete-page/<int:pk>/', views.bucket_delete, name='bucket_delete'),
    
    # Period Tracker
    path('period-tracker/', views.period_tracker, name='period_tracker'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)