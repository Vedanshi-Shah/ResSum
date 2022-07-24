from fastT5 import get_onnx_model, get_onnx_runtime_sessions, OnnxT5
from transformers import T5Config,AutoTokenizer
from pathlib import Path
import os

trained_model_path = './t5-large'
pretrained_model_name = Path(trained_model_path).stem
encoder_path = os.path.join(trained_model_path, f"{pretrained_model_name}-encoder-quantized.onnx")
decoder_path = os.path.join(trained_model_path, f"{pretrained_model_name}-decoder-quantized.onnx")
init_decoder_path = os.path.join(trained_model_path, f"{pretrained_model_name}-init-decoder-quantized.onnx")

model_paths = encoder_path, decoder_path, init_decoder_path
model_sessions = get_onnx_runtime_sessions(model_paths)

t5_model = OnnxT5(trained_model_path, model_sessions)
t5_tokenizer = AutoTokenizer.from_pretrained(trained_model_path)

sents = """
    There's nothing more romantic than a hunt for hidden treasure—and when those riches are located in the watery depths of the ocean, it can seem even more exciting. Shipwrecks spark the imagination, prompting dreams of untold riches and swashbuckling adventure.
More vessels lie at the bottom of the sea than you might think; the National Oceanic and Atmospheric Administration’s database lists over 10,000 known wrecks off of United States shores alone—and that’s not a complete list. According to United Nations cultural agency UNESCO, there are at least 3 million such wrecks worldwide, some thousands of years old.
"""

inputs = t5_tokenizer.encode("summarize: " + sents, return_tensors="pt", max_length=512, padding="max_length", truncation=True)
summary_ids = t5_model.generate(inputs, num_beams=int(2),no_repeat_ngram_size=3,length_penalty=2.0,min_length=50,max_length=500,early_stopping=True)
output = t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
print(output)
