import taml
while True:
    text = input('TAML 8==> ')
    result, error = taml.run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)