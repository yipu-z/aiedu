library(tidyr)
library(dplyr)
library(jsonlite)
library(ggplot2)
library(tm)
library(SnowballC)
library(tidytext)
library(reshape2)
library(topicmodels)

## Upload Data
md0 <- fromJSON("C:/Users/zkr2/Downloads/01_Research&Project/LearningAnalytics/2020_Yipu_aiedu/data/JAIED_20132020/json_summary_1320.json")
md1 <- md0$data

# Remove prefaces of special issues from the data set
md1 <- md1[-grep("preface", md1[,1], ignore.case = TRUE),]
md1 <- md1[-grep("special issue", md1[,1], ignore.case = TRUE),]

# Separate metadate into four two-year spans
md1314 <- filter(md1, md1[,7] <= 2014)
md1516 <- filter(md1, md1[,7] >= 2015 & md1[,7] <= 2016)
md1718 <- filter(md1, md1[,7] >= 2017 & md1[,7] <= 2018)
md1920 <- filter(md1, md1[,7] >= 2019 & md1[,7] <= 2020)

## Preprocess Text

# Convert the abstract in metadata to the corpus format in tm 
abs1314 <- Corpus(VectorSource(md1314$abstract))
# Remove spaces
abs1314 <- tm_map(abs1314, stripWhitespace)
# Convert to lower case
abs1314 <- tm_map(abs1314, content_transformer(tolower)) 
# Remove pre-defined stop words ('the', 'a', etc)
abs1314 <- tm_map(abs1314, removeWords, stopwords('english'))
# Convert words to stems ("education" = "edu") for analysis, for more info see  http://tartarus.org/~martin/PorterStemmer/
abs1314 <- tm_map(abs1314, stemDocument)
# Remove numbers
abs1314 <- tm_map(abs1314, removeNumbers, lazy=TRUE)
# remove punctuation
abs1314 <- tm_map(abs1314, removePunctuation, lazy=TRUE)

# Do the same for md1516, md1718, md1920
abs1516 <- Corpus(VectorSource(md1516$abstract))
abs1516 <- tm_map(abs1516, stripWhitespace)
abs1516 <- tm_map(abs1516, content_transformer(tolower)) 
abs1516 <- tm_map(abs1516, removeWords, stopwords('english'))
abs1516 <- tm_map(abs1516, stemDocument)
abs1516 <- tm_map(abs1516, removeNumbers, lazy=TRUE)
abs1516 <- tm_map(abs1516, removePunctuation, lazy=TRUE)

abs1718 <- Corpus(VectorSource(md1718$abstract))
abs1718 <- tm_map(abs1718, stripWhitespace)
abs1718 <- tm_map(abs1718, content_transformer(tolower)) 
abs1718 <- tm_map(abs1718, removeWords, stopwords('english'))
abs1718 <- tm_map(abs1718, stemDocument)
abs1718 <- tm_map(abs1718, removeNumbers, lazy=TRUE)
abs1718 <- tm_map(abs1718, removePunctuation, lazy=TRUE)

abs1920 <- Corpus(VectorSource(md1920$abstract))
abs1920 <- tm_map(abs1920, stripWhitespace)
abs1920 <- tm_map(abs1920, content_transformer(tolower)) 
abs1920 <- tm_map(abs1920, removeWords, stopwords('english'))
abs1920 <- tm_map(abs1920, stemDocument)
abs1920 <- tm_map(abs1920, removeNumbers, lazy=TRUE)
abs1920 <- tm_map(abs1920, removePunctuation, lazy=TRUE)

## Topic modeling

# Term Frequency Inverse Document Frequency
dtm.tfi1314 <- DocumentTermMatrix(abs1314, control = list(weighting = weightTf))
dtm.tfi1516 <- DocumentTermMatrix(abs1516, control = list(weighting = weightTf))
dtm.tfi1718 <- DocumentTermMatrix(abs1718, control = list(weighting = weightTf))
dtm.tfi1920 <- DocumentTermMatrix(abs1920, control = list(weighting = weightTf))
# Remove zero entries
rowTotals <- apply(dtm.tfi1314, 1, sum) #Find the sum of words in each Document
dtm.tfi1314 <- dtm.tfi1314[rowTotals> 0, ]
rowTotals <- apply(dtm.tfi1516, 1, sum)
dtm.tfi1516 <- dtm.tfi1516[rowTotals> 0, ]
rowTotals <- apply(dtm.tfi1718, 1, sum)
dtm.tfi1718 <- dtm.tfi1718[rowTotals> 0, ]
rowTotals <- apply(dtm.tfi1920, 1, sum)
dtm.tfi1920 <- dtm.tfi1920[rowTotals> 0, ]

# Find appropriate k for the LDA Model in each two-year span
PERPvector1314 <- vector(length = 29)
for (i in 2:30) {
  a= LDA(dtm.tfi1314, k = i)
  PERPvector1314[i-1] <- perplexity(a)
}
plot(PERPvector1314, type="l", main = "Perplexity Plot (2013-2014)", xlab="+1 => # of Topics", ylab="Perplexity", xlim = c(0,30), ylim = c(0,450))

PERPvector1516 <- vector(length =29)
for (i in 2:30) {
  a= LDA(dtm.tfi1516, k = i)
  PERPvector1516[i-1] <- perplexity(a)
}
plot(PERPvector1516, type="l", main = "Perplexity Plot (2015-2016)", xlab="+1 => # of Topics", ylab="Perplexity", xlim = c(0,30), ylim = c(0,700))

PERPvector1718 <- vector(length =29)
for (i in 2:20) {
  a= LDA(dtm.tfi1718, k = i)
  PERPvector1718[i-1] <- perplexity(a)
}
plot(PERPvector1718, type="l", main = "Perplexity Plot (2017-2018)", xlab="+1 => # of Topics", ylab="Perplexity", xlim = c(0,30))

PERPvector1920 <- vector(length =29)
for (i in 2:20) {
  a= LDA(dtm.tfi1920, k = i)
  PERPvector1920[i-1] <- perplexity(a)
}
plot(PERPvector1920, type="l", main = "Perplexity Plot (2019-2020)", xlab="+1 => # of Topics", ylab="Perplexity", xlim = c(0,30))

# Let the number of topics be 21.

abs.lda1314 = LDA(dtm.tfi1314, k = 21, control = list(seed = 1234))
# Word-topic probabilities
abs.topics1314 <- tidy(abs.lda1314, matrix = "beta")
# Plot work-topic probabilities
abs.top.terms1314 <- abs.topics1314 %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)
abs.top.terms1314 %>%
  mutate(term=reorder_within(term, beta, topic)) %>%
  ggplot(aes(term, beta, fill=factor(topic))) + 
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip() +
  scale_x_reordered()

abs.lda1516 = LDA(dtm.tfi1516, k = 21, control = list(seed = 1234))
# Word-topic probabilities
abs.topics1516 <- tidy(abs.lda1516, matrix = "beta")
# Plot work-topic probabilities
abs.top.terms1516 <- abs.topics1516 %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)
abs.top.terms1516 %>%
  mutate(term=reorder_within(term, beta, topic)) %>%
  ggplot(aes(term, beta, fill=factor(topic))) + 
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip() +
  scale_x_reordered()

abs.lda1718 = LDA(dtm.tfi1718, k = 21, control = list(seed = 1234))
# Word-topic probabilities
abs.topics1718 <- tidy(abs.lda1718, matrix = "beta")
# Plot work-topic probabilities
abs.top.terms1718 <- abs.topics1718 %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)
abs.top.terms1718 %>%
  mutate(term=reorder_within(term, beta, topic)) %>%
  ggplot(aes(term, beta, fill=factor(topic))) + 
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip() +
  scale_x_reordered()

abs.lda1920 = LDA(dtm.tfi1920, k = 21, control = list(seed = 1234))
# Word-topic probabilities
abs.topics1920 <- tidy(abs.lda1920, matrix = "beta")
# Plot work-topic probabilities
abs.top.terms1920 <- abs.topics1920 %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)
abs.top.terms1920 %>%
  mutate(term=reorder_within(term, beta, topic)) %>%
  ggplot(aes(term, beta, fill=factor(topic))) + 
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip() +
  scale_x_reordered()
