# from django.test import TestCase
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.urls import reverse
# from .models import User

# class FaceAuthenticationTest(TestCase):
#     def setUp(self):
#         # Create a user with a profile image in the `media/profile_pics/` folder
#         self.user = User.objects.create(username="testuser", role="student", profile_image="testuser.jpg")
#         # Replace 'testuser.jpg' with the actual path to the test image in `media/profile_pics`

#     def test_authenticate_with_face(self):
#         with open("path_to_test_upload_image.jpg", "rb") as img_file:
#             upload_image = SimpleUploadedFile("upload.jpg", img_file.read(), content_type="image/jpeg")
#             response = self.client.post(reverse("authenticate_with_face"), {"photo": upload_image})

#         # Check if the authentication succeeded
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("token", response.json())
