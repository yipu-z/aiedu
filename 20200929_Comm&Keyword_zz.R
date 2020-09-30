library(jsonlite)
library(dplyr)
library(tidyr)
library(ggplot2)
library(tidytext)

## Upload Data
cl0 <- read.csv("C:/Users/zkr2/Downloads/01_Research&Project/LearningAnalytics/2020_Yipu_aiedu/data/cluster_lists_all_years.csv") #Cluster Lists
md0 <- fromJSON("C:/Users/zkr2/Downloads/01_Research&Project/LearningAnalytics/2020_Yipu_aiedu/data/JAIED_20132020/json_summary_1320.json")
md1 <- md0$data
kw0 <- read.csv("C:/Users/zkr2/Downloads/01_Research&Project/LearningAnalytics/2020_Yipu_aiedu/data/keyword_dict_0922.csv")
names(kw0) <- c("Key")

# Separate metadate into four two-year spans
md1314 <- filter(md1, md1[,7] <= 2014)
md1516 <- filter(md1, md1[,7] >= 2015 & md1[,7] <= 2016)
md1718 <- filter(md1, md1[,7] >= 2017 & md1[,7] <= 2018)
md1920 <- filter(md1, md1[,7] >= 2019 & md1[,7] <= 2020)

# Separate cluster lists into four two-year spans and one of all years
cl1320 <- select(cl0, author_13_20, comm_13_20)
cl1314 <- select(cl0, author_13_20, comm_13_14)
cl1516 <- select(cl0, author_13_20, comm_15_16)
cl1718 <- select(cl0, author_13_20, comm_17_18)
cl1920 <- select(cl0, author_13_20, comm_19_20)

# An author-article df for all years (2013-2020)
for (i in 1:nrow(cl1320)) {
  for (j in 1:nrow(md1)) {
    cl1320[i,j+2] <- 0
  }
}

for (i in 1:nrow(cl1320)) {
  for (j in 1:nrow(md1)) {
    cl1320[i,j+2] <- ifelse(
      identical(
        grep(cl1320[i,1], gsub(' ', '.',md1[j,2]), ignore.case = TRUE), 
        integer(0)),
      cl1320[i,j+2],
      cl1320[i,j+2]+1)
  }
}

# Rename new columns using the article rowID in metadata
names(cl1320) <- c("author_13_20", "comm_13_20", 1:nrow(md1))

# 
cl1320.1 <- gather(cl1320, "articleID", "yes", 3:ncol(cl1320))
cl1320.1 <- cl1320.1[,-1]
cl1320.2 <- cl1320.1 %>% group_by(comm_13_20, articleID) %>% summarise(n = sum(yes)) %>% ungroup()
cl1320.3 <- filter(cl1320.2, n > 0)
cl1320.4 <- cl1320.3[,-3]
cl1320.4$articleID <- as.numeric(cl1320.4$articleID)

for (i in 1:nrow(cl1320.4)) {
  for (j in 1:nrow(kw0)) {
    cl1320.4[i,j+2] <- 0
  }
}

for (i in 1:nrow(cl1320.4)) {
  for (j in 1:nrow(kw0)) {
    cl1320.4[i,j+2] <- ifelse(
      identical(
        grep(kw0[j,1], md1[as.numeric(cl1320.4[i,2]),8], ignore.case = TRUE), 
        integer(0)),
      cl1320.4[i,j+2],
      cl1320.4[i,j+2]+1)
  }
}

names(cl1320.4) <- c("comm_13_20", "articleID", kw0$Key)

cl1320.5 <- gather(cl1320.4, "Key", "n", 3:ncol(cl1320.4))
cl1320.5 <- cl1320.5[,-2]
cl1320.5 <- cl1320.5 %>% group_by(comm_13_20, Key) %>% summarise(n = sum(n)) %>% ungroup()

cl1320.kw.top <- cl1320.5 %>%
  group_by(comm_13_20) %>%
  top_n(5, n) %>%
  ungroup() %>%
  arrange(comm_13_20, -n)

cl1320.kw.top[which(cl1320.kw.top$comm_13_20 <= 15 & cl1320.kw.top$n > 0),] %>%
  mutate(Key=reorder_within(Key, n, comm_13_20)) %>%
  ggplot(aes(Key, n, fill=factor(comm_13_20))) + 
  geom_col(show.legend = FALSE) +
  facet_wrap(~ comm_13_20, scales = "free") +
  coord_flip() +
  scale_x_reordered()
