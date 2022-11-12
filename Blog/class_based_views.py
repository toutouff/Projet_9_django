from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TicketForm,ReviewForm
from .models import Ticket, Review , UserFollows
from django.views import View


class Follow(View):
    def get(self, request,user_id = None):
        user = request.user
        if user_id:
            followed_user = get_object_or_404(User,id= user_id)
            user_follows = get_object_or_404(UserFollows,user=user,followed_user=followed_user)
            user_follows.delete()
            return redirect('follow')
        else:
            following_user = UserFollows.objects.filter(user=user)
            followed_user = UserFollows.objects.filter(followed_user = user)
        return render(request, 'Blog/follow.html', context={'following_users':following_user,'followed_users': followed_user})

    def post(self,request):
        user = request.user
        searched_data = request.POST.get('search_bar')
        print(searched_data)
        searched_user = User.objects.filter(username = searched_data).first()
        print(searched_user)
        if searched_user is not None and searched_user is not user:
            user_follows = UserFollows.objects.filter(user = user , followed_user = searched_user)
            print(len(user_follows))
            if not len(user_follows):
                user_follows = UserFollows(user = user ,followed_user = searched_user)
                user_follows.save()
                print(user_follows)
            else:
                message='deja abonnée '
                print(message)
        else:
            message = "l'utilisateur n'existe pas "
            print(message)
        return redirect('follow')



class Content_Create(View):
    ticket_form = None
    review_form = None
    def get(self,request,ticket_id = None):
        if self.ticket_form and not self.review_form:
            # creation of a ticket
            form = self.ticket_form
            return render(request,'Blog/ticket_creation.html',{'form':form})

        elif not self.ticket_form and self.review_form and ticket_id:
                #creation d'une review a partir d'un ticket soit /reply
            ticket = get_object_or_404(Ticket,id=ticket_id)    # carful of ticket_id as argument
            form = self.review_form
            return render(request,'Blog/review_creation.html',{'ticket':ticket,'review_form':form})

        elif self.ticket_form and self.review_form:
            return render(request,'Blog/review_creation.html',{'ticket_form':self.ticket_form,'review_form':self.review_form})

    def post(self,request,ticket_id = None):
        if self.ticket_form and not self.review_form:
            form = self.ticket_form(request.POST,request.FILES)
            if form.is_valid():
                ticket = form.save(commit= False)
                ticket.user = request.user
                ticket.save()
                return redirect('flux')
            else:
                message = 'Veillez a respecter les champs obligatoires'
                return render(request,'Blog/ticket_creation',{'form':form,
                                                              'message':message})

        elif not self.ticket_form and self.review_form and ticket_id:
            ticket= get_object_or_404(Ticket,id=ticket_id)
            form = self.review_form(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user,review.ticket = request.user,ticket
                review.save()
                return redirect('flux')
            else:
                message = 'Veillez a respecter les champs obligatoires'
                return render(request, 'Blog/review_creation', {'form': form,
                                                                'message': message})
        elif self.ticket_form and self.review_form:
            t_form = self.ticket_form(request.POST,request.FILES)
            if t_form.is_valid():
                ticket = t_form.save(commit=False)
                ticket.user = request.user
                r_form = self.review_form(request.POST)
                if r_form.is_valid():
                    review = r_form.save(commit=False)
                    review.ticket,review.user = ticket,ticket.user
                    ticket.save()
                    review.save()
                    return redirect('flux')


class Content_Edit(View):
    def get(self,request,ticket_id):
        ticket_form = None
        review_form = None
        review = None
        ticket = get_object_or_404(Ticket,id=ticket_id)
        if len(Review.objects.filter(ticket=ticket)):
            review = Review.objects.filter(ticket=ticket).first()
            if review.user == request.user:
                review_form = ReviewForm(instance=review)
        if ticket.user == request.user:
            ticket_form = TicketForm(instance=ticket)

        """
        - ticket_form = F_obj or None
        - review_form = F_obj or None
        - ticket = obj
        - review = obj or none
        
        """

        if ticket_form and review_form:  # ticket_form = 1 r_form = 1 review = 1
            context = {'review_form':review_form,'ticket_form':ticket_form}
        elif ticket_form and review:  # t_form = 1 r_form = 0 et review = 1
            context = {'ticket_form':ticket_form,'review':review}
        elif ticket and review_form:# t_form = 0 review_form = 1 review =1
            context = {'ticket':ticket,'review_form':review_form}
        elif ticket_form : # t_form = 0 r_form = 0 review = 0
            context = {'ticket_form':ticket_form}
        else :
            context= {'message':'une errreure est survenue'}
            print(context)
        render(request,'Blog/edit.html',context = context)


    def post(self,request):
        pass
