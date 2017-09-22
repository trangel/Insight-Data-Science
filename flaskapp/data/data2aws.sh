# model
scp -i ../../aws/autismxpert.pem lsi* ubuntu@13.59.215.199://home/ubuntu/Insight/flaskapp/data/.
scp -i ../../aws/autismxpert.pem tdidf.save ubuntu@13.59.215.199://home/ubuntu/Insight/flaskapp/data/.
scp -i ../../aws/autismxpert.pem dictionary.save ubuntu@13.59.215.199://home/ubuntu/Insight/flaskapp/data/.

# dataframe
scp -i ../../aws/autismxpert.pem *csv ubuntu@13.59.215.199://home/ubuntu/Insight/flaskapp/data/.

# questions
scp -i ../../aws/autismxpert.pem questions.dat ubuntu@13.59.215.199://home/ubuntu/Insight/flaskapp/data/.


