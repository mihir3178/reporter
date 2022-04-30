
import csv
from io import StringIO
from django.shortcuts import render
from custom_exception import CustomException
import magic
from report_app.models import ReportData
from django.contrib.auth.decorators import login_required

@login_required
def upload_data(request):
    """ This function is responsible for Uploading data through csv file"""
    user = request.user
    data_list = ReportData.objects.filter(user_id=user.id)
    try:
        if request.method == "POST":
            if request.FILES:
                file_data = request.FILES["file"].read()
                mime = magic.Magic(mime=True)
                if mime.from_buffer(file_data) == "application/csv":
                    file_data = file_data.decode("utf-8")
                    output = list(csv.reader(StringIO(file_data)))
                    column = output[0]
                    data_lines = output[1:]
                    if column == ['name','age'] and all(
                        [len(i) == 2 for i in data_lines]
                    ):
                        for data in data_lines:
                            try:
                                name = str(data[0])
                                age = str(data[1])
                                try:
                                    ReportData.objects.get(name=name, age=age)
                                except ReportData.DoesNotExist:
                                    rep = ReportData.objects.create(name=name, age=age)
                                    rep.user_id = user.id
                                    rep.save()
                            except:
                                raise CustomException(
                                    description="Some data in csv file are in invalid format or some data already exist.",
                                    status_code=400,
                                )
                    else:
                        raise CustomException(
                            description="Invalid format of the csv file",
                            status_code=412,
                        )
                else:
                    raise CustomException(
                        description="Only csv file are allowded", status_code=412
                    )
            else:
                raise CustomException(description="No file provided", status_code=412)
            
            return render(request, 'view_report.html', context={'data': data_list, 'error': '0'})
        else:
            raise CustomException(description="Invalid method", status_code=400)
    except CustomException as e:
        return render(request, 'view_report.html', context={'data': data_list, 'upload_error_msg': e.description}, status=e.status_code)
    except Exception as e:
        return render(request, 'view_report.html', context={'data': data_list, 'upload_error_msg': "unable to upload data"}, status=500)


@login_required
def view_uploaded_data(request):
    """ This function is responsible for filtering data from table"""
    user = request.user
    name = request.GET.get("name")
    age = request.GET.get("age")
    data_list = ReportData.objects.filter(user_id=user.id)
    if name:
        data_list = data_list.filter(name=name)
    if age:
        data_list = data_list.filter(age=age)
    return render(request, 'view_report.html', context={'data': data_list})
        
            



@login_required
def delete_data(request):
    """ This function is responsible for deleting data from table"""
    user = request.user
    data_list = ReportData.objects.filter(user_id=user.id)
    try:
        if request.method == "POST":
            user = request.user
            name = request.POST.get("name")
            age = request.POST.get("age")
            # data uploaded by login user
            data = ReportData.objects.filter(user_id=user.id)
            if name:
                data.filter(name=name).delete()
            if age:
                data.filter(age=age).delete()
            return render(request, 'view_report.html', context={'data': data_list})
        else:
            raise CustomException(description="Invalid method", status_code=400)
    except CustomException as e:
        return render(request, 'view_report.html', context={'data': data_list, 'delete_error_msg': e.description})
    except Exception as e:
        return render(request, 'view_report.html', context={'data': data_list, 'delete_error_msg': "unable to delete data"})
