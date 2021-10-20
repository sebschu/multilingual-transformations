import numpy as np
import os
import re
import sys
import glob
import argparse
import matplotlib.pyplot as plt

from metrics import compute_metrics



def main():


      argparser = argparse.ArgumentParser()
      
      argparser.add_argument("--checkpoint_dir")
      argparser.add_argument("--gold_filename")
      argparser.add_argument("--metrics")
      
      argparser.add_argument("--out_dir")    
      args = argparser.parse_args()
      
      if args.out_dir is None:
        args.out_dir = args.checkpoint_dir

      eval_results = {}
      metric_names = args.metrics.split(",")
      metrics_str = "-".join(metric_names)
      basename = os.path.basename(args.gold_filename).replace(".json", "")
      for path in glob.glob(os.path.join(args.checkpoint_dir, "checkpoint-*", "")):

          pred_filename = os.path.join(path, basename + ".eval_preds_seq2seq.txt")
          it_res = re.match(".*checkpoint-([0-9]+)[/].*", path)
          it = int(it_res.group(1))
          print(">>>", it)
          eval_results[it] = compute_metrics(metric_names, pred_filename, args.gold_filename) 
          
      for m in metric_names:
        its = sorted(eval_results.keys())
        vals = []
        for it in its:
          vals.append(eval_results[it][m])
        plt.plot(its,vals, label=m)
        
            
      plt.legend()
      plt.savefig(os.path.join(args.out_dir, basename + "." + metrics_str + ".learning_curve.png"))



if __name__ == '__main__':
  main()
