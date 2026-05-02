from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from cryptography.fernet import Fernet
from .models import SecureData, UserProfile, AuditLog
from .forms import ProfileUpdateForm
import hashlib


# Fixed Key
def get_key():
    return b'7fL-S4FAfVigVbJ09kfCcXuCV5LRrAsZHqcJ0oPt2sE='


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'profile.html', {'form': form})


@login_required
def audit_logs_view(request):
    logs = AuditLog.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'audit_logs.html', {'logs': logs})


@login_required
def home(request):
    msg, decrypted_msg = "", ""

    try:
        records = SecureData.objects.all().order_by('-id')
    except Exception as e:
        print(f"Database Error: {e}")
        records = []

    if request.method == "POST":
        try:
            cipher = Fernet(get_key())

            # --- ENCRYPTION LOGIC ---
            if "data_name" in request.POST and "content" in request.POST:
                name = request.POST.get("data_name")
                text = request.POST.get("content")
                if name and text:
                    token = cipher.encrypt(text.encode('utf-8'))
                    h = hashlib.sha256(text.encode('utf-8')).hexdigest()
                    SecureData.objects.create(
                        data_name=name,
                        encrypted_content=token.decode('utf-8'),
                        integrity_hash=h
                    )
                    AuditLog.objects.create(user=request.user, action=f"Encrypted data: {name}")
                    return redirect('home')

            # --- DECRYPTION LOGIC (FIXED) ---
            elif "decrypt_id" in request.POST:
                record = get_object_or_404(SecureData, id=request.POST.get("decrypt_id"))

                # Fetch encrypted content
                enc_data = record.encrypted_content

                # FIX: PostgreSQL memoryview error handling
                if isinstance(enc_data, memoryview):
                    enc_data = enc_data.tobytes()
                elif isinstance(enc_data, str):
                    enc_data = enc_data.encode('utf-8')

                # Decrypting
                dec_text = cipher.decrypt(enc_data).decode('utf-8')
                decrypted_msg = f"Secret for {record.data_name}: {dec_text}"
                AuditLog.objects.create(user=request.user, action=f"Decrypted data: {record.data_name}")

        except Exception as e:
            # Error message for UI
            msg = f"Security Error: {str(e)}"

    return render(request, "index.html", {"msg": msg, "decrypted_msg": decrypted_msg, "records": records})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
