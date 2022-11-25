## Project description 
>solution web permetant a une comunauté d'utilisateur de demander ou de poster des critique de livre

## how to install and run the project 
the project need django and python 
### how to install 
- on the terminal type the comande to clone the github to the working directory 
```zsh
git clone https://github.com/toutouff/Projet_9_django
```
- create the pip virtual environement 
```zsh
python3 venv Name_of_the_Venv 
```
- then install all the required packages 
```zsh
pip install -r requirement.txt
```
- finaly source the Virtual environement
on OSX/Unix: 
```zsh 
source Name_of_the_Venv/bin/activate 
```
on Windows
```powershell
.\Name_of_the_Venv\Scripts\activate
```
### run the project

```zsh
python3 LITReview/manage.py runserver 
```
>if you want to run it on a specific IP (like the the ip of your computer rather than the localhost(127.0.0.1:8000)) you can by specify it 

## basic structure and explanation of what does what 
the project is constitued of 2 app 
- the blog app 
- the Auth app 

- #### the blog app 
this app serve all the site views and logic exepts the login and signup view and logic
##### models.py 
is based on this database scheme 
![[Pasted image 20221124172846.png]]
***models.py***
```python
class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(blank=True ,null=True,upload_to='Blog')
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_closed = models.BooleanField(default= False) 

```
the ```is_closeed``` was added so Database can register when a ticket as been responded 

##### Views.py
all the view are Class Based and inherit of the View class from django.views 
there are 4 fundamentals view 
the Follow class 
the get method generate the follow page which show all the followers username and the username of user we follow as well as an username search bar to follow user  

the post method get a username from the 'searchbar' key inside request.POST data and then 
get the user from the database coresponding to the username then if the searched user exist it's gonna create a UserFollows object 

the Content_create class
as two global parameters wich store either the Ticket form or the Rewies form wich are set when calling the view
then the get method serve the selected form 
example 
```python
import forms
Content_create.as_view(Ticket_form = forms.Ticket_form)
# gona return the html page to create a ticket only 

Content_create.as_view(Ticket_form = forms.Ticket_form,Review_form = forms.Review_form)
# gonna return the html page to create a ticket and and review based on the ticket

Content_create.as_view(Review_form = forms.Review_form)
# when only the review_form is set a ticket id is send as argument from the url 
# then its gonna return the html page to create the review based on the ticket
```
the post method gonna check what it recieve from the request.POST data and will fill and save the different object in the data base 


the Content_edit class works quite as same as the Content_create class but 
add a security overlay by insuring that user are allowed to edit what they're willing to update 
example :
>you're User A and you respond to a ticket from User B
>you want to edit your review ,let see how the server gonna take ad respond to your request 
>the server recieve a /blog/ticket/*ticket_id*/edit? request 
>it's gonna get the ticket with the ticket_id value 
>then check if a review exist and if yes gonna temporaly store it 
>after the program check if user A has written the ticket (if yes gonna set a ticket_form containing the forms.Ticket_forms) in this case no so its gonna make the same with the review (check and set review_form)
>then respond the html page containg the seted form or object 

concretly

if you have written only the review its gonna send the ticket as an object and not a form and the rview as a form 
if you have written the two then respond the two as form 
so you cant edit what you havent write 

the Content_page class

work thanks to two sub method 
the get_userlist(request ,feed = False) which fetch the user then if followed = True all followed user and  after return the userlist 
the get_content(userlist) method which fetch all review and ticket independly from userlist and add them all to a content list and then return it 
so the get method work quite simply : 

```python
def get(self, request):  
    userlist = self.get_userlist(request)  #get all user in a list
    contentlist = self.get_content(userlist)  # get all content in a list
    return render(request, self.template_url,  
                  context={'contentlist': contentlist}) # return the page with the content list as context 
```

and the Content_delete class

witch check if we can delete and delete the following content