from aiohttp import web
from .config import web_routes
from .jinjapage import jinjapage, get_location
from .dblock import dblock


@web_routes.get("/course")
async def view_list_courses(request):
    with dblock() as db:

        db.execute("""
        SELECT * FROM course
        where cn in (
            select max(cn) from course
            group by no
        );
        """)

        items = list(db)

    return jinjapage('course_list.html',
                     location=get_location(request),
                     items=items)


@web_routes.get("/course/view_course/{no}")
def view_course(request):
    no = request.match_info.get("no")
    if no is None :
        return web.HTTPBadRequest(text="cou_sn, must be required")

    with dblock() as db:

        db.execute("""
        SELECT * FROM course
        where (
            no = %(no)s
            );
        """,dict(no=no))

        items = list(db)
        

    return jinjapage('course_view.html',
                     location=get_location(request),
                     items=items)


@web_routes.get("/course/view_course_grade/{cn}")
def view_course_grade(request):
    cn = request.match_info.get("cn")
    if cn is None :
        return web.HTTPBadRequest(text="cou_sn, must be required")

    with dblock() as db:

        db.execute("""
        SELECT g.stu_sn, g.cou_sn,s.no,c.no as cno,
            s.name as stu_name, 
            c.name as cou_name, 
            g.grade ,c.semester
        FROM student as s,course as c,course_grade as g 
        WHERE (  cou_sn = %(cn)s
        and  g.stu_sn = s.sn 
        and  g.cou_sn = c.cn
        )
        """,dict(cn=cn))

        items = list(db)
        

    return jinjapage('course_view_grade.html',
                     location=get_location(request),
                     items=items)


                