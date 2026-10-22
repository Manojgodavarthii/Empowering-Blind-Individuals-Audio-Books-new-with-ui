from transformers import BlipProcessor, BlipForConditionalGeneration, AutoTokenizer, AutoModelForCausalLM

print("Downloading and saving BLIP to ./models/blip ...")
blip_proc = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
blip_proc.save_pretrained("./models/blip")
blip_model.save_pretrained("./models/blip")

print("Downloading and saving Qwen to ./models/qwen ...")
qwen_tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
qwen_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
qwen_tok.save_pretrained("./models/qwen")
qwen_model.save_pretrained("./models/qwen")

print("Saved locally. You can now load entirely offline from disk!")