from django.shortcuts import render
from .forms import UploadForm
from .process_csv import save_data


def upload(request):
    error = ""
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                save_data(form.cleaned_data["file"])
            except Exception as e:
                error = e
                print(e)
    else:
        form = UploadForm()
    return render(request, "upload.html", {"error": error, "form": form})
