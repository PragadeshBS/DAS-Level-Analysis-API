def get_reponse_for_question(question: str, tokenizer, saved_model):
    bot_input_ids = tokenizer.encode(
        question + tokenizer.eos_token, return_tensors="pt"
    )
    chat_history_ids = saved_model.generate(
        bot_input_ids,
        max_length=100,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=10,
        top_p=0.7,
        temperature=0.8,
    )
    return tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1] :][0],
        skip_special_tokens=True,
    ).replace(" Charlie", "")
