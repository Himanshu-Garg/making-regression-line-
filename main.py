import math

"""

Here, data is in the form (journal_name;H-Index;Impact_factor)
i.e. each is seperated by a semi-colon (;)

We have to obtain the regression line
so, want Xi*Yi, n (total no of observation), mean(x), mean(y) and pow(Xi,2) ------ which will be inserted in a new file in the same order as shown

so, our final table will be in order   [Xi,Yi,Xi*Yi,pow(Xi,2)]

"""

summation_xi=0
summation_yi=0
summation_xi_square=0
summation_XiYi=0

file_from = open("journal/training_data.txt","r")
open('journal/processed_data.txt', 'w').close()				#to erase all the contents in that file
file_to = open("journal/processed_data.txt","a")

data=file_from.readlines()
n=len(data)

#---------------------------------- for processing data line by line -------------------------------------------------------------

for i in range(0,n):
	temp_data=list(map(str,data[i].split(";")))
	Xi=float(temp_data[1])
	Yi=float(temp_data[2])
	#print(Xi, "  ",  Yi)
	XiYi=Xi * Yi
	Xi_square = Xi * Xi

	# for making table in processed_data file-------------------------------------------------------------------------------

	s=temp_data[0] + ";" + temp_data[1] + ";" + temp_data[2][:-1] + ";" + str(XiYi) + ";" + str(Xi_square) + "\n"
	file_to.write(s)
	#print(s)

	#------------------------------------------------------------------------------------------------------------------------------


	summation_xi+=Xi 								#calculating summation of Xi for mean
	summation_yi+=Yi 								#calculating summation of Yi for mean
	summation_xi_square+=Xi_square					#calculating summation of Xi square for mean
	summation_XiYi+=XiYi							#calculating summation of Xi*Yi for mean

#print(summation_xi)
#print(summation_yi)
#print(summation_XiYi)
#print(summation_xi_square)

#-------------------------------------- for making regression line ----------------------------------------------------------------


mean_x = summation_xi / n
mean_y = summation_yi / n
#print(mean_y, mean_x)

"""
since, line is of the form y = ax + b;
where:
	a=covar(x,y)/var(x);
	b=mean(y) - a* mean(x);
"""

a=( (summation_XiYi/n) - (mean_y*mean_x) ) / ( (summation_xi_square/n)-(mean_x*mean_x) )
b=( mean_y - (a*mean_x) )

print ("regression line : " + "y = " + str(a) + " x + " + str(b))

# ---------------------------------------------------------------------------------------------------------------------------------

# -------------------------- working on test data ---------------------------------------------------------------------------------

file1 = open("journal/test_data.txt","r")
open('journal/test_data_after_predicting.txt', 'w').close()				#to erase all the contents in that file
file2 = open("journal/test_data_after_predicting.txt","a")

"""
here, in test_data_after_predicting file contains data after prediction and % error for each row;
and the format of the file is:
	[journal name ; H-index; impact factor (actual) ; impact factor (predicted); error]
"""
data=file1.readlines()
n=len(data)
summation_error_squared=0

for i in range(0,n):
	temp_data=list(map(str,data[i].split(";")))
	actual_IF=float(temp_data[2][:-1])
	predicted_IF = ( a * float(temp_data[1]) ) + b
	error = ( predicted_IF - actual_IF )
	summation_error_squared += error * error
	
	#for writing data to test_data_after_predicting.txt in prescribed format
	s=temp_data[0] + ";" + temp_data[1] + ";" + temp_data[2][:-1] + ";" + str(predicted_IF) + ";" + str(error) + "\n"
	file2.write(s)

#print(summation_percentage_error)
print ("error percentage(mean squared error) = " + str(summation_error_squared/n))
#----------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------- for predicting conferences impact factor ---------------------------------------------

file3 = open("cleaning_conferences/conferences_after.txt","r")
open('cleaning_conferences/conferences_with_predicted_data.txt', 'w').close()				#to erase all the contents in that file
file4 = open('cleaning_conferences/conferences_with_predicted_data.txt',"a")

data=file3.readlines()
n=len(data)
for i in range(1,n):

	try:							#since, some vaues dont have h-Index
		temp_data=list(map(str,data[i].split(";")))
		predicted_IF = ( a * float(temp_data[1][1:-1]) ) + b
		s=temp_data[0] + ";" + temp_data[1][1:-1] + " ; " + str(predicted_IF) + "\n"
		file4.write(s)
	except:
		a="a"


#----------------------------------------------------------------------------------------------------------------------------------

file_from.close()
file_to.close()
file1.close()
file2.close()
file3.close()
file4.close()
