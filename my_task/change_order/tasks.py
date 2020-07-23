from datetime import datetime

from my_task.main import app
from order.models import Order


@app.task(name="check_order")
def check_order():
    """完成过期取消订单"""
    order_obj = Order.objects.all()
    for order in order_obj:
        if order.order_status == 1 or order.order_status == 2:
            pass
        elif order.order_status == 0:
            order.order_status = 3
            order.save()
        return "ok"
