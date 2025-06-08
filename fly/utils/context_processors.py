def menu_processor(request):
    return {
        'active_menu': request.path  # 或更复杂的逻辑判断
    }