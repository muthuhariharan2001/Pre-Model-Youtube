# from django.shortcuts import render, get_object_or_404
# from .models import Video
# from .forms import VideoSearchForm

# def video_list(request):
#     form = VideoSearchForm(request.GET)
#     videos = Video.objects.all()
#     if form.is_valid():
#         query = form.cleaned_data['query']
#         videos = videos.filter(title__icontains=query)
#     return render(request, 'index.html', {'form': form, 'videos': videos})

# def video_detail(request, video_id):
#     video = get_object_or_404(Video, id=video_id)
#     return render(request, 'detail.html', {'video': video})


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Video, Comment
from .forms import VideoSearchForm, CommentForm

def video_list(request):
    form = VideoSearchForm(request.GET)
    videos = Video.objects.all()
    if form.is_valid():
        query = form.cleaned_data['query']
        videos = videos.filter(title__icontains=query)
    return render(request, 'index.html', {'form': form, 'videos': videos})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    is_liked = video.likes.filter(id=request.user.id).exists()
    comments = video.comments.all()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.video = video
            new_comment.user = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('video_detail', args=[video.id]))
    else:
        comment_form = CommentForm()

    return render(request, 'detail.html', {
        'video': video,
        'is_liked': is_liked,
        'total_likes': video.total_likes(),
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    })

def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if video.likes.filter(id=request.user.id).exists():
        video.likes.remove(request.user)
    else:
        video.likes.add(request.user)
    return HttpResponseRedirect(reverse('video_detail', args=[video.id]))
