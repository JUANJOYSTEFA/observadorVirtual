def session_variables(request):
    return {
        # Cambia 'mi_variable' por el nombre de tu variable de sesión
        'isLogged': request.session.get('isLogged', None),
        # Otra variable de sesión
        'userId': request.session.get('userId', None),
        'userType': request.session.get('userType', None),
        'userNombre': request.session.get('userNombre', None)
    }
