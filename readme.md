# Project description
> web solution allowing a community of users to request or post book reviews

## How to install and run the project
The project requirement are :
- python 3.X,
- django 2.X,

and are specified in the requirement.txt file.

### How to install it
- on the terminal type the following command to clone the github to the working directory 
```zsh
git clone https://github.com/toutouff/Projet_9_django
```
- create the pip virtual environement 
```zsh
python3 venv Name_of_the_Venv 
```
- then, install all the required packages 
```zsh
pip install -r requirement.txt
```
- finally, source the Virtual environement
on OSX/Unix: 
```zsh 
source Name_of_the_Venv/bin/activate 
```
- on Windows
```powershell
.\Name_of_the_Venv\Scripts\activate
```
### Run the project

```zsh
python3 LITReview/manage.py runserver 
```
>If you want to run it on a specific IP (like the IP of your computer rather than the localhost (127.0.0.1:8000) you can specify it 
>```zsh
> python3 LITReview/manage.py runserver 192.168.1.X:8000
>```


## Basic structure and explanation of what it does 
The project is constitued of 2 app 
- the blog app 
- the Auth app 

### The blog app 

This app serves all the site views and logics exept for login and signup

#### models.py
```python
class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    image = models.ImageField(blank=True ,null=True,upload_to='Blog')
    time_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_closed = models.BooleanField(default= False) 

```
the ```is_closeed``` was added to the database so it can register when a ticket as been responded 

#### Views.py
all the views are Class Based and inherit of the View class from django.views .
There are 4 fundamental views 
- **The Follow class**
  - The get method : generates the follow page which shows all the followers' username, usernames of users we follow  and an username search bar (to follow users).  
  - The post method : gets an username from the 'searchbar' key inside request.POST data. Then it gets the user from the database coresponding to the username and if the searched user exists, it's gonna create a UserFollows object.


- **The Content_create class** 
  - as two global parameters wich store either the Ticket or Review Form wich are set when calling the view.
  - Then the get method serve the selected form 
    - _**exemple**_ :
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
  - The post method will check what it receives from the request.POST data and will fill and save the different object in the database.
- **The Content_edit class** 
  - works quite as same as the Content_create class but it adds a security overlay by insuring that user are allowed to edit what they're willing to update. 
  - Example :
    - You are User A and you respond to a ticket from User B 
      - You want to edit your review, let's see how the server will handle it and respond to your request. 
      - The server receives a /blog/ticket/*ticket_id*/edit? request
      - It will get the ticket with the ticket_id value,
      - then check if a review exists. 
        - If the answer is "yes" it will be temporaly stored.
      - After the program checks if User A has written the ticket :
        - if yes : it sets a ticket_form containing the forms.Ticket_forms) in this case  
        - if no : it does the same with the review (check and set review_form), then it responds the html page which contains the selected form or object

> Concretely :
> - if you have written only the review :
>   - it will send the ticket as an object and the review as a form
> - if you have written only the ticket :
>   - it will send the ticket as a form and the review as an object
> - if you have written both :
>   - it will send the ticket as a form and the review as a form
> 
> **So you cannot edit what you did not write.**



- **The Content_page class**
  - It work thanks to two sub method.
    - The get_userlist(request ,feed = False) which fetches the user then if followed = True all followed user ...... and after return the userlist 
    - The get_content(userlist) method which fetches all reviews and tickets independly from userlist and add them all to a content list and then return it.
  - So the get method works quite simply : 
```python
def get(self, request):  
    userlist = self.get_userlist(request)  #get all user in a list
    contentlist = self.get_content(userlist)  # get all content in a list
    return render(request, self.template_url,  
                  context={'contentlist': contentlist}) # return the page with the content list as context 
```

- **the Content_delete class** 
  - which checks if we can delete, 
    - and if yes, it deletes the following content.