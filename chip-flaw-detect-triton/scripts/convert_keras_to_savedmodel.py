import os
import argparse

import tensorflow as tf
from adabelief_tf import AdaBeliefOptimizer
from tensorflow_addons.losses import SigmoidFocalCrossEntropy

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inp', required=True, type=str)
    parser.add_argument('--out', required=True, type=str)
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    model = tf.keras.models.load_model(
        args.inp,
        custom_objects={
            "AdaBeliefOptimizer": AdaBeliefOptimizer,
            "SigmoidFocalCrossEntropy": SigmoidFocalCrossEntropy
        }
    )
    model.save(args.out)
    
    
    
    
    
if __name__ == '__main__':
    main()
    
