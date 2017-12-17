CREATE DATABASE istudy
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE istudy;
DROP TABLE IF EXISTS student CASCADE;
DROP TABLE IF EXISTS teacher CASCADE;
DROP TABLE IF EXISTS take_course CASCADE;
DROP TABLE IF EXISTS question CASCADE;
DROP TABLE IF EXISTS paper CASCADE;
DROP TABLE IF EXISTS notes CASCADE;

CREATE TABLE student (
  student_uid    INTEGER AUTO_INCREMENT NOT NULL COMMENT '学生学号，唯一编号',
  student_email  VARCHAR(100)           NOT NULL COMMENT '学生邮箱，用于登录',
  student_name   VARCHAR(30) COMMENT '学生姓名',
  student_passwd VARCHAR(64) COMMENT 'SHA-256加密',
  PRIMARY KEY (student_uid),
  UNIQUE (student_uid)
)
  COMMENT '学生表';

CREATE TABLE teacher (
  teacher_uid    INTEGER AUTO_INCREMENT NOT NULL COMMENT '老师学号，唯一编号',
  teacher_email  VARCHAR(100)           NOT NULL COMMENT '老师邮箱，用于登录',
  teacher_name   VARCHAR(30) COMMENT '老师姓名',
  teacher_passwd VARCHAR(64) COMMENT 'SHA-256加密',
  PRIMARY KEY (teacher_uid),
  UNIQUE (teacher_uid)
)
  COMMENT '教师表';

CREATE TABLE take_course (
  student_uid        INTEGER NOT NULL,
  teacher_uid        INTEGER NOT NULL,
  usual_behave_grade DOUBLE COMMENT '平时成绩',
  master_test_grade  DOUBLE COMMENT '期末成绩',
  final_term_grade   DOUBLE COMMENT '总评成绩',
  PRIMARY KEY (student_uid, teacher_uid),
  FOREIGN KEY (student_uid) REFERENCES student (student_uid)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  FOREIGN KEY (teacher_uid) REFERENCES teacher (teacher_uid)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
  COMMENT '记录学生登记的课程';

CREATE TABLE question (
  question_id INTEGER AUTO_INCREMENT NOT NULL
  COMMENT '问题编号',
  content     VARCHAR(2000)          NOT NULL
  COMMENT '问题题目，或者说主题内容',
  answer      VARCHAR(2000) COMMENT '问题答案，主观题就空吧',
  PRIMARY KEY (question_id),
  UNIQUE (question_id)
)
  COMMENT '考试题库';

CREATE TABLE paper (
  paper_id          INTEGER AUTO_INCREMENT NOT NULL
  COMMENT '试卷编号',
  create_time       DATETIME DEFAULT now()
  COMMENT '试卷创建时间，每次添加的时候自动生成',
  last_modification DATETIME DEFAULT now() ON UPDATE now()
  COMMENT '试卷最后修订时间，自动更新',
  PRIMARY KEY (paper_id),
  UNIQUE (paper_id)
)
  COMMENT '出题试卷';

CREATE TABLE question__paper (
  question_id INTEGER NOT NULL,
  paper_id    INTEGER NOT NULL,
  ind         INTEGER NOT NULL,
  PRIMARY KEY (question_id, paper_id),
  FOREIGN KEY (question_id) REFERENCES question (question_id),
  FOREIGN KEY (paper_id) REFERENCES paper (paper_id)
)
  COMMENT '将试卷和试题关联';
CREATE TABLE notes (
  student_uid INTEGER AUTO_INCREMENT NOT NULL,
  note        VARCHAR(10000),
  PRIMARY KEY (student_uid),
  FOREIGN KEY (student_uid) REFERENCES student (student_uid)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


UPDATE student
SET student_passwd = #{student_passwd}
WHERE student_uid = #{student_uid};
UPDATE teacher
SET teacher_passwd = #{student_passwd}
WHERE teacher_uid = #{student_uid};
UPDATE student
SET student_email = #{student_email}
WHERE student_uid = #{student_uid};
UPDATE teacher
SET teacher_email = #{teacher_email}
WHERE teacher_uid = #{teacher_uid};

DELETE FROM student
WHERE student_uid = #{student_uid};
DELETE FROM teacher
WHERE teacher_uid = #{teacher_uid};

DELETE FROM take_course
WHERE student_uid = #{student_uid} AND teacher_uid = #{teacher_uid};





