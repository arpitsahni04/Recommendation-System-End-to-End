import os
import sys
import pandas as pd
from sklearn.metrics import mean_squared_error
from scipy.stats import ttest_ind
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def check_drift(train_ratings_df_path,new_ratings_df_path,sender_email_address,sender_email_password,recipient_email_address,stats_txt_path,stats_csv_path):
    # Load initial ratings and user dataframe used to train the model
    train_ratings_df = pd.read_csv(train_ratings_df_path)

    # Load new incoming ratings and user dataframe obtained every 24 hours from kafka stream
    new_ratings_df = pd.read_csv(new_ratings_df_path)

    # Check for data drift by comparing statistics of the two datasets
    # Compute mean and standard deviation of ratings in both datasets
    train_mean_rating = train_ratings_df['rating'].mean()
    train_std_rating = train_ratings_df['rating'].std()
    new_mean_rating = new_ratings_df['rating'].mean()
    new_std_rating = new_ratings_df['rating'].std()

    # Check for concept drift by comparing the distribution of ratings in both datasets
    # Use a two-sample t-test with a 5% significance level
    t_stat, p_val = ttest_ind(train_ratings_df['rating'], new_ratings_df['rating'], equal_var=False)

    # Define threshold values for data and concept drift
    rating_threshold = 0.2 # 20% change in mean rating or standard deviation of rating
    p_val_threshold = 0.05 # 5% significance level for t-test

    # Send email alert if there is a substantial drift
    if abs(train_mean_rating - new_mean_rating) > rating_threshold*train_mean_rating or \
        abs(train_std_rating - new_std_rating) > rating_threshold*train_std_rating or \
        p_val < p_val_threshold:
        
        # Create message for email alert
        msg = MIMEText("There is a substantial drift in the movie recommendation system.\n"
                    "Mean rating: train={}, new={}\n"
                    "Std rating: train={}, new={}\n"
                    "t-statistic: {}\n"
                    "p-value: {}".format(train_mean_rating, new_mean_rating,
                                            train_std_rating, new_std_rating,
                                            t_stat, p_val))
        try: 
            # Set up email server and send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email_address, sender_email_password)
            server.sendmail(sender_email_address, recipient_email_address, msg.as_string())
            server.quit()
        
        except:
            print("Failed to send mail but here are the comparison stats:")
            print(msg)
    else:

        # Print statistics if no substantial drift
        msg = ("There was no substantial drift in the movie recommendation system, but here are some stats.\n"
                    "Mean rating: train={}, new={}\n"
                    "Std rating: train={}, new={}\n"
                    "t-statistic: {}\n"
                    "p-value: {}".format(train_mean_rating, new_mean_rating,
                                            train_std_rating, new_std_rating,
                                            t_stat, p_val))
        print("No drift was detected, but here are some stats:")
        print(msg)
    
    #save the statistics comparison of the two ratings matrices
    print("Saving stats...")
    
    write_file = f"{new_ratings_df_path},{train_mean_rating},{new_mean_rating},{train_std_rating},{new_std_rating},{t_stat},{p_val}\n"
    start_file = "Day,Train mean,New mean,Train std,New std,t-statistic,p-value\n"
    is_start = False
    if os.path.getsize(stats_txt_path) == 0:
        is_start = True
        
    with open(stats_txt_path,'a') as f:
        if is_start:
            f.write(start_file)
        f.write(write_file)
    f.close()

    stats = pd.read_csv(stats_txt_path,sep=',')
    stats = stats.drop_duplicates(keep='last',ignore_index=True)
    stats.to_csv(stats_csv_path)

    print("Stats file finished updating!")

if __name__=='__main__':
    train_ratings_df_path = sys.argv[1]
    new_ratings_df_path = sys.argv[2]
    sender_email_address = sys.argv[3]
    sender_email_password = sys.argv[4]
    recipient_email_address = sys.argv[5]
    stats_txt_path = sys.argv[6]
    stats_csv_path = sys.argv[7]
    check_drift(train_ratings_df_path,new_ratings_df_path,sender_email_address,sender_email_password,recipient_email_address,stats_txt_path,stats_csv_path)