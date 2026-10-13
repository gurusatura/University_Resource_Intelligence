-- PostgreSQL Schema for University Resource Intelligence System

-- 1. students
CREATE TABLE IF NOT EXISTS students (
    student_id UUID PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(50),
    address TEXT,
    program_name VARCHAR(255),
    year INT
);

-- 2. instructors
CREATE TABLE IF NOT EXISTS instructors (
    instructor_id UUID PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(50),
    department VARCHAR(255)
);

-- 3. courses
CREATE TABLE IF NOT EXISTS courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    credits INT,
    description TEXT
);

-- 4. classrooms
CREATE TABLE IF NOT EXISTS classrooms (
    classroom_id INT PRIMARY KEY,
    building_name VARCHAR(255),
    room_number INT,
    capacity INT,
    room_type VARCHAR(255)
);

-- 5. timeslots
CREATE TABLE IF NOT EXISTS timeslots (
    timeslot_id INT PRIMARY KEY,
    day VARCHAR(50),
    start_time TIME,
    end_time TIME,
    timeslot_valid BOOLEAN
);

-- 6. schedule
CREATE TABLE IF NOT EXISTS schedule (
    student_id UUID REFERENCES students(student_id),
    course_id INT REFERENCES courses(course_id),
    instructor_id UUID REFERENCES instructors(instructor_id),
    classroom_id INT REFERENCES classrooms(classroom_id),
    timeslot_id INT REFERENCES timeslots(timeslot_id),
    semester VARCHAR(50),
    academic_year INT,
    PRIMARY KEY (student_id, course_id)
);

-- 7. Indexes on schedule's FK columns (frequent filter columns for conflict/utilization)
CREATE INDEX idx_schedule_classroom_id ON schedule(classroom_id);
CREATE INDEX idx_schedule_timeslot_id ON schedule(timeslot_id);
CREATE INDEX idx_schedule_instructor_id ON schedule(instructor_id);
CREATE INDEX idx_schedule_course_id ON schedule(course_id);
