from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import Response

import requests
import os
import json

BACKEND_URL = os.environ['BACKEND_URL']  # From docker-compose.yml
FRONTEND_PORT = 6543                     # This is the port number for the frontend server


#----------------------Helper Functions-------------------------
def show_home(req):
    return render_to_response('templates/home.html', {}, request=req)
    

def show_users(req):
    response = requests.get(BACKEND_URL + "/get_users")

    # If GET has succeeded
    if (response.status_code == 200):
        users = response.json()
        return render_to_response('templates/users.html', {"users": users}, request=req)
    else:
        return Response(response.text)

def add_user(req):
    new_user = req.POST.mixed()
    response = requests.post(BACKEND_URL + "/add_user", data=new_user)
    
    # If POST accepted
    if (response.status_code == 201):
        # Decide what to do with a after adding user!
        response = requests.get(BACKEND_URL + "/get_users")
        users = response.json()
        return render_to_response('templates/users.html', {"users": users}, request=req)

    else:
        return Response("Error: Please check your form for correct field names. They MUST match the keys of the DB dictionary!")


def edit_user_form(req):
     return render_to_response('templates/editUser.html', {}, request=req)


def edit_user(req):
    # Add loginc to edit user here:
    user = req.POST.mixed()
    response = requests.post(BACKEND_URL + "/edit_user", data=user)
    
    # If POST accepted
    if (response.status_code == 201):
        # return home if successful
        return render_to_response('templates/home.html', {}, request=req)

    else:
        return Response("Error: Please check your form for correct username and password")



def show_moves(req):
    response = requests.get(BACKEND_URL + "/get_tello_moves")

    # If GET has succeeded
    if (response.status_code == 200):
        moves = response.json()
        return render_to_response('templates/moves.html', {"moves": moves}, request=req)
    else:
        return Response(response.text)


if __name__ == '__main__':
    config = Configurator()
    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')


    #--------------------------Routes---------------------------
    # Route for default route
    config.add_route('home', '/')
    config.add_view(show_home, route_name='home')

    # Route to view users
    config.add_route('show_users', '/show_users')
    config.add_view(show_users, route_name='show_users')

    # Route to add a user
    # NOTE: request_method='POST'
    config.add_route('add_user', '/add_user')
    config.add_view(add_user, route_name='add_user', request_method='POST')


    # Route to the form for edit user
    config.add_route('edit_user_form', '/edit_user_form')
    config.add_view(edit_user_form, route_name='edit_user_form')


    # Route to edit a user
    # Add route to edit user (POST request)
    # NOTE: route must be '/edit_user'
    config.add_route('edit_user', '/edit_user')
    config.add_view(edit_user, route_name='edit_user')


    # Route to show moves
    # Add route to show moves (GET request)
    # NOTE: Use 'show_users' as inspiration
    # NOTE: route must be '/show_moves'
    config.add_route('show_moves', '/show_moves')
    config.add_view(show_moves, route_name='show_moves')

    #------------------------Add static view (for css)----------
    config.add_static_view(name='/', path='./public', cache_max_age=3600)


    # Create 'app' and server and run it forever!
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', FRONTEND_PORT, app)
    server.serve_forever()
