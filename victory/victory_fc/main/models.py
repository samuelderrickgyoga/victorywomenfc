from django.db import models



class PlayerProfile(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='player_photos/')
    position = models.CharField(max_length=50)
    bio = models.TextField()
    dream = models.TextField()

    def __str__(self):
        return self.name

class CoachProfile(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='coach_photos/')
    role = models.CharField(max_length=50)
    bio = models.TextField()

    def __str__(self):
        return self.name

class Match(models.Model):
    home_team = models.CharField(max_length=100, blank=True, null=True)
    home_team_logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)
    home_score = models.PositiveIntegerField(default=0)

    away_team = models.CharField(max_length=100)
    away_team_logo = models.ImageField(upload_to='team_logos/',  blank=True, null=True)
    away_score = models.PositiveIntegerField(default=0)

    league_logo = models.ImageField(upload_to='league_logos/', blank=True, null=True)  # Optional league logo

    date = models.DateTimeField()
    time = models.TimeField()  # Separate time field if needed

    location = models.CharField(max_length=100)
    practice_time = models.TimeField()
    match_time = models.TimeField()

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date.strftime('%Y-%m-%d')}"

class Event(models.Model):
    EVENT_TYPES = [
        ('Match', 'Match'),
        ('Workshop', 'Workshop'),
        ('Community Event', 'Community Event'),
    ]
    
    title = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='event_photos/', default="bg.jpg")
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)

    def __str__(self):
        return self.title

class Donation(models.Model):
    donor_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Donation by {self.donor_name} - ${self.amount}"

class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=50)
    availability = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Sponsor(models.Model):
    sponsor_name = models.CharField(max_length=100)
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sponsor: {self.sponsor_name} for {self.player.name}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Contact from {self.name}"

class SuccessStory(models.Model):
    player_name = models.CharField(max_length=100)
    story = models.TextField()
    image = models.ImageField(upload_to='success_stories/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.player_name

#gallerry

class GalleryItem(models.Model):
    POST_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('text', 'Text'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    content_image = models.ImageField(upload_to='gallery_images/', blank=True, null=True)
    content_video = models.FileField(upload_to='gallery_videos/', blank=True, null=True)
    content_text = models.TextField(blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    gmail = models.EmailField()  # Store the Gmail address
    gallery = models.ForeignKey('GalleryItem', on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gmail} liked {self.gallery.title}"


class Comment(models.Model):
    gmail = models.EmailField()  # Store the Gmail address
    gallery = models.ForeignKey('GalleryItem', on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gmail} commented on {self.gallery.title}"


class Reaction(models.Model):
    REACTION_TYPES = [
        ('like', 'Like'),
        ('love', 'Love'),
        ('wow', 'Wow'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
    ]
    gmail = models.EmailField()  # Store the Gmail address
    gallery = models.ForeignKey('GalleryItem', on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_TYPES)
    reacted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gmail} reacted {self.reaction_type} to {self.gallery.title}"