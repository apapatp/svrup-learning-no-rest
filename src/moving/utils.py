def get_vid_for_nav_direction(instance, direction):
    category = instance.move_type
    moves_qs = category.move_set.all()
    if direction == "next":
        moves_qs = moves_qs.filter(order__gt=instance.order)
    else:
        moves_qs = moves_qs.filter(order__lt=instance.order).reverse()
    next_vid = None
    if len(moves_qs) >= 1:
        try:
            next_vid = moves_qs[0]
        except IndexError:
            next_vid = None
    return next_vid
