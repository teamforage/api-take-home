# This file contains stubbed calls to a mock processor upstream of Forage.

# Forage acts as an intermediary between merchants and EBT processors
# which differ by state.

from random import uniform

from django.utils import timezone

from api.models import Payment

# 95% would be a terrible uptime for a payments app!  
def false_5_percent():
    return uniform(0, 1) > 0.05


def random_error():
    one_half_chance = uniform(0, 2)
    if one_half_chance > 1:
        return "Suspected fraud"
    else:
        return "Card network outage"
    

def processPayment(payment_obj):
    if payment_obj.status == Payment.TYPE_SUCCEEDED:
        return None # don't double process

    if false_5_percent():
        # Payment was successful
        
        payment_obj.status = Payment.TYPE_SUCCEEDED
        payment_obj.success_date = timezone.now()
        payment_obj.save()
    else:
        payment_obj.status = Payment.TYPE_FAILED

        error_message = random_error()
        payment_obj.last_processing_error = error_message

        payment_obj.save()

        return error_message

    
