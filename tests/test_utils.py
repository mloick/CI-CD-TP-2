from src.utils import capitalize, calculate_average, slugify, clamp, sort_students

class TestUtils:
    def test_capitalize(self):
        assert capitalize("hello") == "Hello"
        assert capitalize("WORLD") == "World"
        assert capitalize("jOHn") == "John"
        assert capitalize("") == ""
        assert capitalize(None) == ""
        assert capitalize(123) == ""

    def test_calculate_average(self):
        assert calculate_average([1, 2, 3]) == 2.0
        assert calculate_average([1.5, 2.5, 3.5]) == 2.5
        assert calculate_average([10, 20.555, 30]) == 20.18
        assert calculate_average([]) == 0.0
        assert calculate_average(None) == 0.0
        assert calculate_average(["a", "b"]) == 0.0

    def test_slugify(self):
        assert slugify("Hello World") == "hello-world"
        assert slugify(" Café & Croissant! ") == "caf-croissant"
        assert slugify("---Test---") == "test"
        assert slugify("") == ""
        assert slugify(None) == ""
        assert slugify("123!@#    456") == "123-456"

    def test_clamp(self):
        assert clamp(10, 0, 20) == 10
        assert clamp(-5, 0, 20) == 0
        assert clamp(25, 0, 20) == 20
        assert clamp(None, 0, 20) == 0
        assert clamp(10, 20, 30) == 20
        assert clamp("10", 0, 20) == 0

class TestSortStudents:
    def test_sort_students_grade_asc(self):
        students = [{"name": "A", "grade": 10}, {"name": "B", "grade": 5}]
        assert sort_students(students, "grade", "asc")[0]["name"] == "B"

    def test_sort_students_grade_desc(self):
        students = [{"name": "A", "grade": 10}, {"name": "B", "grade": 5}]
        assert sort_students(students, "grade", "desc")[0]["name"] == "A"

    def test_sort_students_name_asc(self):
        students = [{"name": "B"}, {"name": "A"}]
        assert sort_students(students, "name", "asc")[0]["name"] == "A"

    def test_sort_students_age_asc(self):
        students = [{"name": "A", "age": 20}, {"name": "B", "age": 15}]
        assert sort_students(students, "age", "asc")[0]["name"] == "B"

    def test_sort_students_null(self):
        assert sort_students(None) == []

    def test_sort_students_empty(self):
        assert sort_students([]) == []

    def test_sort_students_no_mutation(self):
        students = [{"name": "B"}, {"name": "A"}]
        sort_students(students, "name", "asc")
        assert students[0]["name"] == "B"

    def test_sort_students_default_asc(self):
        students = [{"name": "B"}, {"name": "A"}]
        assert sort_students(students, "name")[0]["name"] == "A"
