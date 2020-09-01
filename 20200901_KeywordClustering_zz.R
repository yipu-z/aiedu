library(jsonlite)
library(dplyr)

# Upload Data
md00 <- fromJSON("C:/Users/zkr2/Downloads/01_Research&Project/LearningAnalytics/2020_Yipu_aiedu/data/json_summary.json")
md01 <- md00$data
kw00 <- read.csv("C:/Users/zkr2/Downloads/01_Research&Project/LearningAnalytics/2020_Yipu_aiedu/data/keyword_dict.csv")

# Select all key words
ka.m <- select(kw00,Key)

# Remove "(Science"
ka.m[555,1]<-c("Early STEM")

# Create a frame for the keyword-article matrix
for (j in 1:nrow(ka.m)) {
  for (i in 1:nrow(md01)) {
    ka.m[j,i+1] <- 0
  }
}

# Build the keyword-article matrix
for (j in 1:nrow(ka.m)) {
  for (i in 1:nrow(md01)) {
    ka.m[j,i+1] <- ifelse(
      identical(
       grep(ka.m[j,1], md01[i,8], ignore.case = TRUE), 
        integer(0)),
      ka.m[j,i+1],
      ka.m[j,i+1]+1)
  }
}
ka.m <- as.matrix(ka.m[,-1])
rownames(ka.m) = kw00$Key

# Get the keyword-keyword matrix
k.m <- ka.m
k.m = k.m %*% t(k.m)
names(k.m) = kw00$Key
rownames(k.m) = kw00$Key

# K-means Clustering
WSSvector <- vector(length = 15)
for (i in 1:15) {
  cl <- kmeans(k.m,i)
  WSSvector[i] <- cl$tot.withinss
}
plot(WSSvector, type="l", main = "Scree Plot", xlab="# of Clusters", ylab="Total Sum of Squared Difference from Cluster Centers")
## Num of topics can be around 4.
cl4 <- kmeans(k.m,4)
cl8 <- kmeans(k.m,8)

# Hiearchical Clustering
## the additive tree
ka.m.d = dist(ka.m,method="euclidean")
ka.m.add.tree = hclust(ka.m.d,method="ward.D2")
plot(ka.m.add.tree)
ka.m.cut4 <- cutree(ka.m.add.tree, k=4)
ka.m.cut8 <- cutree(ka.m.add.tree, k=8)

# comparison
comp <- as.data.frame(matrix(nrow=nrow(kw00), ncol=4))
comp[,1] <- cl4$cluster
comp[,3] <- cl8$cluster
comp[,2] <- ka.m.cut4
comp[,4] <- ka.m.cut8
rownames(comp) = kw00$Key
names(comp) = c("kmeans4","addtree4","kmeans8","addtree8")
