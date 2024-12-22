from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Reservation, Post, Comment

User = get_user_model()

class ReservationViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_create_reservation_success(self):
        data = {
            "date": "2024-12-20",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "max_participants": 5,
            "is_open": True
        }
        response = self.client.post('/bookingapi/reservation/', data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_create_reservation_failed(self):
        data = {
            "date": "",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "max_participants": 5,
            "is_open": True
        }
        response = self.client.post('/bookingapi/reservation/', data)  
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_create_reservation_unauthenticated(self):
        self.client.logout()
        data = {
            "date": "2024-12-20",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "max_participants": 5,
            "is_open": True
        }
        response = self.client.post('/bookingapi/reservation/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Reservation.objects.count(), 0)

    def test_create_reservation_end_time_before_start_time(self):
        data = {
            "date": "2024-12-20",
            "start_time": "14:00:00",
            "end_time": "12:00:00",  
            "max_participants": 5,
            "is_open": True
        }
        response = self.client.post('/bookingapi/reservation/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Reservation.objects.count(), 0)


    def test_create_reservation_time_conflict(self):
        existing_reservation = Reservation.objects.create(
            user=self.user,
            date="2024-12-20",
            start_time="10:00:00",
            end_time="12:00:00",
            max_participants=5,
            is_open=True
        )
        data = {
            "date": "2024-12-20",
            "start_time": "11:00:00", 
            "end_time": "13:00:00",    
            "max_participants": 5,
            "is_open": True
        }

        response = self.client.post('/bookingapi/reservation/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'This time slot is already booked on this day!')


class ReservationRetrieveTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.other_user = User.objects.create_user(email='otheruser', password='password123')
        
        self.reservation = Reservation.objects.create(
            user=self.user,
            date="2024-12-20",
            start_time="10:00:00",
            end_time="12:00:00",
            max_participants=5,
            is_open=True
        )
        
        self.other_reservation = Reservation.objects.create(
            user=self.other_user,
            date="2024-12-21",
            start_time="14:00:00",
            end_time="16:00:00",
            max_participants=5,
            is_open=True
        )

    def test_get_reservations_unauthenticated(self):
        self.client.logout()  
        response = self.client.get('/bookingapi/reservation/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_reservations_authenticated(self):
        response = self.client.get('/bookingapi/reservation/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 

    def test_get_single_reservation_authenticated(self):
        response = self.client.get(f'/bookingapi/reservation/{self.reservation.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.reservation.id)

    def test_get_single_reservation_not_owned(self):
        response = self.client.get(f'/bookingapi/reservation/{self.other_reservation.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Reservation not found or you do not have permission to access this reservation.')


class ReservationDeleteTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

        self.other_user = User.objects.create_user(email='otheruser', password='password123')

        self.reservation = Reservation.objects.create(
            user=self.user,
            date="2024-12-20",
            start_time="10:00:00",
            end_time="12:00:00",
            max_participants=5,
            is_open=True
        )

        self.other_reservation = Reservation.objects.create(
            user=self.other_user,
            date="2024-12-21",
            start_time="14:00:00",
            end_time="16:00:00",
            max_participants=5,
            is_open=True
        )

    def test_delete_reservation_success(self):
        response = self.client.delete(f'/bookingapi/reservation/{self.reservation.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Reservation.objects.count(), 1) 

    def test_delete_reservation_unauthenticated(self):
        self.client.logout()  
        response = self.client.delete(f'/bookingapi/reservation/{self.reservation.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_delete_reservation_not_found_or_not_owned(self):
        response = self.client.delete(f'/bookingapi/reservation/{self.other_reservation.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Reservation not found or you do not have permission to delete this reservation.')

    def test_delete_reservation_not_found(self):
        response = self.client.delete('/bookingapi/reservation/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Reservation not found or you do not have permission to delete this reservation.')


class ReservationEditTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.user2 = User.objects.create_user(email='testuser2@example.com', password='password123')
        self.client.force_authenticate(user=self.user)
        self.reservation = Reservation.objects.create(
            user=self.user,
            date="2024-12-20",
            start_time="10:00:00",
            end_time="12:00:00",
            max_participants=5,
            is_open=True
        )

        self.reservation.participants.add(self.user)
        self.reservation.participants.add(self.user2)


    def test_put_reservation_success(self):
        data = {
            "max_participants": 10,
            "is_open": False
        }

        response = self.client.put(f'/bookingapi/reservation/{self.reservation.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.max_participants, 10)
        self.assertEqual(self.reservation.is_open, False)

    def test_put_reservation_max_participants_less_than_current(self):
        data = {
            "max_participants": 1  
        }

        response = self.client.put(f'/bookingapi/reservation/{self.reservation.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'New max participants cannot be less than current participants count!')
    
    def test_put_reservation_not_authenticated(self):
        self.client.logout()

        data = {
            "max_participants": 10,
            "is_open": False
        }

        response = self.client.put(f'/bookingapi/reservation/{self.reservation.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_put_reservation_not_found(self):
        invalid_id = 9999  
        data = {
            "max_participants": 10,
            "is_open": False
        }

        response = self.client.put(f'/bookingapi/reservation/{invalid_id}/', data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Reservation not found or you do not have permission to edit this reservation.')

    def test_put_reservation_invalid_data(self):
        data = {
            "max_participants": -1,  
            "is_open": True
        }

        response = self.client.put(f'/bookingapi/reservation/{self.reservation.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('max_participants', response.data)


class JoinReservationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.user2 = User.objects.create_user(email='testuser2@example.com', password='password123')
        self.user3 = User.objects.create_user(email='testuser3@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

        self.reservation = Reservation.objects.create(
            user=self.user2,
            date="2024-12-20",
            start_time="10:00:00",
            end_time="12:00:00",
            max_participants=2,
            is_open=True
        )

    def test_join_reservation_success(self):
        response = self.client.post(f'/bookingapi/reservation/{self.reservation.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'You have successfully joined the reservation!')
        self.assertIn(self.user, self.reservation.participants.all())
    
    def test_join_reservation_not_authenticated(self):
        self.client.logout()
        response = self.client.post(f'/bookingapi/reservation/{self.reservation.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_join_reservation_not_found(self):
        invalid_id = 9999
        response = self.client.post(f'/bookingapi/reservation/{invalid_id}/join/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Reservation not found!')


    def test_join_reservation_already_participant(self):
        self.reservation.participants.add(self.user)
        response = self.client.post(f'/bookingapi/reservation/{self.reservation.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'You are already a participant in this reservation!')

    def test_join_reservation_own_reservation(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/bookingapi/reservation/{self.reservation.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'You cannot join your own reservation!')

    def test_join_reservation_full(self):
        self.reservation.participants.add(self.user3)
        self.reservation.participants.add(self.user2)
        response = self.client.post(f'/bookingapi/reservation/{self.reservation.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'This reservation is closed or full!')

    def test_join_reservation_closed(self):
        self.reservation.is_open = False
        self.reservation.save()
        response = self.client.post(f'/bookingapi/reservation/{self.reservation.id}/join/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'This reservation is closed or full!')


class ParticipantReservationsTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.user2 = User.objects.create_user(email='testuser2@example.com', password='password123')
        self.user3 = User.objects.create_user(email='testuser3@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

        self.reservation1 = Reservation.objects.create(
            user=self.user2,
            date="2024-12-20",
            start_time="10:00:00",
            end_time="12:00:00",
            max_participants=5,
            is_open=True
        )
        self.reservation1.participants.add(self.user)

        self.reservation2 = Reservation.objects.create(
            user=self.user3,
            date="2024-12-21",
            start_time="14:00:00",
            end_time="16:00:00",
            max_participants=5,
            is_open=True
        )
        self.reservation2.participants.add(self.user)

        self.reservation3 = Reservation.objects.create(
            user=self.user,
            date="2024-12-22",
            start_time="10:00:00",
            end_time="12:00:00",
            max_participants=5,
            is_open=True
        )

    def test_get_reservations_success(self):
        response = self.client.get('/bookingapi/reservations/joined/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  
        reservation_ids = [res['id'] for res in response.data]
        self.assertIn(self.reservation1.id, reservation_ids)
        self.assertIn(self.reservation2.id, reservation_ids)
        self.assertNotIn(self.reservation3.id, reservation_ids)  

    def test_get_reservations_not_authenticated(self):
        self.client.logout()
        response = self.client.get('/bookingapi/reservations/joined/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_reservations_no_participation(self):
        self.client.force_authenticate(user=self.user3)  
        response = self.client.get('/bookingapi/reservations/joined/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  

class LeaveReservationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.user2 = User.objects.create_user(email='testuser2@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

        self.reservation = Reservation.objects.create(
            user=self.user2,
            date="2024-12-20",
            start_time="10:00:00",
            end_time="12:00:00",
            max_participants=5,
            is_open=True
        )
        self.reservation.participants.add(self.user)

    def test_leave_reservation_success(self):
        response = self.client.post(f'/bookingapi/reservation/{self.reservation.id}/leave/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'You have successfully left the reservation!')
        self.assertNotIn(self.user, self.reservation.participants.all())

    def test_leave_reservation_not_authenticated(self):
        self.client.logout()
        response = self.client.post(f'/bookingapi/reservation/{self.reservation.id}/leave/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_leave_reservation_not_found(self):
        invalid_reservation_id = 9999
        response = self.client.post(f'/bookingapi/reservation/{invalid_reservation_id}/leave/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Reservation not found!')

    def test_leave_reservation_not_participant(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(f'/bookingapi/reservation/{self.reservation.id}/leave/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'You are not a participant in this reservation!')

class ReservationParticipantTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.user2 = User.objects.create_user(email='testuser2@example.com', password='password123')
        self.user3 = User.objects.create_user(email='testuser3@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

        self.reservation = Reservation.objects.create(
            user=self.user,
            date="2024-12-20",
            start_time="10:00:00",
            end_time="12:00:00",
            max_participants=5,
            is_open=True
        )
        self.reservation.participants.add(self.user2)

    def test_remove_participant_success(self):
        response = self.client.delete(f'/bookingapi/reservation/{self.reservation.id}/participant/{self.user2.id}/remove/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'User has been removed from the reservation successfully!')
        self.assertNotIn(self.user2, self.reservation.participants.all())

    def test_remove_participant_not_authenticated(self):
        self.client.logout()
        response = self.client.delete(f'/bookingapi/reservation/{self.reservation.id}/participant/{self.user2.id}/remove/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_remove_participant_reservation_not_found(self):
        invalid_reservation_id = 9999
        response = self.client.delete(f'/bookingapi/reservation/{invalid_reservation_id}/participant/{self.user2.id}/remove/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Reservation not found or you do not have permission to remove a participant.')

    def test_remove_participant_user_not_found(self):
        invalid_user_id = 9999
        response = self.client.delete(f'/bookingapi/reservation/{self.reservation.id}/participant/{invalid_user_id}/remove/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User not found!')

    def test_remove_participant_not_in_reservation(self):
        response = self.client.delete(f'/bookingapi/reservation/{self.reservation.id}/participant/{self.user3.id}/remove/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'This user is not a participant in this reservation!')

class PostViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='password123')
        self.user2 = get_user_model().objects.create_user(email='testuser2@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

        self.reservation = Reservation.objects.create(
            user=self.user,
            date="2024-12-20",
            start_time="10:00:00",
            end_time="12:00:00",
            max_participants=5,
            is_open=True
        )

        self.post = Post.objects.create(
            content="Test content",
            user=self.user,
            reservation=self.reservation
    )

    def test_create_post_success(self):
        data = {
            'content': 'Test content for post',
            'reservationId': self.reservation.id
        }
        response = self.client.post('/bookingapi/post/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Test content for post')
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['reservation']['id'], self.reservation.id)

    def test_create_post_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {
            'content': 'Test content for post',
            'reservationId': self.reservation.id
        }
        response = self.client.post('/bookingapi/post/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_create_post_reservation_not_found(self):
        data = {
            'content': 'Test content for post',
            'reservationId': 99999 
        }
        response = self.client.post('/bookingapi/post/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Reservation not found')

    def test_create_post_missing_content(self):
        data = {
            'reservationId': self.reservation.id
        }
        response = self.client.post('/bookingapi/post/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)

    def test_create_post_invalid_reservation(self):
        other_reservation = Reservation.objects.create(
            user=self.user2,
            date="2024-12-21",
            start_time="14:00:00",
            end_time="16:00:00",
            max_participants=5,
            is_open=True
        )

        data = {
            'content': 'Test content for post',
            'reservationId': other_reservation.id
        }
        response = self.client.post('/bookingapi/post/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['reservation']['id'], other_reservation.id)
        self.assertEqual(response.data['user']['id'], self.user.id)

    def test_create_post_no_reservation_id(self):
        data = {
            'content': 'Test content for post'
        }
        response = self.client.post('/bookingapi/post/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Test content for post')
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertIsNone(response.data.get('reservation'))
    
    def test_get_post_by_id_success(self):
        response = self.client.get(f'/bookingapi/post/{self.post.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.post.id)
        self.assertEqual(response.data['content'], self.post.content)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['reservation']['id'], self.reservation.id)

    def test_get_post_by_id_not_found(self):
        response = self.client.get('/bookingapi/post/99999/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Post not found or you do not have permission to access this post.')

    def test_get_posts_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/bookingapi/post/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_all_posts_success(self):
        response = self.client.get('/bookingapi/posts/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.post.id)
        self.assertEqual(response.data[0]['content'], self.post.content)

    def test_get_all_posts_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/bookingapi/posts/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_delete_post_success(self):
        response = self.client.delete(f'/bookingapi/post/{self.post.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_delete_post_not_found(self):
        response = self.client.delete('/bookingapi/post/99999/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Post not found.')

    def test_delete_post_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(f'/bookingapi/post/{self.post.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')


class CommentViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='password123')
        self.user2 = get_user_model().objects.create_user(email='testuser2@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

        self.reservation = Reservation.objects.create(
            user=self.user,
            date="2024-12-20",
            start_time="10:00:00",
            end_time="12:00:00",
            max_participants=5,
            is_open=True
        )

        self.post = Post.objects.create(
            content="Test content",
            user=self.user,
            reservation=self.reservation
        )

        self.comment = Comment.objects.create(
            content="This is a test comment",
            user=self.user,
            post=self.post
        )

    def test_create_comment_success(self):
        data = {
            'content': 'This is a test comment'
        }
        response = self.client.post(f'/bookingapi/post/{self.post.id}/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'This is a test comment')
        self.assertEqual(response.data['user']['id'], self.user.id)  # poprawiono
        self.assertEqual(response.data['post'], self.post.id)

    def test_create_comment_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {
            'content': 'This is a test comment'
        }
        response = self.client.post(f'/bookingapi/post/{self.post.id}/comments/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_create_comment_post_not_found(self):
        data = {
            'content': 'This is a test comment'
        }
        response = self.client.post('/bookingapi/post/99999/comments/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Post not found!')

    def test_create_comment_missing_content(self):
        data = {}
        response = self.client.post(f'/bookingapi/post/{self.post.id}/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('content', response.data)

    def test_get_comment_by_id_success(self):
        response = self.client.get(f'/bookingapi/comment/{self.comment.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.comment.id)
        self.assertEqual(response.data['content'], self.comment.content)
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['post'], self.post.id)

    def test_get_comment_by_id_not_found(self):
        response = self.client.get('/bookingapi/comment/99999/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Comment not found!')

    def test_get_comments_by_post_success(self):
        response = self.client.get(f'/bookingapi/post/{self.post.id}/comments/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.comment.id)
        self.assertEqual(response.data[0]['content'], self.comment.content)
        self.assertEqual(response.data[0]['user']['id'], self.user.id)  # poprawiono
        self.assertEqual(response.data[0]['post'], self.post.id)

    def test_get_comments_by_post_not_found(self):
        response = self.client.get('/bookingapi/post/99999/comments/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Post not found!')

    def test_get_comments_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/bookingapi/post/{self.post.id}/comments/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_delete_comment_success(self):
        response = self.client.delete(f'/bookingapi/comment/{self.comment.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_delete_comment_not_found(self):
        response = self.client.delete('/bookingapi/comment/99999/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Comment not found or you do not have permission to delete this comment.')

    def test_delete_comment_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(f'/bookingapi/comment/{self.comment.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_get_all_comments_success(self):
        response = self.client.get('/bookingapi/comments/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.comment.id)
        self.assertEqual(response.data[0]['content'], self.comment.content)
        self.assertEqual(response.data[0]['user']['id'], self.user.id)
        self.assertEqual(response.data[0]['post'], self.post.id)

    def test_get_all_comments_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/bookingapi/comments/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')



