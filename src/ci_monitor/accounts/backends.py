
class ActiveDirectoryGroupMembershipSSLBackend:

	def authenticate(self,username=None,password=None):
		try:
			if len(password) == 0:
				return None
			ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,settings.AD_CERT_FILE)
			l = ldap.initialize(settings.AD_LDAP_URL)
			l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
			binddn = "%s@%s" % (username,settings.AD_NT4_DOMAIN)
			l.simple_bind_s(binddn,password)
			l.unbind_s()
			return self.get_user(username,password)
			
			
	def get_user(self, username, password):
		try:
			user = User.objects.get(username=username)
			if user.check_password(password):
				return user
		except User.DoesNotExist:
			return None
			
		except MultipleObjectsReturned:
			return None