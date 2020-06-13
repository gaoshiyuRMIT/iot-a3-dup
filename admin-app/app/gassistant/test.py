from assistant import AspenAssistant

test = AspenAssistant()

print(test)
continue_conv, response_text, user_input, rthing = test.assist()
print (continue_conv)
print (user_input)
print (response_text)
print (rthing)