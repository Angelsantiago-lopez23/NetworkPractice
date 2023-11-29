# Going to import the website package and grab the create app package just done. 
from website import create_app

app = create_app()

if __name__ == '__main__':
    # True: Anytime we run it will upload changes. False: Once in production
    app.run(debug=True)

#Put html in templates folder. When you rent your html you call it a template
#Is called a template because there is a special template langauge with flask. Called Jinga 
#Allow you to write a little bit of python language inside the html. So you won't have to render it 
#using javascript. 

