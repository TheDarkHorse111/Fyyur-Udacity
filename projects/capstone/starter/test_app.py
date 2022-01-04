import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database_models.models import setup_db, Actor, Movie



class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        #replace this token with a new Executive Producer token 
        self.access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpsTzkzNXQ0TTVPN3lWdVlaNFhNVyJ9.eyJpc3MiOiJodHRwczovL2Rldi1oMmswMjB1Zi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkMGE3MDlmYTJjZDEwMDY5ZWU0ZGViIiwiYXVkIjoiY2FzdGluZ19hZ2VuY3lfYXBpIiwiaWF0IjoxNjQxMzA1NjgyLCJleHAiOjE2NDEzMTI4ODIsImF6cCI6IkYwQXRzcEFHTGp2QW1sMmI0dXk4eUpqd05ENG5JaTBFIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.Z0aoMMi4BAHYMYXISn2X5fmb5_iO7PFbdyB3DXZjewUR0d6D1q03ZHVa3E9SH-O1qmfOhsXPQ3z4DLDu-jnC1zj95c8cP0nmuunJdS4UfErrZygaaowyShrV4jSDpyvtmIAmcCVnKO53FASnx8WJPneyKNneIDJZWQDKSbiq7ikW93pLxSqbcKH9tLkcWN-rPMjeSZPOZUzNkG8dvvN1JRZff26c2FaNLwVfvk0FTu6qok4vkOOypoj3IqVpxhowpWvdfdLpm5LoDwqwkU1j8x_ifzt2MJtDsUG2_EOsosSDymr4wF-J4JkcUg0w0N6rZAHwT9M-oLTMg6lmyqyBEg'
        #replace this token with a Casting Assistant or Casting Director token 
        self.test_token ='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpsTzkzNXQ0TTVPN3lWdVlaNFhNVyJ9.eyJpc3MiOiJodHRwczovL2Rldi1oMmswMjB1Zi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFkMmUzNDExZTEzZGQwMDY4YzYyMjQ4IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3lfYXBpIiwiaWF0IjoxNjQxMzA3NjA5LCJleHAiOjE2NDEzMTQ4MDksImF6cCI6IkYwQXRzcEFHTGp2QW1sMmI0dXk4eUpqd05ENG5JaTBFIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.T48G7Olp7-EHP1PMvIlETWQt1zb8p_u6k1Vaoh4OCGp9a9wD9hrNVyST0BJ5zr0yhzhttfD1QTz_R_DZ9MyLhB6XrYfh-SF6iW_pLSc7QfNvnsInQdoj7cAfYTCT75RSz3R143fZaaBDf-2juLSktzs8RARy8pZlv1jyyrLm77G7-H5pqtAP_NJn5FX0sw8kszqyToBFHwCm1VqYBo8tXM2BpcJaxOfyTPh4eVBDkbEN1eb5H01Hvdj3Mm6dID6kMK1grO1JTuwh4WqXc_fP54Qt2JPz0DDvsPJJPeRpaWrHvdsJVsT8Fq_uxmZtDAaRBxlofrl5-8airi1J2QLC0w'
        self.headers = {
        'Authorization': 'Bearer {}'.format(self.access_token)
        }
        self.test_headers = {
        'Authorization': 'Bearer {}'.format(self.test_token)
        }
        DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
        DB_NAME = os.getenv('DB_NAME', 'casting_agency_test')
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
        setup_db(self.app, self.database_path)
        self.new_actor = {'name':'Jeff', 'age':12, 'gender':'Male'}
        self.new_movie = {'title': 'The Cool Kids', 'release_date': '2022-1-1'}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_paginated_actors(self):
        res = self.client().get('/actors', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors_total_number"])
        self.assertTrue(len(data["current_actors"]) <= 10)


    def test_get_paginated_movies(self):
        res = self.client().get('/movies', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies_total_number"])
        self.assertTrue(len(data["current_movies"]) <= 10)

    

    def test_404_sent_requesting_beyond_valid_page_for_actors(self):
        res = self.client().get("/actors?page=1000", headers=self.headers, json={"random json": "some value"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_404_sent_requesting_beyond_valid_page_for_movies(self):
        res = self.client().get("/movies?page=1000", headers=self.headers, json={"random json": "some value"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")



    def test_200_delete_actor(self):
        res = self.client().delete("/actors/1", headers=self.headers)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 1)
        self.assertEqual(actor, None)

    
    def test_200_delete_movie(self):
        res = self.client().delete("/movies/1", headers=self.headers)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 1)
        self.assertEqual(movie, None)

    def test_404_if_actor_does_not_exist(self):
        res = self.client().delete("/actors/1000", headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    def test_404_if_movie_does_not_exist(self):
        res = self.client().delete("/movies/1000", headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    def test_create_new_actor(self):
        res = self.client().post("/actors", headers=self.headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


    def test_create_new_movie(self):
        res = self.client().post("/movies", headers=self.headers, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


    def test_400_if_actor_creation_not_allowed_due_to_bad_request(self):
        res = self.client().post("/actors", headers=self.headers, json={'something_wrong':'about this json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")


    def test_400_if_movie_creation_not_allowed_due_to_bad_request(self):
        res = self.client().post("/movies", headers=self.headers, json={'something_wrong':'about this json'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_patch_actor(self):
        res = self.client().patch('/actors/2', headers=self.headers, json={'name':'Steve', 'age':22, 'gender':'Male'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_patch_movie(self):
        res = self.client().patch('/movies/2', headers=self.headers, json={'title': 'The kids who thought they were cool', 'release_date': '2022-12-1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


    def test_405_on_patch_actor(self):
        res = self.client().patch('/actors', headers=self.headers, json={'name':'Steve', 'age':22, 'gender':'Male'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_405_on_patch_movie(self):
        res = self.client().patch('/movies', headers=self.headers, json={'title': 'The kids who thought they were cool', 'release_date': '2022-12-1'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")


    def test_403_unauthorized_delete_movie_without_required_permission(self):
        res = self.client().delete("/movies/1", headers=self.test_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], 'unauthorized')
        self.assertEqual(data["description"], "Permission not found.")

    def test_403_unauthorized_post_movie_without_required_permission(self):
        res = self.client().post("/movies", headers=self.test_headers, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], 'unauthorized')
        self.assertEqual(data["description"], "Permission not found.")

    def test_403_unauthorized_delete_actor_without_required_permission(self):
        res = self.client().delete("/actors/1", headers=self.test_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], 'unauthorized')
        self.assertEqual(data["description"], "Permission not found.")

    def test_403_unauthorized_post_actor_without_required_permission(self):
        res = self.client().post("/actors", headers=self.test_headers, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["code"], 'unauthorized')
        self.assertEqual(data["description"], "Permission not found.")

       
    
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()