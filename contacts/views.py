from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        #Check if user made inquiry

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, name=name, email=email)

            if has_contacted:
                messages.error(request, 'You have already made inquiry')
                return redirect('/listings/'+listing_id)
       
        contact = Contact(listing=listing, listing_id = listing_id, name = name, email = email, phone=phone, message=message, user_id=user_id)

        contact.save()

        send_mail(
            'Property listing inquiry',
            'There had been an inquiry for ' + listing + '. Sign into admin panel to view.',
            'rhillx.code@gmail.com',
            [realtor_email, 'rhillz718@gmail.com'],
            fail_silently=False
        )

        messages.success(request, "Your request has been submitted. A realtor will get back to you at the most earliest convienence.")

        return redirect('/listings/'+listing_id)
