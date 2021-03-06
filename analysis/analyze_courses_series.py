#!/usr/bin/env python

import sys
import csv
import glob
import os
import re


def semester_stats(courses):
    courses_per_semester = {}
    for c in courses.keys():
        m = re.match("[LM]-A[1-4]-S[1-2]-[^-]+-[^-]+", c)
        if m:
            k1 = re.match("[LM]-A[1-4]-S[1-2]", c)[0]
            k2 = re.split("-", c)[4]
            k = k1+"-"+k2
            if not k in courses_per_semester.keys():
                courses_per_semester[k] = {}
            courses_per_semester[k][courses[c]["name"]] = courses[c]

    print("\"semestru\",\"bun\",\"bun_prof\",\"bun_num\",\"bun_proc\",\"bun_eval\",\"dif\",\"slab\",\"slab_prof\",\"slab_num\",\"slab_proc\",\"slab_eval\"")
    for k in courses_per_semester.keys():
        this_courses = courses_per_semester[k]
        if (len(this_courses)) < 2:
            continue
        best = this_courses[sorted(this_courses, key=lambda x: this_courses[x]["course_grade"], reverse=True)[0]]
        worst = this_courses[sorted(this_courses, key=lambda x: this_courses[x]["course_grade"], reverse=False)[0]]
        print("\"{}\",\"{}\",\"{}\",\"{:d}\",\"{:4.2f}\",\"{:3.2f}\",\"{:3.2f}\",\"{}\",\"{}\",\"{:d}\",\"{:4.2f}\",\"{:3.2f}\"".format(k, best["name"], best["prof"], best["nfeedback"], best["perc"], best["course_grade"], best["course_grade"]-worst["course_grade"], worst["name"], worst["prof"], worst["nfeedback"], worst["perc"], worst["course_grade"]))


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <course-feedback-csv-file>\n".format(sys.argv[0]))
        sys.exit(1)

    courses = {}
    csvfile = open(sys.argv[1], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    # Skip header.
    h = next(reader)
    for row in reader:
        courses[row[0]] = {
                "name": row[0],
                "prof": row[1],
                "nfeedback": int(row[2]),
                "perc": float(row[3]),
                "users": int(row[4]),
                "course_grade": float(row[5]),
                }
    csvfile.close()

    semester_stats(courses)

if __name__ == "__main__":
    sys.exit(main())
