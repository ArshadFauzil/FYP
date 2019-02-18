from nltk.parse.generate import generate, demo_grammar
from nltk import CFG

varname = 'rand'
value = 'variable value'
variableGrammar = CFG.fromstring("""
            S -> VN "=" VV
            VN -> '"""+varname+"""'
            VV -> "'"'"""+value+"""'"'"
            """)

arrName = 'arr'
arrayGrammar = CFG.fromstring("""
            S -> AN "= [" AE "]"
            AN -> '"""+arrName+"""'
            AE -> VV AE | VV
            VV -> 
            """)
print(variableGrammar)
print("")
for sentence in generate(variableGrammar):
    print(' '.join(sentence))