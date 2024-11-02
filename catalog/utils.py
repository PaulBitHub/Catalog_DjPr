def upload_to(instance, filename):
    """
    Generate a file upload path based on the model type.
    """
    return f"{instance.__class__.__name__.lower()}/{filename}"