from django.contrib import messages

# Inspired by SuccessMessageMixin
class ErrorMessageMixin:
    """
    Add an error message on invalid form.
    """
    error_message = ''

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.error_message:
            messages.warning(self.request, self.error_message)
        return response