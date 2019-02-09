"""
BSD 3-Clause License

Copyright (c) 2016-2019 Russ 'trdwll' Treadwell. All rights reserved.
"""
from django.shortcuts import render, render_to_response, get_object_or_404
from . models import Post

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def blog_home(request):
	all_posts = Post.objects.all().order_by('-id')

	TOTAL_ON_PAGE = 5

	if len(all_posts) >= TOTAL_ON_PAGE:
		page = request.GET.get('page', 1)

		paginator = Paginator(all_posts, TOTAL_ON_PAGE)
		try:
			all_posts = paginator.page(page)
		except PageNotAnInteger:
			all_posts = paginator.page(1)
		except EmptyPage:
			all_posts = paginator.page(paginator.num_pages)

		return render(request, 'blog.html', {'all_posts': all_posts, 'pagination': paginator})

	return render(request, 'blog.html', {'all_posts': all_posts})


def view_post(request, year, month, slug):
	post = get_object_or_404(Post, created__year=year, created__month=month, slug=slug)

	return render(request, 'view_post.html', {'post': post})
	# return render_to_response('view_post.html', {
	# 	'post': get_object_or_404(Post, created__year=year, created__month=month, slug=slug)
	# })