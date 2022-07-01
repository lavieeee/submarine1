from aiohttp import web

from .dblock import dblock
from .config import web_routes
from .jinjapage import get_location, jinjapage


@web_routes.get("/student")
async def view_student_list(request):
    with dblock() as db:
        db.execute("""
        SELECT sn AS stu_sn, name as stu_name FROM student ORDER BY name
        """)
        students = list(db)

        db.execute("""
        SELECT * FROM student;
        """)

        items = list(db)

    return jinjapage('student_list.html',
                     location=get_location(request),
                     students=students,
                     items=items)


@web_routes.get('/student/view_grade/{sn}')
def view_grade(request):
    sn = request.match_info.get("sn")
    if sn is None :
        return web.HTTPBadRequest(text="stu_sn, cou_sn, must be required")
    
    with dblock() as db:  

        db.execute("""
        SELECT g.stu_sn, g.cou_sn,s.no,
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade, c.semester
        FROM student as s,course as c,course_grade as g 
        WHERE (  stu_sn = %(sn)s
        and  g.stu_sn = s.sn 
        and  g.cou_sn = c.cn
        )
        """, dict(sn=sn))

        items = list(db)

    return jinjapage("view_grade.html",
                     location=get_location(request),
                     items=items,
                     sn=sn)
