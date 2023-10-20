import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import argparse

# Define a class to perform the experimentation
class MovieRecommendationExperiment:
    def __init__(self, rating_set_A, rating_set_B, watch_file_A, watch_file_B):
        # Load the rating sets A and B
        self.rating_set_A = rating_set_A
        self.rating_set_B = rating_set_B
        self.watch_file_A = watch_file_A
        self.watch_file_B = watch_file_B
    
    def run_experiment(self):
        # Compare average ratings for the two user ratings set
        rates_A = pd.read_csv(self.rating_set_A,header=None)
        rates_A = rates_A[0].values
        avg_rate_A = np.mean(rates_A)

        rates_B = pd.read_csv(self.rating_set_B,header=None)
        rates_B = rates_B[0].values
        avg_rate_B = np.mean(rates_B)

        # Compare average watch times for the two user watch times set
        watch_A = pd.read_csv(self.watch_file_A,header=None)
        watch_A = watch_A[0].values
        avg_watch_A = np.mean(watch_A)

        watch_B = pd.read_csv(self.watch_file_B,header=None)
        watch_B = watch_B[0].values
        avg_watch_B = np.mean(watch_B)


        # Get t statistic and p value for t-test for rate sets
        tstat_rate, pval_rate = ttest_ind(rates_A,rates_B)

        # Get t statistic and p value for t-test for rate sets
        tstat_watch, pval_watch = ttest_ind(watch_A,watch_B)

        return avg_rate_A, avg_rate_B, avg_watch_A, avg_watch_B, tstat_rate, pval_rate, tstat_watch, pval_watch, len(rates_A), len(rates_B), len(watch_A),len(watch_B)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Movie Recommendation Experimentation')
    parser.add_argument('rating_set_A', type=str, help='Rating Set A path')
    parser.add_argument('rating_set_B', type=str, help='Rating Set B path')
    parser.add_argument('watch_file_A', type=str, help='Watching log A path')
    parser.add_argument('watch_file_B', type=str, help='Watching log B path')
    args = parser.parse_args()
    # Instantiate two rating sets, two watch files and a MovieRecommendationExperiment object
    rating_set_A = args.rating_set_A
    rating_set_B = args.rating_set_B
    watch_file_A = args.watch_file_A
    watch_file_B = args.watch_file_B
    experiment = MovieRecommendationExperiment(rating_set_A,rating_set_B,watch_file_A,watch_file_B)

    # Run the experiment with the specified group size
    avg_rate_A, avg_rate_B, avg_watch_A, avg_watch_B, tstat_rate, pval_rate, tstat_watch, pval_watch, num_rates_A, num_rates_B, num_watch_A, num_watch_B = experiment.run_experiment()

    # Print statistics
    print ("{:<25}|{:<25}|{:<25}".format('Metric','A','B'))
    print('-'*70)
    print ("{:<25}|{:<25}|{:<25}".format('Number of rate samples', num_rates_A, num_rates_B))
    print ("{:<25}|{:<25}|{:<25}".format('Number of watch samples', num_watch_A, num_watch_B))
    print ("{:<25}|{:<25}|{:<25}".format('Avg Rating', avg_rate_A, avg_rate_B))
    print ("{:<25}|{:<25}|{:<25}".format('Avg Watch time', avg_watch_A, avg_watch_B))
    print()
    print ("{:<15}|{:<25}".format('Metric','Rate sets'))
    print('-'*35)
    print ("{:<15}|{:<25}".format('T statistic', tstat_rate))
    print ("{:<15}|{:<25}".format('P value', pval_rate))
    print()
    print ("{:<15}|{:<25}".format('Metric','Watch sets'))
    print('-'*35)
    print ("{:<15}|{:<25}".format('T statistic', tstat_watch))
    print ("{:<15}|{:<25}".format('P value', pval_watch))