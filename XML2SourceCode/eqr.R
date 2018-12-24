library("e1071")
library("rfUtilities")

head(iris,5)


set.seed(101) # Set Seed so that same sample can be reproduced in future also
# Now Selecting 80% of data as sample from total 'n' rows of the data  

x <- subset(iris, select=-Species)
y <- Species

sample <- sample.int(n = nrow(iris), size = floor(.8*nrow(iris)), replace = F)
x_train <- x[sample, ]
x_test  <- x[-sample, ]
y_train <- y[sample, ]
y_test <- y[-sample, ]

#train <- iris[1:120, ]
#test  <- iris[121:150, ]
attach(train)


x_train <- subset(train, select=-Species)
y_train <- Species

attach(test)

x_test <- subset(test, select=-Species)
y_test <- Species
print(y_test)

#print(Species)
#print(subset(train, select=Species))
#print(Species)




svm_model <- svm(x_train,y_train, kernel ="radial", degree = 3 )
summary(svm_model)
pred <- predict(svm_model,x_test)
system.time(pred <- predict(svm_model,x_test))
#table(pred,y_test)

accuracy(pred, y_test)






