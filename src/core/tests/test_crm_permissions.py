# flake8: noqa:E501
# pylint: disable=invalid-name
# pylint: disable=protected-access
# pylint: disable=line-too-long
from django.test import Client, TestCase
from django.urls import reverse

from core.models import User
from core.urls.crm_urls import urlpatterns as crm_urlpatterns


class CrmPermissionsTestCase(TestCase):
    """Crm Permissions TestCase"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="test", password="test")  # type: ignore

    def test_WhenNotAuthenticatedStaffMember_Then401Unauthorized(self):
        """
        If:
            - unauthenticated user
            OR
            - authenticated non-staff user
        tries to:
            access CRM pages
        then:
            raise `401 Unauthorized`
        """

        self.user.is_staff = False
        self.user.save()

        client = Client()
        client.force_login(self.user)

        # Assert there are patterns present
        self.assertNotEqual(len(crm_urlpatterns), 0)

        for urlpattern in crm_urlpatterns:
            # Try to get urlpattern's name
            try:
                urlpattern.name
            except AttributeError:
                # It's not a `path` object, skip
                continue

            if "<int:pk>" in urlpattern.pattern._route:
                url = reverse(f"core:{urlpattern.name}", kwargs={"pk": 1})
            else:
                url = reverse(f"core:{urlpattern.name}")

            response = client.get(url, follow=True)
            status_code = response.status_code

            # Assert that response status code is 401
            self.assertEqual(status_code, 401)

    def test_WhenAuthenticatedStaffMember_ThenGrantAccess(self):
        """
        If authentizated staff member tries to access CRM pages then
        allow them
        """

        self.user.is_staff = True
        self.user.save()

        client = Client()
        client.force_login(self.user)

        # Assert there are patterns present
        self.assertNotEqual(len(crm_urlpatterns), 0)

        for urlpattern in crm_urlpatterns:
            # Try to get urlpattern's name
            try:
                urlpattern.name
            except AttributeError:
                # It's not a `path` object, skip
                continue

            if "<int:pk>" in urlpattern.pattern._route:
                url = reverse(f"core:{urlpattern.name}", kwargs={"pk": 1})
            else:
                url = reverse(f"core:{urlpattern.name}")

            response = client.get(url, follow=True)
            status_code = response.status_code

            # Assert that response status code is 401
            self.assertNotEqual(status_code, 401)
