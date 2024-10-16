from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import *
from .forms import *
from django.views import View
from django.views.decorators.csrf import*
import re
from django.views.decorators.http import require_POST
# Home Page
def home(request):
    return render(request, 'home.html')

# Player Profile List
def player_list(request):
    players = PlayerProfile.objects.all()
    return render(request, 'player_list.html', {'players': players})

# Player Profile Detail
def player_detail(request, pk):
    player = get_object_or_404(PlayerProfile, pk=pk)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's an AJAX request
        data = {
            'photo_url': player.photo.url,
            'name': player.name,
            'position': player.position,
            'bio': player.bio,
            'dream': player.dream
        }
        return JsonResponse(data)
    else:
        # Fallback if the request isn't AJAX
        # Normally you'd return a template here for a non-AJAX request
        return JsonResponse({'error': 'Invalid request'}, status=400)

# Match List
def match_list(request):
    matches = Match.objects.all()
    return render(request, 'match_list.html', {'matches': matches})

# Match Detail
def match_detail(request, pk):
    match = get_object_or_404(Match, pk=pk)
    return render(request, 'match_detail.html', {'match': match})

# Event List
def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {
        'events': events,
        'photos': [event.photo.url for event in events]  # Assuming the photo field is an ImageField
    })

# Event Detail
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {
        'event': event,
        'photo': event.photo.url  # Assuming the photo field is an ImageField
    })


def coaches_list(request):
    coaches = CoachProfile.objects.all()
    return render(request, 'coaches_list.html', {'coaches': coaches})


# Coach Details View
def coach_detail(request, pk):
    coach = get_object_or_404(CoachProfile, pk=pk)
    return render(request, 'coach_detail.html', {'coach': coach})


# Donation Page
def donation(request):
    return render(request, 'donation.html')

# Volunteer Page
def volunteer(request):
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('volunteer_success') 
    else:
        form = VolunteerForm()

    return render(request, 'volunteer.html', {'form': form})


def volunteer_success(request):
    return render(request,'volunteer_success.html')
# Contact Page
def contact(request):
    return render(request, 'contact.html')



class SponsorView(View):
    def get(self, request):
        players = PlayerProfile.objects.all()
        return render(request, 'sponsor.html', {'players': players})

    def post(self, request):
        sponsor_name = request.POST['sponsor_name']
        email = request.POST['email']
        player_id = request.POST['player']
        amount = request.POST['amount']
        message = request.POST['message']

        # Save the sponsor information
        Sponsor.objects.create(
            sponsor_name=sponsor_name,
            player_id=player_id,
            amount=amount,
            message=message
        )

        return redirect('home.html')  # Redirect to a success page or back to the form


def programs(request):
    return render(request, 'programs.html')


def success_stories(request):
    stories = SuccessStory.objects.all()
    return render(request, 'success_stories.html', {'stories': stories})




# View for rendering the gallery page
# A helper function to validate Gmail addresses
def validate_gmail(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email)

@csrf_exempt
def gallery_list(request):
    items = GalleryItem.objects.all()
    return render(request, 'gallery.html', {'items': items})

@csrf_exempt
def like_item(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(GalleryItem, pk=item_id)
        email = request.POST.get('email')

        if not validate_gmail(email):
            return JsonResponse({'error': 'Invalid Gmail address.'}, status=400)

        item.likes += 1
        item.save()
        return JsonResponse({'likes': item.likes})

@csrf_exempt
def add_comment(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(GalleryItem, pk=item_id)
        email = request.POST.get('email')
        comment_text = request.POST.get('comment')

        if not validate_gmail(email):
            return JsonResponse({'error': 'Invalid Gmail address.'}, status=400)

        comment = Comment(item=item, gmail=email, text=comment_text)
        comment.save()
        return JsonResponse({
            'comment': {
                'gmail': comment.gmail,
                'text': comment.text,
            }
        })



def add_reaction(request):
    data = json.loads(request.body)
    gallery_id = data.get('gallery_id')
    reaction_type = data.get('reaction_type')
    gmail = data.get('gmail')

    gallery = get_object_or_404(Gallery, id=gallery_id)

    # Check if a reaction from this Gmail already exists
    reaction, created = Reaction.objects.update_or_create(
        gmail=gmail, 
        gallery=gallery, 
        defaults={'reaction_type': reaction_type}
    )

    return JsonResponse({'message': 'Reaction added/updated', 'reaction': reaction_type})