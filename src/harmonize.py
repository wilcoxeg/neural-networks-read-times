from collections import Counter

import regex as re



punct_at_end_re = re.compile(r"[-,.!?'\"$()[\]:;]+$")
punct_at_start_re = re.compile(r"^[-,.!?'\"$()[\]:;]+")

# NB we have a branch reset group here. There are just two match groups.
contractions_re = re.compile(r"(?"
                             "|([^' ])('ll|'LL|'re|'RE|'ve|'VE|n't|N'T|'[sS]|'[mM]|'[dD])"
                             "|(can)(not)|(CAN)(NOT))")

def harmonize_rows(ref, d, log_target_code=None):
    """
    Harmonize reading-time and surprisal data which differs in tokenization
    procedures and UNKification.
    
    Args:
        ref: List of reading-time observations, each a tuple of the form
            `(code, token, rt)`, where `code` is a unique integer reference
            for the token within the relevant corpus.
        d: List of model surprisal observations, each a tuple of the form
            `(model_token, surprisal)`.
            
    Returns:
        result: A list of merged reading-time--surprisal data, with each item
            a tuple of the form `(model_token, surprisal, code, token, rt)`.
    """
    
    mismatches = Counter()
    result = []
    curr_d = d.pop(0)
    curr_ref = ref.pop(0)
    
    def process_detokenized(curr_d, curr_ref):
        """
        Remove detokenized trailing and leading punctuation from around the
        current matched data--reference pair.
        
        NB updates `ref`, `d` in-place.
        
        Returns:
            changed: True if the surrounding context was updated.
            curr_d: updated curr_d pointer
            curr_ref: updated curr_ref pointer
        """
        model_token, surprisal = curr_d
        code, rt_token, rt = curr_ref
        
        changed = True
        
        if punct_at_start_re.search(rt_token) and punct_at_end_re.search(rt_token):
            rt_token_new = punct_at_start_re.sub("", punct_at_end_re.sub("", rt_token))
            curr_ref = (code, rt_token_new, rt)

            # If current model token(s) are that punctuation, drop those tokens
            match = punct_at_start_re.findall(rt_token)[0]
            while match.startswith(model_token):
                match = match[len(model_token):]
                model_token, surprisal = d.pop(0)

            curr_d = (model_token, surprisal)

            # If next model token(s) are that punctuation, drop those tokens
            match = punct_at_end_re.findall(rt_token)[0]
            while match.startswith(d[0][0]):
                match = match[len(d[0][0]):]
                d.pop(0)
        # If current ref has trailing punctuation, remove and re-check
        elif punct_at_end_re.search(rt_token):
            rt_token_new = punct_at_end_re.sub("", rt_token)
            curr_ref = (code, rt_token_new, rt)

            # If next model token(s) are that punctuation, drop those tokens
            match = punct_at_end_re.findall(rt_token)[0]
            while match.startswith(d[0][0]):
                match = match[len(d[0][0]):]
                popped = d.pop(0)
        # If current ref has leading punctuation, remove and re-check
        elif punct_at_start_re.search(rt_token):
            rt_token_new = punct_at_start_re.sub("", rt_token)
            curr_ref = (code, rt_token_new, rt)
            
            # If current model token(s) are that punctuation, drop those tokens
            match = punct_at_start_re.findall(rt_token)[0]
            while match.startswith(model_token):
                match = match[len(model_token):]
                model_token, surprisal = d.pop(0)

            curr_d = (model_token, surprisal)
            
        code, rt_token, rt = curr_ref
        # Process PTB detokenized contractions
        if contractions_re.search(rt_token):
            
            # Check that future model tokens comport with this detected
            # contraction.
            #
            # Rather than strictly checking equality between the concatenation
            # of the future model tokens with the current and the RT token,
            # we'll just check the equality of the succeeding tokens with the
            # relevant part of the RT token. This is because sometimes the RT
            # token "stem" and the original model token *should* mismatch --
            # e.g. when the model token is an UNK.
            ideal_tokenized_suffix = tuple(contractions_re.search(rt_token).group(2).split(" "))
            future_model_rows = d[:len(ideal_tokenized_suffix)]
            future_model_tokens = tuple(tok for tok, _ in future_model_rows)
            if ideal_tokenized_suffix == future_model_tokens:
                # Build a little synthetic `curr_d`, `curr_ref` by adding surprisals
                curr_d = (model_token + "".join(future_model_tokens),
                          surprisal + sum(surp for _, surp in future_model_rows))
                # Pop off those tokens from the queue now that they've been absorbed
                for _ in range(len(future_model_tokens)):
                    d.pop(0)
            else:
                # Do nothing.
                changed = False
        else:
            changed = False
            
        return changed, curr_d, curr_ref
    
    def log(curr_d, curr_ref, flags=""):
        model_token, surprisal = curr_d
        code, rt_token, rt = curr_ref
        print(f"{flags}\t{code}\t{rt_token}\t{model_token}")
    
    to_print = 0
    mismatched = [0, None]
    while len(d) > 10:
        model_token, surprisal = curr_d
        code, rt_token, rt = curr_ref
        
        #### HACKS
        # Dundee 61827: "[sic]" has corresponding mysterious "UNK-CAPS-DASH"
        # token preceding it. It's possible that the punctuation was dropped
        # from the Dundee data.
        if code == 61827 and rt_token == "[sic]" and model_token == "UNK-CAPS-DASH":
            curr_d = d.pop(0)
            continue
        
        if punct_at_start_re.search(rt_token):
            to_print = 10
            
        if to_print > 0:
            #log(curr_d, curr_ref)
            to_print -= 1
            if to_print == 0:
                pass
                #print("=======")
                
        if log_target_code is not None and code > log_target_code - 10 and code < log_target_code + 10:
            log(curr_d, curr_ref, "**" if code == log_target_code else "")
                
        if mismatched[0] == 5:
            mismatches[mismatched[1]] += 1
        
        if model_token == rt_token:
            result.append(curr_d + curr_ref)
            curr_d = d.pop(0)
            curr_ref = ref.pop(0)
            mismatched = [0, None]
        else:
            if mismatched[0] == 0:
                mismatched = [1, code]
            else:
                mismatched[0] += 1
            # If current token is unked, then pop both
            if "UNK" in model_token:
                # Before we pop, handle possible punctuation on the rt_token
                process_detokenized(curr_d, curr_ref)
                curr_d = d.pop(0)
                curr_ref = ref.pop(0)
                
            # Check for possible punctuation modifications
            else:
                updated, curr_d, curr_ref = process_detokenized(curr_d, curr_ref)
                if updated:
                    # Punctuation context was modified -- run back through the loop.
                    continue
                # If current ref has leading punctuation, pop both
                elif not rt_token.isalpha():
                    curr_ref = ref.pop(0)
                    curr_d = d.pop(0)
                #If the current word is the end of a line
                elif "EOL" in rt_token:
                    curr_ref = ref.pop(0)
                    curr_d = d.pop(0)
                else:
                    curr_d = d.pop(0)

    return result, mismatches