import unittest
import tempfile
import json
from movie_library import MovieLibrary

class TestMovieLibrary(unittest.TestCase):
    def setUp(self):
        self.app = MovieLibrary.__new__(MovieLibrary)
        self.app.movies = []

    def test_validate_positive(self):
        valid, msg = self.app.validate_movie("Inception", "Sci-Fi", "2010", "8.8")
        self.assertTrue(valid)

    def test_validate_empty_title(self):
        valid, msg = self.app.validate_movie("", "Drama", "2020", "7.5")
        self.assertFalse(valid)
        self.assertIn("Название", msg)

    def test_validate_year_not_number(self):
        valid, msg = self.app.validate_movie("Titanic", "Romance", "abc", "8.0")
        self.assertFalse(valid)
        self.assertIn("целым числом", msg)

    def test_validate_year_boundary(self):
        valid, msg = self.app.validate_movie("Old", "History", "1888", "5.0")
        self.assertTrue(valid)
        valid, msg = self.app.validate_movie("Future", "Sci-Fi", "2026", "6.0")
        self.assertTrue(valid)
        valid, msg = self.app.validate_movie("Invalid", "Fantasy", "2027", "6.0")
        self.assertFalse(valid)

    def test_validate_rating_out_of_range(self):
        valid, msg = self.app.validate_movie("Bad", "Comedy", "2000", "11.0")
        self.assertFalse(valid)
        valid, msg = self.app.validate_movie("Good", "Action", "2000", "-1")
        self.assertFalse(valid)

if __name__ == "__main__":
    unittest.main()