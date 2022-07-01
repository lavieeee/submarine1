DROP TABLE IF EXISTS student;
CREATE TABLE IF NOT EXISTS student  (
    sn       	     VARCHAR(30),  --序号
    no               VARCHAR(10),  --学号
    name             TEXT,         --姓名             
    gender           CHAR(1),      --性别          
    college          TEXT,         --学院         
    Entry_Year       INTEGER,      --入学时间          
    class_name       TEXT,         --班级            
    PRIMARY  KEY(sn)                  
);


-- 给sn创建一个自增序号
CREATE SEQUENCE seq_student_sn 
    START 10000 INCREMENT 1 OWNED BY student.sn;
ALTER TABLE student ALTER sn 
    SET DEFAULT nextval('seq_student_sn');
-- 学号唯一
CREATE UNIQUE INDEX idx_student_no ON student(no);

-- === 课程表
DROP TABLE IF EXISTS course;
CREATE TABLE IF NOT EXISTS course  (
    cn             VARCHAR(10),      --序号
    no             VARCHAR(10),      --课程号
    semester       TEXT,             --学期
    credit         INTEGER,          --学分
    class_hours    INTEGER,          --学时
    name   	       text,             --课程名
    PRIMARY KEY(cn)
);
CREATE SEQUENCE seq_course_cn 
    START 10000 INCREMENT 1 OWNED BY course.cn;
ALTER TABLE course ALTER cn 
    SET DEFAULT nextval('seq_course_cn');
CREATE UNIQUE INDEX idx_course_cn ON course(cn);




DROP TABLE IF EXISTS course_grade;
CREATE TABLE IF NOT EXISTS course_grade  (
    stu_sn VARCHAR(10),     -- 学生序号
    cou_sn VARCHAR(10),     -- 课程序号
    grade  NUMERIC(5,2),    -- 最终成绩
    PRIMARY KEY(stu_sn, cou_sn)
);

-- ===班次表
DROP TABLE IF EXISTS class_order;
CREATE TABLE IF NOT EXISTS class_order  (
    class_sn             VARCHAR(30),       --班次号，文本串
    course_cn            VARCHAR(10),  
    place                TEXT,              --地点，文本串
    time                 DATE,              --时间，日期类型
    teacher              TEXT,              --老师姓名，文本串
    PRIMARY   KEY(class_sn)           --指定class_sn字段为主键
);

CREATE SEQUENCE seq_class_order_cls 
    START 10000 INCREMENT 1 OWNED BY class_order.class_sn;
ALTER TABLE class_order ALTER class_sn 
    SET DEFAULT nextval('seq_class_order_cls');
CREATE UNIQUE INDEX idx_class_order_cls ON class_order(class_sn);


DROP TABLE IF EXISTS course_selection;
CREATE TABLE IF NOT EXISTS course_selection  (
    cs_stu_sn  VARCHAR(10),     -- 学生序号
    co_cls     VARCHAR(10),     -- 班次号
    PRIMARY KEY(cs_stu_sn, co_cls)
);



ALTER TABLE course_grade 
    ADD CONSTRAINT stu_sn_fk FOREIGN KEY (stu_sn) REFERENCES student(sn);
ALTER TABLE course_grade 
    ADD CONSTRAINT cou_sn_fk FOREIGN KEY (cou_sn) REFERENCES course(cn);


ALTER TABLE course_selection 
    ADD CONSTRAINT cs_stu_sn_fk FOREIGN KEY(cs_stu_sn) REFERENCES student(sn);
ALTER TABLE course_selection 
    ADD CONSTRAINT co_cls_fk FOREIGN KEY(co_cls) REFERENCES class_order(class_sn);
   
ALTER TABLE class_order 
    ADD CONSTRAINT course_cn_fk FOREIGN KEY(course_cn) REFERENCES course(cn);

