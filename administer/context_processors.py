def is_user_authenticate(request):
	if request.session.has_key('admin'):
		return { 'admin':True}
	else:
		return { 'admin':False}

