from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from . import forms, models
from django.db import IntegrityError
from django.contrib import messages
from authentication.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


@login_required
def home(request):
    followed_users = models.UserFollows.objects.filter(user=request.user)
    #pourquoi je n'arrive pas à utiliser le résultat du queryset ci-dessus?
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()

    return render(request, 'blog/home.html',context={'tickets': tickets,
                                                     'reviews': reviews})
@login_required
def posts(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    reviews = models.Review.objects.filter(user=request.user)
    return render(request, 'blog/posts.html',context={'tickets': tickets,
                                                     'reviews': reviews})

@login_required
def ticket_upload(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            # set the uploader to the user before saving the model
            ticket.user = request.user
            # now we can save
            ticket.save()
            return redirect('home')
    return render(request, 'blog/ticket.html',context={'form': form})

@login_required
def ticket_review_upload(request):
    form = forms.TicketReviewForm()
    if request.method == 'POST':
        form = forms.TicketReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            # set the uploader to the user before saving the model
            review.user = request.user
            # now we can save
            review.save()
            return redirect('home')
    return render(request, 'blog/ticket_review.html', context={'form': form})

@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'blog/view_ticket.html', {'ticket': ticket})

@login_required
def view_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    return render(request, 'blog/view_review.html', {'review': review})

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, request.FILES,instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST, request.FILES)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,}
    return render(request, 'blog/edit_ticket.html', context=context)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.TicketReviewForm(instance=review)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.TicketReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_review' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST, request.FILES)
            if delete_form.is_valid():
                review.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,}
    return render(request, 'blog/edit_review.html', context=context)


@login_required
def follow_users(request):
    form = forms.UserFollowsForm()
    context = {'form': form}

    # display subscriptions
    followed_users = models.UserFollows.objects.filter(user=request.user)
    context['followed_users'] = followed_users

    # display 'subscribers'
    followers = models.UserFollows.objects.filter(followed_user=request.user)
    context['followers'] = followers

    if request.method == 'POST':
        # get the searched user
        try:
            new_followed_user = User.objects.get(username=request.POST['followed_user'])
        except ObjectDoesNotExist:
            error_message = f"<strong>{request.POST['followed_user'].lower()}" \
                            f"</strong> n'existe pas dans la base de donnée."
            messages.add_message(request, messages.ERROR, message=error_message)
            return render(request,
                          "blog/follow_users_form.html",
                          context=context)
        else:
            # case where the user is looking for himself
            if new_followed_user.username == request.user.username:
                error_message = " --- Vous ne pouvez pas vous suivre vous même! --- "
                messages.add_message(request, messages.ERROR, message=error_message)
                return render(request, "blog/follow_users_form.html",
                              context=context)

            # new followed_user registration
            new_subscription = models.UserFollows(user=request.user, followed_user=new_followed_user)
            try:
                new_subscription.save()
            except IntegrityError:
                error_message = f"Vous suivez déjà <strong>{new_followed_user}</strong>."
                messages.add_message(request, messages.ERROR, message=error_message)
                return render(request,
                              "blog/follow_users_form.html",
                              context=context)
            else:
                success_message = f"Vous suivez désormais <strong>{new_subscription.followed_user}</strong>."
                messages.add_message(request, messages.SUCCESS, message=success_message)
                return render(request,
                              "blog/follow_users_form.html",
                              context=context)
    return render(request,"blog/follow_users_form.html", context=context)