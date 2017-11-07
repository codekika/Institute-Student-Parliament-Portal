def is_user_authenticate(request):
	if request.session.has_key('user_id'):
		return { 'user':True}
	else:
		return { 'user':False}

