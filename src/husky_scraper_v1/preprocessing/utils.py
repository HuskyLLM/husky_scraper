import requests
import json


def create_session():
    session = requests.Session()
    return session


# Step 1: Get available terms (uses a session to manage cookies)
def get_terms(session):
    try:
        terms_url = 'https://nubanner.neu.edu/StudentRegistrationSsb/ssb/classSearch/getTerms?offset=1&max=100000'
        response = session.get(terms_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching terms: {e}")
        return []


# Step 2: Get subjects for each term
def get_subjects(session, term_code):
    try:
        subjects_url = f'https://nubanner.neu.edu/StudentRegistrationSsb/ssb/classSearch/get_subject?term={term_code}&offset=1&max=100000'
        response = session.get(subjects_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching subjects for term {term_code}: {e}")
        return []


# Step 3: Declare term (this will use the session to pass cookies automatically)
def declare_term(session, term_code):
    try:
        declare_term_url = 'https://nubanner.neu.edu/StudentRegistrationSsb/ssb/term/search'
        response = session.post(declare_term_url, data={'term': term_code})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error declaring term {term_code}: {e}")


# Step 1: Get catalog details
def get_catalog_details(session, term_code, course_reference_number):
    try:
        url = 'https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/getSectionCatalogDetails'
        print(f"Fetching catalog details for course {course_reference_number} in term {term_code}")
        response = session.post(url, data={'term': term_code, 'courseReferenceNumber': course_reference_number})
        response.raise_for_status()
        return response.text  # HTML response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching catalog details for {course_reference_number}: {e}")
        return None


# Step 2: Get prerequisites
def get_prerequisites(session, term_code, course_reference_number):
    try:
        url = 'https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/getSectionPrerequisites'
        print(f"Fetching prerequisites for course {course_reference_number} in term {term_code}")
        response = session.post(url, data={'term': term_code, 'courseReferenceNumber': course_reference_number})
        response.raise_for_status()

        # Check if the response is JSON or string
        try:
            return response.json()  # Returns JSON if there are prerequisites
        except json.JSONDecodeError:
            return "No prerequisites"  # Returns this message if there are no prerequisites
    except requests.exceptions.RequestException as e:
        print(f"Error fetching prerequisites for {course_reference_number}: {e}")
        return None


# Step 3: Get co-requisites
def get_corequisites(session, term_code, course_reference_number):
    try:
        url = 'https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/getCorequisites'
        print(f"Fetching co-requisites for course {course_reference_number} in term {term_code}")
        response = session.post(url, data={'term': term_code, 'courseReferenceNumber': course_reference_number})
        response.raise_for_status()

        # Check if the response is JSON or string
        try:
            return response.json()  # Returns JSON if there are co-requisites
        except json.JSONDecodeError:
            return "No co-requisites"  # Returns this message if there are no co-requisites
    except requests.exceptions.RequestException as e:
        print(f"Error fetching co-requisites for {course_reference_number}: {e}")
        return None


# Step 4: Get course description
def get_course_description(session, term_code, course_reference_number):
    try:
        url = 'https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/getCourseDescription'
        print(f"Fetching description for course {course_reference_number} in term {term_code}")
        response = session.post(url, data={'term': term_code, 'courseReferenceNumber': course_reference_number})
        response.raise_for_status()
        return response.text  # HTML response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching course description for {course_reference_number}: {e}")
        return None


# Step 5: Get all course details and prerequisites for all courses in a term and subject
def get_courses(session, term_code, subject_code):
    courses = []
    print(f"Fetching courses for subject {subject_code} in term {term_code}")
    try:
        courses_url = 'https://nubanner.neu.edu/StudentRegistrationSsb/ssb/searchResults/searchResults'
        params = {
            'txt_subject': subject_code,
            'txt_term': term_code,
            'startDatepicker': '',
            'endDatepicker': '',
            'pageOffset': 0,
            'pageMaxSize': 100,
            'sortColumn': 'subjectDescription',
            'sortDirection': 'asc'
        }
        response = session.get(courses_url, params=params)
        response.raise_for_status()
        courses_data = response.json()
        if 'data' in courses_data:
            for course in courses_data['data']:
                # Extract basic course information
                course_reference_number = course.get('courseReferenceNumber', 'N/A')
                course_title = course.get('courseTitle', 'N/A')
                course_number = course.get('courseNumber', 'N/A')
                subject = course.get('subject', 'N/A')
                term_desc = course.get('termDesc', 'N/A')

                # Extract meeting times (list of dictionaries)
                meeting_times = course.get('meetingsFaculty', [])
                # Initialize variables
                faculty = []
                campus = 'N/A'
                campus_description = 'N/A'
                meeting_schedule_type = 'N/A'
                meeting_type_description = 'N/A'
                start_date = 'N/A'
                end_date = 'N/A'
                # Initialize days of the week
                days = {
                    'monday': False,
                    'tuesday': False,
                    'wednesday': False,
                    'thursday': False,
                    'friday': False,
                    'saturday': False,
                    'sunday': False
                }

                # Loop through meeting times to extract required data
                for meeting in meeting_times:
                    # Extract faculty information
                    faculty_data = meeting.get('instructor', {})
                    if faculty_data:
                        faculty_name = faculty_data.get('displayName', 'N/A')
                        faculty_email = faculty_data.get('emailAddress', 'N/A')
                        faculty.append({'name': faculty_name, 'email': faculty_email})

                    # Extract campus information
                    campus = meeting.get('campus', 'N/A')
                    campus_description = meeting.get('campusDescription', 'N/A')

                    # Extract meeting schedule type and description
                    meeting_schedule_type = meeting.get('meetingScheduleType', 'N/A')
                    meeting_type_description = meeting.get('meetingTypeDescription', 'N/A')

                    # Extract start and end dates
                    start_date = meeting.get('startDate', 'N/A')
                    end_date = meeting.get('endDate', 'N/A')

                    # Extract days of the week
                    days['monday'] = meeting.get('monday', False)
                    days['tuesday'] = meeting.get('tuesday', False)
                    days['wednesday'] = meeting.get('wednesday', False)
                    days['thursday'] = meeting.get('thursday', False)
                    days['friday'] = meeting.get('friday', False)
                    days['saturday'] = meeting.get('saturday', False)
                    days['sunday'] = meeting.get('sunday', False)

                # Get other course details
                catalog_details = get_catalog_details(session, term_code, course_reference_number)
                prerequisites = get_prerequisites(session, term_code, course_reference_number)
                co_requisites = get_corequisites(session, term_code, course_reference_number)
                description = get_course_description(session, term_code, course_reference_number)

                # Append course data
                courses.append({
                    'Course Title': course_title,
                    'Course Number': course_number,
                    'Subject': subject,
                    'Term Description': term_desc,
                    'Faculty': faculty,
                    'Campus': campus,
                    'Campus Description': campus_description,
                    'Meeting Schedule Type': meeting_schedule_type,
                    'Meeting Type Description': meeting_type_description,
                    'Start Date': start_date,
                    'End Date': end_date,
                    'Days': days,
                    'Catalog Details': catalog_details,
                    'Prerequisites': prerequisites,
                    'Co-requisites': co_requisites,
                    'Description': description,
                    'Term': term_code
                })
                print(f"Added course {course_title} ({course_number})")
        else:
            print(f"No courses found for subject {subject_code} in term {term_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching courses for subject {subject_code}: {e}")

    return courses