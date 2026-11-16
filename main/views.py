from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, JobPostForm, ApplicationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from .models import JobPost
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import JobPost, Application

@login_required(login_url="/login")
def home(request):
    posts = JobPost.objects.all()
    can_delete_other_posts = request.user.groups.filter(name='HR').exists()  # Check if the user is in the HR group
    is_applicant = request.user.groups.filter(name='Applicant').exists()
    is_hr_user = request.user.groups.filter(name='HR').exists()
    # Check if the user has permission to add or change job posts
    can_add_job_post = request.user.has_perm('main.add_jobpost')
    can_apply_job = request.user.has_perm('main.apply_job')  # Adjust if needed
    can_change_job_post = request.user.has_perm('main.change_jobpost')

    return render(request, 'main/home.html', {
        'posts': posts,
        'can_add_job_post': can_add_job_post,
        'can_apply_job': can_apply_job,
        'can_change_job_post': can_change_job_post,
        'can_delete_other_posts': can_delete_other_posts, 
        'is_applicant': is_applicant,
        'is_hr_user': is_hr_user,
    })

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            
            # Add the user to the "Applicant" group
            applicant_group = Group.objects.get(name='Applicant')
            user.groups.add(applicant_group)
            
            login(request, user)  # Log the user in
            messages.success(request, 'Your account has been created successfully!')
            return redirect('/login')  # Redirect to the login page
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {'form': form})

@login_required(login_url="/login")
@permission_required('main.add_jobpost', raise_exception=True)
def create_job_post(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)  # Don't save to the database yet
            job_post.author = request.user  # Assign the current user as the author
            job_post.save()  # Now save to the database
            messages.success(request, 'Job post created successfully!')
            return redirect('home')  # Redirect to a success page or elsewhere
    else:
        form = JobPostForm()
    return render(request, 'main/create_job_post.html', {'form': form})

@login_required(login_url="/login")
def apply_job(request, post_id):
    job_post = get_object_or_404(JobPost, id=post_id)

    # Check if the user is in the "Applicant" group
    if not request.user.groups.filter(name='Applicant').exists():
        messages.error(request, 'You do not have permission to apply for this job.')
        return redirect('home')  # Redirect to home or a suitable page

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)  # Handle file upload
        if form.is_valid():
            application = form.save(commit=False)
            application.job_post = job_post
            application.applicant = request.user  # Associate with the logged-in user
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('home')  # Redirect to home or a success page
    else:
        form = ApplicationForm()

    return render(request, 'main/apply_job.html', {'job_post': job_post, 'form': form})


@login_required(login_url="/login")
def delete_job_post(request, post_id):
    job_post = get_object_or_404(JobPost, id=post_id)

    # Check if the user is in the HR group or has permission to delete job posts
    if request.user.groups.filter(name='HR').exists() or request.user.has_perm('main.delete_jobpost'):
        job_post.delete()
        messages.success(request, 'Job post deleted successfully!')
    else:
        messages.error(request, 'You do not have permission to delete this job post.')

    return redirect('home')  # Redirect to the home page after deletion

@login_required
def edit_job_post(request, post_id):
    post = get_object_or_404(JobPost, id=post_id)

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page after saving
    else:
        form = JobPostForm(instance=post)

    return render(request, 'main/edit_job_post.html', {'form': form, 'post': post})

@login_required(login_url="/login")
def hr_dashboard(request):
    # Check if the user is in the HR group
    if request.user.groups.filter(name='HR').exists():
        applications = Application.objects.select_related('job_post', 'applicant').all()  # Fetch all applications with related job posts and applicants
        return render(request, 'main/hr_dashboard.html', {'applications': applications})
    else:
        return render(request, 'main/access_denied.html')  # Access denied if not in HR group
    

@login_required(login_url="/login")
def view_applicants(request, post_id):
    job_post = get_object_or_404(JobPost, id=post_id)
    
    # Filter applications by the specific job post
    applications = Application.objects.select_related('job_post', 'applicant').filter(job_post=job_post)
    
    # Check if the user is in the HR group
    if request.user.groups.filter(name='HR').exists():
        return render(request, 'main/view_applicants.html', {
            'job_post': job_post,
            'applications': applications,
        })
    else:
        return render(request, 'main/access_denied.html')  # Render an access denied page if not in HR


@login_required(login_url="/login")
def generate_analysis_report(request, post_id):
    # For now, just render a simple page with "Hello"
    return render(request, 'main/report.html', {
        'post_id': post_id,  # You can pass the post_id if needed later
    })