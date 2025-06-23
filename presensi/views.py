from django.shortcuts import redirect, render
from django.contrib.auth import logout as logout_auth
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta
import json
import xlsxwriter # type: ignore
from io import BytesIO
from .models import AbstractUser, Kelas, MataPelajaran, Presensi

def home(request):
    if request.user.is_authenticated:
        if request.user.abstract_user.role == 'guru':
            guru = request.user.abstract_user
            context = {
                'guru': guru,
                'total_kelas': Kelas.objects.filter(mata_pelajaran__guru=guru).distinct().count(),
                'total_presensi': Presensi.objects.filter(guru=guru).count(),
            }
            return render(request, 'templates/guru/index.html', context)
        else:
            # Redirect non-teacher users to login
            messages.error(request, 'Akses dibatasi hanya untuk guru')
            return redirect('login')
    else:
        return redirect('login')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        error_message = 'Invalid username or password'
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user is a teacher
            if user.abstract_user.role == 'guru':
                auth_login(request, user)  
                messages.success(request, 'Login Berhasil')
                return redirect('home')
            else:
                messages.error(request, 'Akses dibatasi hanya untuk guru')
                return redirect('login')
        else:
            messages.error(request, 'Username atau password salah')  
            return redirect('login') 
    return render(request, 'templates/auth/login.html')

def logout(request):
    logout_auth(request)
    return redirect('login')


@login_required
def presensi_guru(request):
    if request.user.abstract_user.role != 'guru':
        return redirect('home')
    
    # Get mata pelajaran for the logged-in guru
    mapel_list = MataPelajaran.objects.filter(guru=request.user.abstract_user)
    kelas_list = Kelas.objects.filter(mata_pelajaran__in=mapel_list).distinct()
    
    context = {
        'mapel_list': mapel_list,
        'kelas_list': kelas_list,
        'today': datetime.now().strftime('%Y-%m-%d'),
    }
    return render(request, 'templates/guru/presensi.html', context)

@login_required
def get_siswa_kelas(request):
    if request.method == 'GET':
        kelas_id = request.GET.get('kelas_id')
        mapel_id = request.GET.get('mapel_id')
        tanggal = request.GET.get('tanggal')
        
        try:
            kelas = Kelas.objects.get(id=kelas_id)
            mapel = MataPelajaran.objects.get(id=mapel_id)
            
            # Get all students in the class with role 'siswa'
            siswa_list = kelas.siswa.filter(role='siswa')
            
            # Get existing attendance for the selected date
            existing_presensi = Presensi.objects.filter(
                kelas=kelas,
                mata_pelajaran=mapel,
                tanggal=tanggal
            ).values_list('user_id', 'status')
            
            # Create a dict of existing attendance
            attendance_dict = {str(user_id): status for user_id, status in existing_presensi}
            
            # Format student data
            students_data = []
            for siswa in siswa_list:
                students_data.append({
                    'id': siswa.id,
                    'name': f"{siswa.first_name} {siswa.last_name}",
                    'status': attendance_dict.get(str(siswa.id))
                })
            
            return JsonResponse({'students': students_data})
        except (Kelas.DoesNotExist, MataPelajaran.DoesNotExist) as e:
            return JsonResponse({'error': str(e)}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def submit_presensi(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            kelas_id = data.get('kelas_id')
            mapel_id = data.get('mapel_id')
            tanggal = datetime.now().date()
            presensi_data = data.get('presensi_data')
            
            kelas = Kelas.objects.get(id=kelas_id)
            mapel = MataPelajaran.objects.get(id=mapel_id)
            current_time = datetime.now().time()
            
            # Delete existing attendance records for this class, subject and date
            Presensi.objects.filter(
                kelas=kelas,
                mata_pelajaran=mapel,
                tanggal=tanggal
            ).delete()
            
            # Create new attendance records
            for data in presensi_data:
                student = AbstractUser.objects.get(id=data['student_id'])
                Presensi.objects.create(
                    user=student,
                    kelas=kelas,
                    mata_pelajaran=mapel,
                    tanggal=tanggal,
                    jam_masuk=current_time,
                    guru=request.user.abstract_user,
                    status=data['status'],
                    keterangan=data.get('keterangan', '')
                )
            
            return JsonResponse({'message': 'Presensi berhasil disimpan'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_date_range(period_type, year=None, month=None, week=None, semester=None):
    today = datetime.now().date()
    
    if period_type == 'week':
        # Get start of week (Monday)
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif period_type == 'month':
        # Get start and end of month
        start_date = today.replace(day=1)
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
    elif period_type == 'semester':
        # Semester 1: July - December, Semester 2: January - June
        current_year = today.year
        if semester == '1':
            start_date = datetime(current_year, 7, 1).date()
            end_date = datetime(current_year, 12, 31).date()
        else:
            start_date = datetime(current_year, 1, 1).date()
            end_date = datetime(current_year, 6, 30).date()
    else:
        start_date = today
        end_date = today
    
    return start_date, end_date

@login_required
def export_presensi(request):
    if request.user.abstract_user.role != 'guru':
        return redirect('home')
        
    kelas_id = request.GET.get('kelas_id')
    mapel_id = request.GET.get('mapel_id')
    period_type = request.GET.get('period', 'week')  # week, month, semester
    semester = request.GET.get('semester')  # 1 or 2
    
    try:
        kelas = Kelas.objects.get(id=kelas_id)
        mapel = MataPelajaran.objects.get(id=mapel_id)
        
        start_date, end_date = get_date_range(period_type, semester=semester)
        
        # Get all students in the class
        students = kelas.siswa.filter(role='siswa')
        
        # Get attendance records for the period
        presensi_records = Presensi.objects.filter(
            kelas=kelas,
            mata_pelajaran=mapel,
            tanggal__range=[start_date, end_date]
        ).order_by('tanggal', 'user')
        
        # Create Excel file
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Add headers
        headers = ['No', 'Nama Siswa', 'Tanggal', 'Status', 'Jam Masuk', 'Keterangan']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
        
        # Add data
        row = 1
        for record in presensi_records:
            worksheet.write(row, 0, row)
            worksheet.write(row, 1, f"{record.user.first_name} {record.user.last_name}")
            worksheet.write(row, 2, record.tanggal.strftime('%Y-%m-%d'))
            worksheet.write(row, 3, record.get_status_display())
            worksheet.write(row, 4, record.jam_masuk.strftime('%H:%M'))
            worksheet.write(row, 5, record.keterangan or '')
            row += 1
        
        workbook.close()
        
        # Create response
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=presensi_{kelas.nama}_{mapel.nama}_{start_date}_{end_date}.xlsx'
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def get_presensi_period(request):
    if request.method == 'GET':
        kelas_id = request.GET.get('kelas_id')
        mapel_id = request.GET.get('mapel_id')
        period_type = request.GET.get('period', 'week')
        semester = request.GET.get('semester')
        
        try:
            kelas = Kelas.objects.get(id=kelas_id)
            mapel = MataPelajaran.objects.get(id=mapel_id)
            
            start_date, end_date = get_date_range(period_type, semester=semester)
            
            # Get attendance records for the period
            presensi_records = Presensi.objects.filter(
                kelas=kelas,
                mata_pelajaran=mapel,
                tanggal__range=[start_date, end_date]
            ).select_related('user').order_by('tanggal', 'user')
            
            # Format data for response
            data = []
            for record in presensi_records:
                data.append({
                    'id': record.id,
                    'student_name': f"{record.user.first_name} {record.user.last_name}",
                    'date': record.tanggal.strftime('%Y-%m-%d'),
                    'status': record.status,
                    'time': record.jam_masuk.strftime('%H:%M'),
                    'notes': record.keterangan or ''
                })
            
            return JsonResponse({
                'data': data,
                'period': {
                    'start': start_date.strftime('%Y-%m-%d'),
                    'end': end_date.strftime('%Y-%m-%d')
                }
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def rekap_presensi(request):
    if request.user.abstract_user.role != 'guru':
        return redirect('home')
    
    # Get mata pelajaran for the logged-in guru
    mapel_list = MataPelajaran.objects.filter(guru=request.user.abstract_user)
    kelas_list = Kelas.objects.filter(mata_pelajaran__in=mapel_list).distinct()
    
    context = {
        'mapel_list': mapel_list,
        'kelas_list': kelas_list,
    }
    return render(request, 'templates/guru/rekap.html', context) 


