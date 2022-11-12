from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review, UserFollows


@login_required
def ticket_create(request):
    if request.method == 'POST':
        ticket = Ticket(user=request.user)
        form = TicketForm(request.POST,request.FILES, instance=ticket)
        if form.is_valid():
            ticket.save()
            return redirect('post')
    else:
        form = TicketForm()
    return render(request, 'Blog/ticket_creation.html', {'form': form})


@login_required
def post(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    posts = []
    for j in range(len(tickets)):
        ticket = tickets[j]
        reviews = Review.objects.filter(ticket=ticket)
        if len(reviews) == 1:
            review = reviews[0]
            f_review = {'ticket': ticket, 'closed': True, 'review': review}
        else:
            f_review = {'ticket': ticket, 'closed': False}
        posts.append(f_review)
    return render(request, 'Blog/post.html', context={'posts': posts})


@login_required
def review_create(request, ticket_id=None):
    if request.method == 'POST':
        if ticket_id is not None:
            ticket = Ticket.objects.get(id=ticket_id)
            review = Review(ticket=ticket, user=request.user)
            review_form = ReviewForm(request.POST, instance=review)
            if review_form.is_valid():
                review_form.save()
                return redirect('post')
        else:
            ticket = Ticket(user=request.user)
            ticket_form = TicketForm(request.POST, instance=ticket)
            if ticket_form.is_valid():
                review = Review(ticket=ticket, user=request.user)
                review_form = ReviewForm(request.POST, instance=review)
                if review_form.is_valid():
                    ticket_form.save()
                    review_form.save()
                    return redirect('post')
    else:
        if ticket_id is not None:
            ticket = Ticket.objects.get(id=ticket_id)
            review_form = ReviewForm()
            return render(request, 'Blog/review_creation.html', {
                'ticket': ticket,
                'review_form': review_form
            })
        else:
            ticket_form = TicketForm()
            review_form = ReviewForm()
            return render(request, 'Blog/review_creation.html', {
                'review_form': review_form,
                'ticket_form': ticket_form
            })


@login_required
def follow_page(request):
    # TODO: make unfollow button + no unfollow when try to dubplicate userFollows object
    if request.method == 'POST':
        user = request.user
        data = request.POST.get('search_bar')
        searched_user = User.objects.filter(username=data).first()
        if searched_user is not None:
            if searched_user != user:
                user_follows = UserFollows.objects.filter(
                    user=user, followed_user=searched_user).first()
                if user_follows is None:
                    user_follows = UserFollows(
                        user=user, followed_user=searched_user)
                    user_follows.save()
                else:
                    message = 'Vous suivez déjà cet utilisateur.'
        user = request.user
        following_user = UserFollows.objects.filter(user=user)
        followed_user = UserFollows.objects.filter(followed_user=user)
        return render(request, 'Blog/follow.html', context={'following_users': following_user, 'followed_users': followed_user})
    else:
        user = request.user
        following_user = UserFollows.objects.filter(user=user)
        followed_user = UserFollows.objects.filter(followed_user=user)
        return render(request, 'Blog/follow.html',
                      context={'following_users': following_user,
                               'followed_users': followed_user})


@login_required
def unfollow(request, user_id):
    user = request.user
    followed_user = User.objects.get(id=user_id)
    user_follows = UserFollows.objects.filter(
        user=user, followed_user=followed_user).first()
    user_follows.delete()
    return redirect('follow')


@login_required
def flux(request):
    # TODO: ulist = user + f_user
    # TODO: getreviews(ulist)
    # TODO: gettickets(ulist) - tickets from reviews
    # todo: format data for template (ticket, review, is_closed) & sort by date
    # todo: edit template:
    #
    user = request.user
    followed_users = UserFollows.objects.filter(user=user)

    posts = []
    user_tickets = Ticket.objects.filter(user=user)
    for k in range(len(user_tickets)):
        user_ticket = user_tickets[k]
        user_reviews = Review.objects.filter(
            ticket=user_ticket)    # get user reviews
        if len(user_reviews) == 1:
            user_review = user_reviews[0]
            f_review = {'ticket': user_ticket,
                        'closed': True, 'review': user_review}
        else:
            f_review = {'ticket': user_ticket, 'closed': False}
        posts.append(f_review)

    for i in range(len(followed_users)):
        f_user = followed_users[i].followed_user
        tickets = Ticket.objects.filter(user=f_user)
        for j in range(len(tickets)):
            ticket = tickets[j]
            reviews = Review.objects.filter(ticket=ticket)
            if len(reviews) == 1:
                review = reviews[0]
                f_review = {'ticket': ticket, 'closed': True, 'review': review}
            else:
                f_review = {'ticket': ticket, 'closed': False}
            posts.append(f_review)
    posts.sort(key=lambda x: x['ticket'].time_created, reverse=False)
    return render(request, 'Blog/flux.html', context={'posts': posts})


@login_required
def edit(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    review = Review.objects.filter(ticket=ticket).first()
    user = request.user
    print(f'user: {user},try to edit ticket: {ticket} and review: {review}')
    message = ''
    if review is not None:
        if user == review.user:     # user is the owner of the review
            print(f'user: {user}, is the owner of the review: {review}')
            if user == ticket.user:     # user is the owner of the ticket
                print(f'user: {user}, is the owner of the ticket: {ticket}')
                if request.method == 'POST':
                    ticket_form = TicketForm(request.POST, instance=ticket)
                    review_form = ReviewForm(request.POST, instance=review)
                    if ticket_form.is_valid() and review_form.is_valid():
                        ticket_form.save()
                        review_form.save()
                        return redirect('post')
                    else:
                        message = 'veillez a bien remplir tous les champs'
                else:

                    review_form = ReviewForm(instance=review)
                    ticket_form = TicketForm(instance=ticket)
                    return render(request, 'Blog/edit.html',
                                  {"ticket_form": ticket_form,
                                   "review_form": review_form,
                                   'closed': True,
                                   "message": message})
            # TODO: user can only edit his review but the ticket is shown

        else:  # user is not the owner of the review
            if user == ticket.user:  # if user is the owner of the ticket
                print(f'user: {user}, is the owner of the ticket: {ticket}'
                      f'and can edit it')
                if request.method == 'POST':
                    form = TicketForm(request.POST, instance=ticket)
                    if form.is_valid():
                        form.save()
                        return redirect('post')
                else:
                    form = TicketForm(instance=ticket)
                    return render(request, 'Blog/edit.html',
                                  {'ticket_form': form, 'closed': False,
                                   'message': message})

    else:
        if user == ticket.user:     # if user is the owner of the ticket
            print(f'user: {user}, is the owner of the ticket: {ticket}'
                  f'and can edit it')
            if request.method == 'POST':
                form = TicketForm(request.POST, instance=ticket)
                if form.is_valid():
                    form.save()
                    return redirect('post')
            else:
                form = TicketForm(instance=ticket)
                return render(request, 'Blog/edit.html', {'ticket_form': form, 'closed': False, 'message': message})
        else:   # if user is not the owner of the ticket
            print(f'user: {user}, is not the owner of the ticket: {ticket}')
            return redirect('post')
        #   nesexecute pas


@login_required
def delete(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    review = Review.objects.filter(ticket=ticket).first()
    if review is not None:
        review.delete()
    ticket.delete()
    return redirect('post')
