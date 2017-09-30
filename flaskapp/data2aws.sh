#scp -i ../aws/autismxpert.pem views.py ubuntu@13.59.215.199://home/ubuntu/Insight/flaskapp/.
scp -i ../aws/autismxpert.pem query_model.py ubuntu@13.59.215.199://home/ubuntu/Insight/flaskapp/.
#scp -i ../aws/autismxpert.pem get_questions.py ubuntu@13.59.215.199://home/ubuntu/Insight/flaskapp/.

#scp -i ../aws/autismxpert.pem -r static ubuntu@13.59.215.199://home/ubuntu/Insight/flaskapp/.

#cd data
#bash data2aws.sh
#cd ..
#

#cd static
#bash data2aws.sh
#cd ..

#cd templates
#bash data2aws.sh
#cd ..
