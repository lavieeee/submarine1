from aiohttp import web
from .config import web_routes
from .jinjapage import jinjapage, get_location
from .dblock import dblock


@web_routes.get("/selection")
async def view_list_classes(request):
    with dblock() as db:

        db.execute("""
        SELECT sn AS stu_sn, name as stu_name FROM student ORDER BY name
        """)
        students = list(db)

        db.execute("""
        SELECT cn AS cou_sn, name as cou_name FROM course ORDER BY name
        """)
        courses = list(db)

        db.execute("""
        SELECT co.class_sn,co.place,co.time,co.teacher,c.name
	        FROM class_order as co
		        inner join course as c on co.course_cn = c.cn 
            order by class_sn;
        """)

        items = list(db)

    return jinjapage('course_selection.html',
                     location=get_location(request),
                     students=students,
                     courses=courses,
                     items=items)


@web_routes.get("/selection/view")
def view_course_selection(request):

    with dblock() as db:

        db.execute("""
        SELECT s.no,s.name,cs.co_cls ,co.course_cn ,c.name as c_name
	        FROM course_selection as cs
		        inner join student as s on s.sn = cs.cs_stu_sn
		        inner join class_order as co on co.class_sn = cs.co_cls  
		        inner join course as c on co.course_cn = c.cn ;
        """)

        items = list(db)
        

    return jinjapage('course_selection_view.html',
                     location=get_location(request),
                     items=items)                     