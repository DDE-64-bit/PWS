from django.shortcuts import render
from .models import NFCTag

def home(request):
    tags = NFCTag.objects.all()
    return render(request, 'core/home.html', {'tags': tags})


from django.shortcuts import render, get_object_or_404, redirect
from .models import NFCTag
from .forms import BalanceForm

def adjust_balance(request):
    if request.method == 'POST':
        # Zoek naar de naam die is opgegeven
        name = request.POST.get('name', '').strip()
        
        if name:
            # Probeer de NFC-tag te vinden
            tag = get_object_or_404(NFCTag, name__iexact=name)
            form = BalanceForm(request.POST, instance=tag)
            
            if form.is_valid():
                form.save()
                return redirect('adjust_balance')
        else:
            form = BalanceForm()
        
    else:
        form = BalanceForm()
    return render(request, 'adjust_balance.html', {'form': form})
