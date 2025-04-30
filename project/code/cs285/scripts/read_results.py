import glob
# import tensorflow as tf
from tensorflow.python.summary.summary_iterator import summary_iterator

def get_section_results(file):
    """
        requires tensorflow==1.12.0
    """
    X = [1]
    Y = [2]
    for e in summary_iterator(file):
        for v in e.summary.value:
            if v.tag == 'Train_EnvstepsSoFar':
                X.append(v.simple_value)
            elif v.tag == 'Eval_AverageReturn':
                Y.append(v.simple_value)
    return X, Y

if __name__ == '__main__':
    import glob

    logdir = 'data/q1_sb_rtg_dsa_CartPole-v0_26-09-2020_15-14-17/events.out.tfevents.1601158457.hayashiintans-MacBook-Pro.local'
    eventfile = glob.glob(logdir)[0]
    X, Y = get_section_results(eventfile)
    for i, (x, y) in enumerate(zip(X, Y)):
        print('Iteration {:d} | Train steps: {:d} | Return: {}'.format(i, int(x), y))