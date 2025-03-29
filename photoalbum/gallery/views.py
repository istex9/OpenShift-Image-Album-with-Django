from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo
from django.contrib.auth.decorators import login_required
from .forms import PhotoForm

def home(request):
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'date':
        photos = Photo.objects.order_by('-uploaded_at')
    else:
        photos = Photo.objects.order_by('name')
    return render(request, 'gallery/home.html', {'photos': photos})

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.owner = request.user
            photo.save()
            return redirect('home')
    else:
        form = PhotoForm()
    return render(request, 'gallery/upload.html', {'form': form})

@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id, owner=request.user)
    photo.delete()
    return redirect('home')

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'gallery/detail.html', {'photo': photo})
