from django.db.models import QuerySet, Q, Sum


class CustomQuerySet(QuerySet):
    '''
    Custom queryset that will be reused by different models.
    It enables soft delete and precise filtering, (ie to get all
    property that has not been soft deleted, simply run:
        Property.active_objects.all_objects()
        )
    '''

    def _active(self):
        '''Return only objects that haven't been soft deleted.'''
        return self.filter(is_deleted=False)

    def _total(self):
        '''Return only objects that haven't been soft deleted.'''
        return self.filter(is_deleted=False).count()

    def all_objects(self):
        '''Return all objects that haven't been soft deleted'''
        return self._active()

    def all_approved(self):
        '''Return client companies that are approved'''
        return self._active().filter(approval_status='approved')

class RegistrationQuery(CustomQuerySet):
    '''Queryset that will be used for ClientAccount model'''

    def all_published(self):
        """Returns all property that is published"""
        return self._active().filter(is_published=True)

    def not_deleted(self, owner):
        '''Return client details that are not deleted'''
        return self._active().filter(owner=owner)

    def client_admin_has_client(self, client_admin_id):
        '''check if client Admin has an Client Account
        if not do not enable him/her to submit account details'''
        return self._active().filter(owner_id=client_admin_id)

class RegistrationEnquiryQuery(CustomQuerySet):
    """ Queryset for the Enquiry property """

    def for_user(self, user):
        """ returns all the queries made by a buyer """
        return self._active().filter(requester=user)

    def for_client(self, client):
        """ return all the queires made for a certain client """
        return self._active().filter(client=client)
