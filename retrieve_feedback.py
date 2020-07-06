#!/usr/bin/env python3
# (c) Mihai Chiroiu 18 May 2020
# sudo pip3 install requests
# https://docs.moodle.org/dev/Web_service_API_functions

import json
import requests
import getpass

username = input('Utilizator Moodle: ') 
try:
  password = getpass.getpass(prompt='Parola Moodle: ')
except Exception as error:
  print('ERROR', error)
  exit(0)

base_url = 'https://acs.curs.pub.ro/2018/'
rest_url = base_url + '/webservice/rest/server.php'
moodle_token = ''
userid = ''

def get_auth_token():
  global moodle_token 

  token_url = base_url + 'login/token.php'
  payload = {
    "username":username,
		"password":password,
    "moodlewsrestformat":"json", 
		"service":"moodle_mobile_app"
    }

  r=requests.post(token_url, params=payload)
  res_json = r.json()
  moodle_token = res_json['token']

def get_userid():
  global moodle_token 
  global userid  
    
  payload = {
		"wstoken":moodle_token,
    "moodlewsrestformat":"json", 
		"wsfunction":"core_webservice_get_site_info"
    }
  r=requests.post(rest_url, params=payload)
  res_json = r.json()
  userid = res_json['userid']

def get_user_courses_ids():
  global moodle_token 
  global userid  

  payload = {
		"wstoken":moodle_token,
    "moodlewsrestformat":"json", 
		"wsfunction":"core_enrol_get_users_courses",
    "userid":userid
    }
  r=requests.post(rest_url, params=payload)
  res_json = r.json()
  course_ids = {}

  for course in res_json:
    course_ids[course['id']] = course['fullname']
  return course_ids

def get_user_feedback_ids():
  global moodle_token 
  global userid  

  course_ids = get_user_courses_ids()

  payload = {
		"wstoken":moodle_token,
    "moodlewsrestformat":"json", 
		"wsfunction":"mod_feedback_get_feedbacks_by_courses"
    }
  # create a json of all courses id for the user
  i = 0
  for course_id in course_ids:
    course_id_json = {"courseids["+str(i)+"]":course_id}
    i+=1
    payload.update(course_id_json)

  r=requests.post(rest_url, params=payload)
  res_json = r.json()

  # create the list of feedback ids in all the courses
  feedback_ids = {}
  for feedback in res_json['feedbacks']:
    feedback_ids[feedback['id']] = course_ids[feedback['course']]
  return feedback_ids

def get_user_feedback():
  global moodle_token 
  global userid  
  
  feedback_ids = get_user_feedback_ids()

  payload = {
		"wstoken":moodle_token,
    "moodlewsrestformat":"json", 
		"wsfunction":"mod_feedback_get_responses_analysis"
    }

  for feedback_id in feedback_ids:
    course_id_json = {"feedbackid":feedback_id}
    payload.update(course_id_json)
    r=requests.post(rest_url, params=payload)
    res_json = r.json()
    with open(feedback_ids[feedback_id]+".json", 'w') as outfile:
      json.dump(res_json, outfile)

def main():
  get_auth_token()
  get_userid()
  get_user_feedback()

if __name__ == "__main__":
  main()
