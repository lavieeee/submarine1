from aiohttp import web
from urllib.parse import urlencode
from psycopg.errors import UniqueViolation, ForeignKeyViolation
from .config import web_routes
from .dblock import dblock

@web_routes.post('/action/class_order/add')
async def action_class_order_add(request):
    params = await request.post()
    stu_sn = params.get("stu_sn")
    class_sn = params.get("class_sn")

    if stu_sn is None or class_sn is None:
        return web.HTTPBadRequest(text="stu_sn, cou_sn, class_sn must be required")

    try:
        stu_sn = int(stu_sn)
        class_sn = int(class_sn)
    except ValueError:
        return web.HTTPBadRequest(text="invalid value")

    
    try:
        with dblock() as db:
            db.execute("""
            INSERT INTO course_selection (cs_stu_sn, co_cls) 
            VALUES ( %(stu_sn)s, %(class_sn)s)
            """, dict(stu_sn=stu_sn,class_sn=class_sn))
    except UniqueViolation:
        query = urlencode({
            "message": "已经置入该学生的该课程班次",
            "return": "/selection"
        })
        return web.HTTPFound(location=f"/error?{query}")
    except ForeignKeyViolation as ex:
        return web.HTTPBadRequest(text=f"无此学生或课程班次: {ex}")

    

    return web.HTTPFound(location="/selection")





