from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string


def generate_invite_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    avatar_color = models.CharField(max_length=7, default='#e91e8c')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True
    )

    def __str__(self):
        return self.name


class EmailVerificationOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Valid for 10 minutes
        return timezone.now() < self.created_at + timezone.timedelta(minutes=10)

    def __str__(self):
        return f"{self.email} - {self.otp}"


class Couple(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='couple_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='couple_as_user2')
    invite_code = models.CharField(max_length=8, unique=True, default=generate_invite_code)
    start_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user1.name} & {self.user2.name if self.user2 else 'Waiting...'}"

    @property
    def days_together(self):
        if self.start_date:
            return (timezone.now().date() - self.start_date).days
        return 0

    @property
    def is_complete(self):
        return self.user1 is not None and self.user2 is not None

class CoupleImage(models.Model):
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='couple_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.couple}"

class Profile(models.Model):
    # Changed 'on_submit' to 'on_delete'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)
    age = models.IntegerField(null=True, blank=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('mood', 'Mood'),
        ('memory', 'Memory'),
        ('movie', 'Movie'),
        ('song', 'Song'),
        ('bucket', 'Bucket List'),
        ('status', 'Status'),
    ]
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    reference_id = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.activity_type} by {self.user.name}"


class MovieTracker(models.Model):
    TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('tv', 'Series'),
        ('anime', 'Anime')
    ]

    STATUS_CHOICES = [
        ('watchlist', 'Watchlist'),
        ('watching', 'Watching'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped')
    ]

    # --- RELATIONSHIPS ---
    couple = models.ForeignKey('Couple', on_delete=models.CASCADE, related_name='movies')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_movies')

    # --- CORE MOVIE DATA ---
    title = models.CharField(max_length=255)
    tmdb_id = models.IntegerField(null=True, blank=True)
    poster_url = models.URLField(max_length=500, null=True, blank=True)
    year = models.CharField(max_length=10, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    imdb_rating = models.FloatField(default=0.0)

    # --- TRACKING ---
    movie_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='movie')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='watchlist')
    date_added = models.DateTimeField(auto_now_add=True)

    # Collaborative notes - perfect for keeping it simple for now
    shared_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title


class MovieReview(models.Model):
    # Link to your existing MovieTracker model
    movie = models.ForeignKey(MovieTracker, on_delete=models.CASCADE, related_name='movie_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.IntegerField(default=0)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s review for {self.movie.title}"


class Playlist(models.Model):
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='playlists')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='playlist_covers/', null=True, blank=True)
    cover_url = models.URLField(blank=True)
    is_external = models.BooleanField(default=False)
    platform = models.CharField(max_length=50, blank=True)
    external_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class SongMemory(models.Model):
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='songs')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    memory_description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    platform = models.CharField(max_length=50, blank=True) # spotify or youtube
    track_id = models.CharField(max_length=100, blank=True)
    cover_url = models.URLField(blank=True)
    playlists = models.ManyToManyField(Playlist, related_name='songs', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.title} - {self.artist}"


class Memory(models.Model):
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='memories')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, default='New Memory')
    description = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

class MemoryPhoto(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='memories/')
    caption = models.CharField(max_length=300, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['added_at']

    def __str__(self):
        return f"Photo for {self.memory.title}"

class DashboardSnap(models.Model):
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='dashboard_snaps')
    image = models.ImageField(upload_to='dashboard_snaps/')
    caption = models.CharField(max_length=300, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_at']

    def __str__(self):
        return f"Snap for {self.couple}"

class YourMoodEntry(models.Model):
    MOOD_KEYS = [
        ('ecstatic', 'Ecstatic 🤩'),
        ('happy', 'Happy 😊'),
        ('calm', 'Calm 😌'),
        ('sad', 'Low 😔'),
        ('tired', 'Tired 😴'),
        ('anger', 'Anger 😡'),
        ('naughty', 'Naughty 😈'),
        ('romantic', 'Romantic ❤️'),
        ('playful', 'Playful 🤪'),
    ]

    couple = models.ForeignKey('Couple', on_delete=models.CASCADE, related_name='mood_entries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood_type = models.CharField(max_length=20, choices=MOOD_KEYS, default='calm')
    energy_percent = models.IntegerField(default=70)
    naughty_percent = models.IntegerField(default=0) # Added back for you
    stress_percent = models.IntegerField(default=20)
    sleep_hours = models.FloatField(default=0.0)
    bedtime = models.CharField(max_length=20, default="11:00 PM")
    wake_time = models.CharField(max_length=20, default="06:30 AM")
    journal_text = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']

    @property
    def mood_emoji(self):
        emoji_map = {
            'ecstatic': '🤩',
            'happy': '😊',
            'calm': '😌',
            'sad': '😔',
            'tired': '😴',
            'anger': '😡',
            'naughty': '😈',
            'romantic': '❤️',
            'playful': '🤪',
        }
        return emoji_map.get(self.mood_type, '😶')

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class BucketList(models.Model):
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]

    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='bucket_items')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    target_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class StatusUpdate(models.Model):
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='statuses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status_text = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"{self.user.name}: {self.status_text}"

class Milestone(models.Model):
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='milestones')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    icon = models.CharField(max_length=10, default='💞')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date'] # Past to Future ordering

    def __str__(self):
        return f"{self.date} - {self.title}"

class PeriodCycle(models.Model):
    couple = models.ForeignKey(Couple, on_delete=models.CASCADE, related_name='period_cycles')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    cycle_length = models.IntegerField(default=28)
    period_length = models.IntegerField(default=5)
    
    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"Cycle for {self.couple} starting {self.start_date}"

class SymptomLog(models.Model):
    cycle = models.ForeignKey(PeriodCycle, on_delete=models.CASCADE, related_name='symptoms')
    date = models.DateField()
    flow = models.CharField(max_length=20, blank=True) # Light, Medium, Heavy
    mood = models.CharField(max_length=50, blank=True)
    symptoms = models.TextField(blank=True) # Comma separated or JSON

    class Meta:
        ordering = ['date']
        unique_together = ('cycle', 'date')

    def __str__(self):
        return f"Symptoms on {self.date}"