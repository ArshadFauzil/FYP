import os

PROJECT_ID = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
c = os.getenv('API_CONTENT_TYPE')

print(PROJECT_ID)
print(c)

