from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import TicketForm, ReviewForm
from .models import Ticket, Review, UserFollows
from django.views import View


class Follow(View):
    def get(self, request, user_id=None):
        user = request.user
        if user_id:
            followed_user = get_object_or_404(User, id=user_id)
            user_follows = get_object_or_404(UserFollows, user=user,
                                             followed_user=followed_user)
            user_follows.delete()
            return redirect('follow')
        else:
            following_user = UserFollows.objects.filter(user=user)
            followed_user = UserFollows.objects.filter(followed_user=user)
        return render(request, 'Blog/follow.html',
                      context={'following_users': following_user,
                               'followed_users': followed_user})

    def post(self, request):
        user = request.user
        searched_data = request.POST.get('search_bar')
        searched_user = User.objects.filter(username=searched_data).first()
        if searched_user is not None and searched_user is not user:
            user_follows = UserFollows.objects.filter(user=user,
                                                      followed_user=searched_user)
            if not len(user_follows):
                user_follows = UserFollows(user=user,
                                           followed_user=searched_user)
                user_follows.save()
            else:
                message = 'deja abonnée '
        else:
            message = "l'utilisateur n'existe pas "
        return redirect('follow')


class Content_Create(View):
    ticket_form = None
    review_form = None

    def get(self, request, ticket_id=None):
        if self.ticket_form and not self.review_form:
            # creation of a ticket
            form = self.ticket_form
            return render(request, 'Blog/ticket_creation.html', {'form': form})

        elif not self.ticket_form and self.review_form and ticket_id:
            # creation d'une review a partir d'un ticket soit /reply
            ticket = get_object_or_404(Ticket,
                                       id=ticket_id)  # carful of ticket_id as argument
            form = self.review_form
            return render(request, 'Blog/review_creation.html',
                          {'ticket': ticket, 'review_form': form})

        elif self.ticket_form and self.review_form:
            return render(request, 'Blog/review_creation.html',
                          {'ticket_form': self.ticket_form,
                           'review_form': self.review_form})

    def post(self, request, ticket_id=None):
        if self.ticket_form and not self.review_form:
            # creation d'un ticket method post
            form = self.ticket_form(request.POST, request.FILES)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.user = request.user
                ticket.save()
                return redirect('flux')
            else:
                message = 'Veillez a respecter les champs obligatoires'
                return render(request, 'Blog/ticket_creation', {'form': form,
                                                                'message': message})

        elif not self.ticket_form and self.review_form and ticket_id:
            user = request.user
            # creation d'une review a partir d'un ticket
            ticket = get_object_or_404(Ticket, id=ticket_id)
            form = self.review_form(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user, review.ticket = user, ticket
                review.save()
                ticket.is_closed = True
                ticket.save(update_fields=['is_closed'])
                #print(f'review_user = {review.user.username},user = {user.username}')
                return redirect('flux')
            else:
                message = 'Veillez a respecter les champs obligatoires'
                return render(request, 'Blog/review_creation', {'form': form,
                                                                'message': message})
        elif self.ticket_form and self.review_form:
            # creation dune review et dun ticket
            t_form = self.ticket_form(request.POST, request.FILES)
            if t_form.is_valid():
                ticket = t_form.save(commit=False)
                ticket.user = request.user
                #print(request.FILES)
                r_form = self.review_form(request.POST)
                if r_form.is_valid():
                    review = r_form.save(commit=False)
                    review.ticket, review.user ,ticket.is_closed= ticket, ticket.user,True
                    ticket.save()
                    review.save()
                    return redirect('flux')


class Content_Edit(View):
    user = None
    ticket_form = None
    review_form = None
    review = None
    ticket = None

    def get(self, request, ticket_id):
        self.user = request.user
        self.ticket = get_object_or_404(Ticket, id=ticket_id)
        if len(Review.objects.filter(ticket=self.ticket)):
            self.review = Review.objects.filter(ticket=self.ticket).first()
            if self.review.user.username == self.user.username:
                self.review_form = ReviewForm(instance=self.review)
        if self.ticket.user.username == self.user.username:
            self.ticket_form = TicketForm(instance=self.ticket)
        """
        - ticket_form = F_obj or None
        - review_form = F_obj or 
        - ticket = obj
        - review = obj or none
        
        """
        #print(f'ticket = {ticket} review = {review} ticket_form = {ticket_form} review_form = {review_form}')

        if self.ticket_form and self.review_form:  # ticket_form = 1 r_form = 1 review = 1
            context = {'review_form': self.review_form, 'ticket_form': self.ticket_form}
            return render(request, 'Blog/edit.html', context=context)
        elif self.ticket_form and self.review:  # t_form = 1 r_form = 0 et review = 1
            context = {'ticket_form': self.ticket_form, 'review': self.review}
            return render(request, 'Blog/edit.html', context=context)
        elif self.ticket and self.review_form:  # t_form = 0 review_form = 1 review =1
            context = {'ticket': self.ticket, 'review_form': self.review_form}
            return render(request, 'Blog/edit.html', context=context)
        elif self.ticket_form:  # t_form = 0 r_form = 0 review = 0
            context = {'ticket_form': self.ticket_form}
            return render(request, 'Blog/edit.html', context=context)
        else:
            context = {'message': 'une errreure est survenue'}
        #print(context)
        return render(request, 'Blog/edit.html', context=context)


    def post(self, request,ticket_id):
        self.user = request.user
        self.ticket = get_object_or_404(Ticket, id=ticket_id)
        if len(Review.objects.filter(ticket=self.ticket)):
            self.review = Review.objects.filter(ticket=self.ticket).first()
            if self.review.user.username == self.user.username:
                self.review_form = ReviewForm(instance=self.review)
        if self.ticket.user.username == self.user.username:
            self.ticket_form = TicketForm(instance=self.ticket)
        

        print(self.review_form,self.ticket_form,self.review ,self.ticket)
        if self.ticket_form and self.review_form:
            print('ticket and review edit')
            ticket_form = TicketForm(request.POST,instance = self.ticket)
            review_form = ReviewForm(request.POST,instance = self.review)
            if ticket_form.is_valid():
                if review_form.is_valid():
                    ticket = ticket_form.save(commit=False)
                    review = review_form.save(commit=False)
                    ticket.save()
                    review.save()


        elif self.ticket_form and self.review:
            ticket_form = TicketForm(request.POST,instance= self.ticket)
            if ticket_form.is_valid():
                ticket_form.save()
        elif self.review_form and not self.ticket_form:
            review_form = ReviewForm(request.POST,instance=self.review)
            if review_form.is_valid():
                review_form.save()
        elif self.ticket_form:
            ticket_form = TicketForm(request.POST,instance = self.ticket)
            if ticket_form.is_valid():
                ticket_form.save()

        return redirect('post')
     
class Content_page(View):
    feed = False
    template_url = "Blog/flux.html"

    def get_userlist(self, request):
        userlist = []
        user = request.user
        userlist.append(user)
        if self.feed:
            followeduserlist = UserFollows.objects.filter(user=user)
            for i in range(len(followeduserlist)):
                followeduser = followeduserlist[i]
                userlist.append(followeduser.followed_user)
        return userlist

    def get_content(self, userlist):
        content = []
        for user in userlist:
            ticketlist = Ticket.objects.filter(user=user)
            reviewlist = Review.objects.filter(user=user)
            content.extend([ticketlist[i] for i in range(len(ticketlist))])
            content.extend([reviewlist[i] for i in range(len(reviewlist))])
        content.sort(key=lambda x: x.time_created,reverse=True)
        return content

    def get(self, request):
        request = request
        userlist = self.get_userlist(request)
        contentlist = self.get_content(userlist)
        return render(request, self.template_url,
                      context={'contentlist': contentlist})

    def post(self, request):
        pass
