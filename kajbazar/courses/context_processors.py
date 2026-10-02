from .models import Category

def categories_processor(request):
    """
    Context processor to make categories available to all templates
    """
    return {
        'categories': Category.objects.all()
    }
