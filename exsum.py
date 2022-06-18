from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def lex_rank(name):
    inp = f"parsed-output/{name}.txt"
    out = f"parsed-output/{name}.txt"
    with open(inp, "r", encoding="utf-8") as f:
        sample_text = f.read()
    f.close()
    my_parser = PlaintextParser.from_string(sample_text,Tokenizer('english'))
    lex_rank_summarizer = LexRankSummarizer()
    lexrank_summary = lex_rank_summarizer(my_parser.document,sentences_count=64)
    lexranksumm=[]
    for sentence in lexrank_summary:
        lexranksumm.append(sentence.__str__())
        #print(sentence)
    lexranksummary = ' '.join(lexranksumm)
    with open(out, "w", encoding="utf-8") as f:
        f.write(lexranksummary)
    f.close()

 