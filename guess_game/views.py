from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import plivo
import random


@csrf_exempt
def index(request):
    response = plivo.Response()
    response.addSpeak(body="Hello, welcome to Plivo's "
                      "demo guessing game app!")
    response.addWait(length=2)

    action_url = '/main_menu_response/'
    absolute_action_url = request.build_absolute_uri(action_url)

    getDigits = plivo.GetDigits(action=absolute_action_url, method='POST',
                                timeout=4, numDigits=4, retries=1)
    getDigits.addSpeak(body='To play the game Press 1')
    getDigits.addWait(length=1)
    getDigits.addSpeak(body='To learn how to play Press 2')
    getDigits.addWait(length=1)
    getDigits.addSpeak(body='You can end this call at any time.')

    response.add(getDigits)

    return HttpResponse(str(response), content_type='text/xml')


@csrf_exempt
def mm_response(request):
    if request.method == 'GET':
        return exit_sequence()
    post_args = request.POST

    response = plivo.Response()
    input_digit = post_args.get('Digits', None)
    if input_digit != "1" and input_digit != "2":
        response.addSpeak(body="Sorry, we did not receive a valid response. "
                          "You will now be redirected back to the main menu.")
        response.addWait(length=1)
        action_url = '/guess_game/'
        absolute_action_url = request.build_absolute_uri(action_url)
        response.addRedirect(body=absolute_action_url, method='POST')
        return HttpResponse(str(response), content_type='text/xml')
    else:
        if input_digit == "1":
            action_url = '/play_game/'
            absolute_action_url = request.build_absolute_uri(action_url)
            response.addRedirect(body=absolute_action_url, method='POST')
            return HttpResponse(str(response), content_type='text/xml')
        else:
            action_url = '/how_to_play/'
            absolute_action_url = request.build_absolute_uri(action_url)
            response.addRedirect(body=absolute_action_url, method='POST')
            return HttpResponse(str(response), content_type='text/xml')


@csrf_exempt
def exit_sequence(msg="Oops! There was an error!"):
    response = plivo.Response()
    response.addSpeak("We will hangup now.")
    response.addHangup()
    return HttpResponse(str(response), content_type='text/xml')


@csrf_exempt
def play_game(request):
    if not request.GET.get('guesses', None):
        secret = random.randint(1, 100)
        guesses = 10

        response = plivo.Response()
        action_url = '/play_game/?secret=%d&guesses=%d' % (secret, guesses)
        absolute_action_url = request.build_absolute_uri(action_url)
        getDigits = plivo.GetDigits(action=absolute_action_url, method='POST',
                                    timeout=10, numDigits=4, retries=1)
        getDigits.addSpeak(body="I have thought of a secret number between "
                           "one and one hundred. "
                           "You have ten guesses to find it!")
        getDigits.addSpeak(body="You can make your guess now.")
        response.add(getDigits)
        return HttpResponse(str(response), content_type='text/xml')
    else:
        secret = int(request.GET.get('secret', '0'))
        guesses = int(request.GET.get('guesses', '0')) - 1
        action_url = 'play_game/?secret=%d&guesses=%d' % (secret, guesses)
        absolute_action_url = request.build_absolute_uri(action_url)

        input_num = request.POST.get('Digits', "0")
        response = plivo.Response()
        try:
            input_num = int(input_num)
        except ValueError, e:
            print e
            return exit_sequence()

        if input_num == secret:
            response.addSpeak("Congratulations! %d is the right number!"
                              " You have guessed"
                              " it in %d guesses - your score is %d." %
                              (secret, 10 - guesses, guesses + 1))
            response.addWait(length=2)
            response.addHangup()
            return HttpResponse(str(response), content_type='text/xml')
        else:
            if input_num > secret:
                answer = "Sorry, you guessed %d. The secret is lesser."
            else:
                answer = "Sorry, you guessed %d. The secret is greater."
            response.addSpeak(answer % (input_num))
            if guesses > 0:
                getDigits = plivo.GetDigits(action=absolute_action_url,
                                            method='POST',
                                            timeout=10, numDigits=4,
                                            retries=1)
                getDigits.addWait(length=1)
                getDigits.addSpeak("You have %d guesses remaining! Guess again!" % guesses)
                response.add(getDigits)
            else:
                response.addWait(length=1)
                response.addSpeak("Sorry, you don't have any remaining guesses. The secret was %d." % (secret))
                response.addHangup()
            return HttpResponse(str(response), content_type='text/xml')


@csrf_exempt
def how_to_play(request):
    response = plivo.Response()
    response.addSpeak(body="I will think of a secret number that you will have to guess.")
    response.addSpeak(body="The number will be between one and one hundred.")
    response.addSpeak(body="To guess a number just dial the digits and end with the hash sign.")
    response.addSpeak(body="For each guess, if it is not the secret number, I will tell you if it is lesser of greater than it.")
    response.addSpeak(body="You will have a maximum of ten chances to guess the number.")

    response.addWait(length=2)
    response.addSpeak(body="You will now be transferred to the main menu.")

    redirect_url = "/guess_game/"
    abs_red_url = request.build_absolute_uri(redirect_url)
    response.addRedirect(body=abs_red_url, method='POST')

    return HttpResponse(str(response), content_type='text/xml')
