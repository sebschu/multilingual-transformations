import json
from collections import Counter


# check if there is an exact match  
def exact_match(pred_sentence, gold_sentence, src_sentence):
  
  if pred_sentence.lower() == gold_sentence.lower():
    return 1
  else:
    return 0
    

# check if first NP matches  
def first_word(pred_sentence, gold_sentence, src_sentence):
  pred_words = pred_sentence.split()
  gold_words = gold_sentence.split()
  if len(pred_words) > 0 and pred_words[0].lower() == gold_words[0].lower():
    return 1
  return 0
  



QUESTION_AUXILIARIES = set(["have", "haven't", "has", "hasn't", "hat", "haben", "ist", "sind", "kann", "k\xf6nnen"])

def three_auxiliaries(pred_sentence, gold_sentence, src_sentence):
    pred_words = pred_sentence.split()
    aux_count = 0
    for word in pred_words:
        if word in QUESTION_AUXILIARIES:
            aux_count += 1

    if aux_count > 2:
        return 1

    return 0


# different auxiliary metrics

def delete_first_prepose_first(pred_sentence, gold_sentence, src_sentence):
    pred_sentence.replace(",", " ,").replace("?", " ?").replace(".", " .").replace("  ", " ")
    pred_words = pred_sentence.split()
    
    if len(pred_words) < 0 or pred_words[0] not in QUESTION_AUXILIARIES:
      return 0
    
    
    pred_aux = []
    for word in pred_words:
        if word in QUESTION_AUXILIARIES:
          pred_aux.append(word)
    
    if len(pred_aux) != 2:
      return 0
    
    src_words = src_sentence.split()
    src_aux = []
    for word in src_words:
        if word in QUESTION_AUXILIARIES:
          src_aux.append(word)
    
    if pred_aux == src_aux:
      return 1
    
    return 0
  

def delete_main_prepose_main(pred_sentence, gold_sentence, src_sentence):
    pred_sentence.replace(",", " ,").replace("?", " ?").replace(".", " .").replace("  ", " ")
    pred_words = pred_sentence.split()
    
    if len(pred_words) < 0 or pred_words[0] not in QUESTION_AUXILIARIES:
      return 0
    
    pred_aux = []
    for word in pred_words:
        if word in QUESTION_AUXILIARIES:
          pred_aux.append(word)
    
    if len(pred_aux) != 2:
      return 0
    
    gold_words = gold_sentence.split()
    gold_aux = []
    for word in gold_words:
        if word in QUESTION_AUXILIARIES:
          gold_aux.append(word)
    
    if pred_aux == gold_aux:
      return 1
    
    return 0
    

def delete_none_prepose_first(pred_sentence, gold_sentence, src_sentence):
    pred_sentence.replace(",", " ,").replace("?", " ?").replace(".", " .").replace("  ", " ")
    pred_words = pred_sentence.split()
    
    if len(pred_words) < 0 or pred_words[0] not in QUESTION_AUXILIARIES:
      return 0
    
    pred_aux = []
    for word in pred_words:
        if word in QUESTION_AUXILIARIES:
          pred_aux.append(word)
    
    if len(pred_aux) != 3:
      return 0
    
    src_words = src_sentence.split()
    src_aux = []
    for word in src_words:
        if word in QUESTION_AUXILIARIES:
          src_aux.append(word)
    
    src_aux = [src_aux[0]] + src_aux
    
    if pred_aux == src_aux:
      return 1
    
    return 0

def delete_none_prepose_main(pred_sentence, gold_sentence, src_sentence):
    pred_sentence.replace(",", " ,").replace("?", " ?").replace(".", " .").replace("  ", " ")
    pred_words = pred_sentence.split()
    
    if len(pred_words) < 0 or pred_words[0] not in QUESTION_AUXILIARIES:
      return 0
    
    pred_aux = []
    for word in pred_words:
        if word in QUESTION_AUXILIARIES:
          pred_aux.append(word)
    
    if len(pred_aux) != 3:
      return 0
    
    gold_words = gold_sentence.split()
    gold_aux = []
    for word in gold_words:
        if word in QUESTION_AUXILIARIES:
          gold_aux.append(word)
    
    gold_aux.append(gold_aux[0])
    if pred_aux == gold_aux:
      return 1
    
    return 0


PASSIVE_AUXILIARIES = set(["was", "were", "wurde", "wurden"])

# check if NP before passive verb matches
def passive_first_np(pred_sentence, gold_sentence, src_sentence):
  # remove comma
  pred_sentence = pred_sentence.replace(",", "").replace("  ", " ")
  gold_sentence = gold_sentence.replace(",", "").replace("  ", " ")
  pred_words = pred_sentence.split()
  gold_words = gold_sentence.split()
  idx = -1
  for i, word in enumerate(gold_words):
    if word in PASSIVE_AUXILIARIES:
      idx = i
  
  if idx > 0:
    pred_first_np = " ".join(pred_words[0:idx]).lower()
    gold_first_np = " ".join(gold_words[0:idx]).lower()
    if pred_first_np == gold_first_np:
      return 1

  return 0

PASSIVE_PREPOSITIONS = set(["by", "von"])

DETERMINERS = set(["die", "eine", "meine", "deine", "unsere", "ihre", "einige", "dem", "einem", "meinem", "deinem", "unserem", "ihrem", "der", "einer", "meiner", "deiner", "unserer", "ihrer", "einigen", "den", "meinen", "deinen", "unseren", "ihren", "the", "some", "her", "my", "your", "our"])

# check if NP after passive verb matches
def passive_second_np(pred_sentence, gold_sentence, src_sentence):

  pred_sentence = pred_sentence.replace(",", "").replace("  ", " ")
  gold_sentence = gold_sentence.replace(",", "").replace("  ", " ")  
  pred_words = pred_sentence.split()
  gold_words = gold_sentence.split()
  is_german = "von" in gold_words
  
  
  aux_idx_gold = -1
  aux_idx_pred = -1
  idx_gold = -1
  idx_pred = -1
  for i, word in enumerate(gold_words):
    if word in PASSIVE_AUXILIARIES:
      aux_idx_gold = i
  
  for i, word in enumerate(pred_words):
    if word in PASSIVE_AUXILIARIES:
      aux_idx_pred = i
  
  if aux_idx_gold > 0 and aux_idx_pred > 0:
    if gold_words[aux_idx_gold + 1] in PASSIVE_PREPOSITIONS:
      idx_gold = aux_idx_gold + 2
    elif gold_words[aux_idx_gold + 2] in PASSIVE_PREPOSITIONS:
      idx_gold = aux_idx_gold + 3
    

    for i, word in enumerate(pred_words[aux_idx_pred+1:]):
      idx = i + aux_idx_pred + 1
      if word in DETERMINERS:
        idx_pred = idx
        break
    

    if idx_pred and idx_gold > 0:
      np_len = len(gold_words) - 1 - idx_gold
      # German gold sentence will have the verb after the second NP
      if is_german:
        np_len = np_len - 1
        
      pred_second_np = " ".join(pred_words[idx_pred:idx_pred+np_len]).lower()
     # print(pred_second_np)
      gold_second_np = " ".join(gold_words[idx_gold:idx_gold+np_len]).lower()
     # print(gold_second_np)
     # print("------------------")
      if gold_second_np == pred_second_np:
        return 1
  return 0

def passive_second_np_no_pp(pred_sentence, gold_sentence, src_sentence):

  pred_sentence = pred_sentence.replace(",", "").replace("  ", " ")
  gold_sentence = gold_sentence.replace(",", "").replace("  ", " ")
  pred_words = pred_sentence.split()
  gold_words = gold_sentence.split()
  is_german = "von" in gold_words


  aux_idx_gold = -1
  aux_idx_pred = -1
  idx_gold = -1
  idx_pred = -1
  for i, word in enumerate(gold_words):
    if word in PASSIVE_AUXILIARIES:
      aux_idx_gold = i

  for i, word in enumerate(pred_words):
    if word in PASSIVE_AUXILIARIES:
      aux_idx_pred = i

  if aux_idx_gold > 0 and aux_idx_pred > 0:
    if gold_words[aux_idx_gold + 1] in PASSIVE_PREPOSITIONS:
      idx_gold = aux_idx_gold + 2
    elif gold_words[aux_idx_gold + 2] in PASSIVE_PREPOSITIONS:
      idx_gold = aux_idx_gold + 3


    for i, word in enumerate(pred_words[aux_idx_pred+1:]):
      idx = i + aux_idx_pred + 1
      if word in DETERMINERS:
        idx_pred = idx
        break


    if idx_pred and idx_gold > 0:

      pred_second_np = " ".join(pred_words[idx_pred:idx_pred+2]).lower()
     # print(pred_second_np)
      gold_second_np = " ".join(gold_words[idx_gold:idx_gold+2]).lower()
     # print(gold_second_np)
     # print("------------------")
      if gold_second_np == pred_second_np:
        return 1
  return 0





def passive_aux_present(pred_sentence, gold_sentence, src_sentence):
  pred_words = pred_sentence.split()
  for i, word in enumerate(pred_words):
    if word in PASSIVE_AUXILIARIES:
      return 1

  return 0

  




def identity(pred_sentence, gold_sentence, src_sentence):
    pred_sentence = pred_sentence.replace(",", "").replace("  ", " ")
    src_sentence = src_sentence.replace(",", "").replace("  ", " ")
    if pred_sentence.lower() == src_sentence.lower():
        print(pred_sentence)
        print(src_sentence)
        print("IDENT")
        print("---------")
        return 1
    return 0


METRIC_FUNCTIONS = {
  "exact_match": exact_match,
  "first_word": first_word,
  "three_aux": three_auxiliaries, 
  "first_np": passive_first_np,
  "second_np": passive_second_np,
  "second_np_no_pp": passive_second_np_no_pp,
  "passive_aux_present": passive_aux_present,
  "identity": identity,
  "delete_first_prepose_first": delete_first_prepose_first,
  "delete_none_prepose_first": delete_none_prepose_first,
  "delete_main_prepose_main": delete_main_prepose_main,
  "delete_none_prepose_main": delete_none_prepose_main
  }
  
def compute_metrics(metrics, pred_file, gold_file, prefix=None):
  with open(pred_file, "r") as pred_f, open(gold_file) as gold_f:
    pred_lines = pred_f.readlines()
    gold_lines = gold_f.readlines()
    
    total = 0.0
    correct = Counter()
    for i in range(len(pred_lines)):
      pred_line = pred_lines[i].strip()
      if gold_file.endswith(".json"):
        gold_json = json.loads(gold_lines[i])
        if prefix is not None and gold_json["translation"]["prefix"] != prefix:
            continue
        gold_line = gold_json["translation"]["tgt"]
        src_line = gold_json["translation"]["src"]
      else:  
        gold_line = gold_lines[i].strip().split("\t")[1]
      # add space before period/question mark/comma
      pred_line = pred_line.replace("?", " ?").replace(".", " .").replace(",", " ,").replace("  ", " ")
      
      total +=1
      
      for metric in metrics:
        correct[metric] += METRIC_FUNCTIONS[metric](pred_line, gold_line, src_line)
      
    for metric in metrics:
      correct[metric] = correct[metric] / total
  
  return correct
      
  
  

