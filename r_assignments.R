library(readxl)
library(plyr)
library(dplyr)

excel_sheets("SaleData.xlsx")
df <- read_excel("SaleData.xlsx", sheet = "Sales Data")
diamond<-read.csv("diamonds.csv")
movie<-read.csv('movie_metadata.csv')
imdb<-read.csv('imdb.csv',header = T)

#Question-1
q1 <- df %>% group_by(Item) %>% summarise(min_sales = min(Sale_amt))
print(q1)

# Question-2
q2 <- df %>% group_by(format(as.Date(OrderDate,format="%Y-%m-%d"),"%Y"),Region) %>% summarise(total_sales = sum(Sale_amt))
print(q2)

#Question-3
df$days_diff <- Sys.Date()- as.Date(df$OrderDate,format="%Y-%m-%d")
print(head(df))

#Question-4
data1 <- data.frame(manager=df$Manager,list_of_salesmen=df$SalesMan)
q4 <- data1 %>% group_by(manager) %>% summarise(list_of_salesmen = paste(unique(list_of_salesmen),collapse = ","))
print(q4)

#Question-5
data2 <- data.frame(Region=df$Region,Salesmen_count=df$SalesMan, total_sales=df$Sale_amt)
data3 <- data2 %>% group_by(Region) %>%  summarise(total_sales= sum(total_sales))
data4 <- data2 %>% group_by(Region) %>% count(Salesmen_count) %>% count(Region)
q5 <- data.frame(data3,Salesmen_count=data4$n)
print(q5)

#Question-6
data6 <- data.frame(Manager=df$Manager, Total_sale=df$Sale_amt)
total_sale_amount= sum(df$Sale_amt)
q6 <- data6 %>% group_by(Manager) %>% summarise(percent_sales= sum(Total_sale)*100/total_sale_amount)
print(q6)

#Question-7

q7<-imdb[5,6]
print(q7)


#Question-8

q8<-function(df){
  i<-2
  while(i<=14762){
    #print(i)
    if(!is.na(df[i,45])){
      #print(i)
      df<-df[-c(i),]
    }
    i=i+1
  }
  ma<-which.max(df$duration)
  mi<-which.min(df$duration)
  r1<-as.numeric(ma)
  r2<-as.numeric(mi)
  df$duration<-as.numeric(as.character(df$duration))
  print("title:")
  print(df[r1,3])
  print("duration:")
  print(df[r1,8])
  print("title:")
  print(df[r2,3])
  print("duration:")
  print(df[r2,8])
}
q8(imdb)

#Question-9
q9<-function(df){
  i<-2
  while(i<=14762){
    #print(i)
    if(!is.na(df[i,45])){
      #print(i)
      df<-df[-c(i),]
    }
    i=i+1
  }
  df$imdbRating<-as.numeric(as.character(df$imdbRating))
  f <-df[order(df$year,-df$imdbRating),]
  return(f)
}
q9(imdb)

#Question-10
q10<-function(df){
  newdata <- subset(df, gross>2000000)
  newdata1 <- subset(newdata, budget<1000000)
  newdata2 <- subset(newdata1, duration >= 30 & duration < 180)
  return(newdata2)
}
q10(movie)



#Question-11
q11<-function(df){
  r<-(nrow(df)-nrow(distinct(df)))
  return(r)
}
q11(diamond)

#Question-12
q12<-function(df){
  df <- df[-which(df$carat == ""), ]
  df <- df[-which(df$cut == ""), ]
  return(df)
}
q12(diamond)

#Question-13
q13<-function(df){
  r<-select_if(df,is.numeric)
  return(r)
}
q13(diamond)


#Question-14
diamond$z<-as.numeric(as.character(diamond$z))
cbind(diamond,volume=0)

q14<-function(df){
  i<-1
  while(i<=53943)
  {
    if(df[i,5]>60){
      df[i,"volume"]<-df[i,8]*df[i,9]*df[i,10]
    } else{
      df[i,"volume"]<-8
    }
    i=i+1
  }
  return(df)
}
q14(diamond)

#Question-15
q15<-function(df){
  i<-1
  df[is.na(df)]<-0
  m<-mean(df$price)
  while(i<=53943){
    if((df[i,7])==0){
      df[i,7]<-m
    }
    i=i+1
  }
  return(df)
}
q15(diamond)

