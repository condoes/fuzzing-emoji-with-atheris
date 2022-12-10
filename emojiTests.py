import atheris

with atheris.instrument_imports():
    import emoji
    import sys


@atheris.instrument_func
def TestDemojizeInput(input_bytes):

    fdp = atheris.FuzzedDataProvider(input_bytes)
    # only want unicode for fuzzed inputs
    data = fdp.ConsumeUnicode(sys.maxsize)

    em = emoji.demojize(data)

def TestEmojiCountInput(input_bytes):
    fdp = atheris.FuzzedDataProvider(input_bytes)
    data = fdp.ConsumeUnicodeNoSurrogates(sys.maxsize)

    if ((emoji.emoji_count(data)) > 0):
        raise RuntimeError('Found emoji')

def TestEmojizeInput(input_byte):
    fdp = atheris.FuzzedDataProvider(input_bytes)
    data = fdp.ConsumeUnicodeNoSurrogates(sys.maxsize)

    if len(data) !=8:
        return 

    try: 
        (emoji.is_emoji(emoji.emojize(data)))
    except:
         raise RuntimeError ('is an emoji')

def TestMutatorInput(input_bytes):
    fdp = atheris.FuzzedDataProvider(input_bytes)
    data = fdp.ConsumeUnicodeNoSurrogates(sys.maxsize)
    # print(f"Test data {data}")
    try:
        em = emoji.demojize(data)
    except:
        return
    
    # print(f"Test returns {em}")
    return em
        
def CustomMutator(input, size, seed):
    # print(f"Input before Mutate: {input}")

    data = atheris.Mutate(input, size)

    # print(f"Data after mutation: { data }")
    
    return data

atheris.Setup(sys.argv, TestDemojizeInput)
atheris.Fuzz()