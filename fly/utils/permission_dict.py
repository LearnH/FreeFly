def get_model_permission(model):
    meta = model._meta
    return {
        'add': f"{meta.app_label}.add_{meta.model_name}",
        'change': f"{meta.app_label}.change_{meta.model_name}",
        'delete': f"{meta.app_label}.delete_{meta.model_name}",
        'view': f"{meta.app_label}.view_{meta.model_name}",
    }