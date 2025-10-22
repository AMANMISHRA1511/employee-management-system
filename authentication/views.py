import random
import string
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST ,require_GET
from .forms import CustomUserCreationForm, CustomAuthenticationForm, TwoFactorForm, ForgotPasswordForm
from .models import TwoFactorCode, User

def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        # Check if user has 2FA enabled
        user = form.get_user()
        if user.two_factor_enabled:
            # Generate and save 2FA code
            code = generate_verification_code()
            expires_at = timezone.now() + timedelta(minutes=10)
            
            TwoFactorCode.objects.create(
                user=user,
                code=code,
                expires_at=expires_at
            )
            
            # Store user ID in session for 2FA verification
            self.request.session['2fa_user_id'] = user.id
            self.request.session['2fa_method'] = user.two_factor_method
            
            # In a real app, send the code via email/SMS/authenticator
            print(f"2FA code for {user.email}: {code}")
            
            return redirect('two_factor')
        else:
            # Normal login process
            return super().form_valid(form)

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'authentication/signup.html', {'form': form})

def two_factor_view(request):
    user_id = request.session.get('2fa_user_id')
    if not user_id:
        return redirect('login')
    
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            
            # Check if code is valid
            try:
                two_factor_code = TwoFactorCode.objects.get(
                    user=user,
                    code=code,
                    is_used=False
                )
                
                if two_factor_code.is_valid:
                    # Mark code as used
                    two_factor_code.is_used = True
                    two_factor_code.save()
                    
                    # Log in the user
                    login(request, user)
                    
                    # Clear 2FA session data
                    del request.session['2fa_user_id']
                    if '2fa_method' in request.session:
                        del request.session['2fa_method']
                    
                    messages.success(request, 'Login successful!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Verification code has expired. Please request a new one.')
            except TwoFactorCode.DoesNotExist:
                messages.error(request, 'Invalid verification code. Please try again.')
    else:
        form = TwoFactorForm()
    
    return render(request, 'authentication/two_factor.html', {
        'form': form,
        'user': user,
        'method': request.session.get('2fa_method', 'email')
    })

def resend_code_view(request):
    user_id = request.session.get('2fa_user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Session expired'})
    
    user = User.objects.get(id=user_id)
    
    # Generate new code
    code = generate_verification_code()
    expires_at = timezone.now() + timedelta(minutes=10)
    
    TwoFactorCode.objects.create(
        user=user,
        code=code,
        expires_at=expires_at
    )
    
    # In a real app, send the code via email/SMS/authenticator
    print(f"New 2FA code for {user.email}: {code}")
    
    return JsonResponse({'success': True, 'message': 'Code sent successfully'})

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            
            # In a real app, send password reset email
            print(f"Password reset link sent to {email}")
            
            messages.success(request, f'Password reset link sent to {email}. Please check your inbox.')
            return redirect('login')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'authentication/forgot_password.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'authentication/profile.html', {'user': request.user})

@login_required
@require_POST
def toggle_2fa_view(request):
    user = request.user
    user.two_factor_enabled = not user.two_factor_enabled
    user.save()
    
    return JsonResponse({
        'success': True,
        'enabled': user.two_factor_enabled
    })

@require_GET  # Allow only GET requests (so clicking a link works)
def logout_view(request):
    logout(request)
    return redirect('/auth/login/')