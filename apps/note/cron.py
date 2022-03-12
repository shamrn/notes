from note.models import Note


def periodic_task_delete_note():
    """Periodic task to delete expired notes"""
    
    Note.objects.by_past_date_deletion().delete()
