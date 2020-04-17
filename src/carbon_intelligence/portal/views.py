from django.shortcuts import render
from .forms import UploadForm
from .process_csv import save_data


def upload_view(request):
    print("hello")
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            save_data(form.cleaned_data["file"])
    else:
        form = UploadForm()
    return render(request, "upload.html", {"form": form})
