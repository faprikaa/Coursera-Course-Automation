import requests

def handle_video(lesson_id, course_slug, user_id, session):
    params = {
        'autoEnroll': 'false',
    }

    json_data = {
        'contentRequestBody': {},
    }
    for attempt in range(3):
        try:
            response = session.post(
                f'https://www.coursera.org/api/opencourse.v1/user/{user_id}/course/{course_slug}/item/{lesson_id}/lecture/videoEvents/ended',
                params=params, json=json_data)
            if response.status_code == 200 or response.json().get('statusCode', None) == 200:
                break
            else :
                print(f"Failed to mark video {lesson_id} as completed. Status code: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")

    return