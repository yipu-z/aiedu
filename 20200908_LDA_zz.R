## Process text
library(tm)
library(SnowballC)
# Convert the abstract in metadata to the corpus format in tm 
abs <- Corpus(VectorSource(md01$abstract))
# Remove spaces
abs <- tm_map(abs, stripWhitespace)
# Convert to lower case
abs <- tm_map(abs, content_transformer(tolower)) 
# Remove pre-defined stop words ('the', 'a', etc)
abs <- tm_map(abs, removeWords, stopwords('english'))
# Convert words to stems ("education" = "edu") for analysis, for more info see  http://tartarus.org/~martin/PorterStemmer/
abs <- tm_map(abs, stemDocument)
# Remove numbers
abs <- tm_map(abs, removeNumbers, lazy=TRUE)
# remove punctuation
abs <- tm_map(abs, removePunctuation, lazy=TRUE)

## LDA Topic Modeling

# Term Frequency Inverse Document Frequency
dtm.tfi <- DocumentTermMatrix(abs, control = list(weighting = weightTf))
# Remove zero entries
rowTotals <- apply(dtm.tfi , 1, sum) #Find the sum of words in each Document
dtm.tfi   <- dtm.tfi[rowTotals> 0, ]

# Find appropriate k for the LDA Model
library(topicmodels)
PERPvector <- vector(length = 49)
for (i in 2:50) {
  abs.lda = LDA(dtm.tfi, k = i)
  PERPvector[i] <- perplexity(abs.lda)
}
plot(PERPvector, type="l", main = "Perplexity Plot", xlab="# of Topics Minus 1", ylab="Perplexity")
# The plot suggests that the number of topics may be larger than 50.

# Let the number of topics be 8 as the qualitative analysis suggests.
abs.lda = LDA(dtm.tfi, k = 8, control = list(seed = 1234))
# Word-topic probabilities
library(tidytext)
library(reshape2)
abs.topics <- tidy(abs.lda, matrix = "beta")
# Plot work-topic probabilities
library(ggplot2)
library(dplyr)
abs.top.terms <- abs.topics %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)
abs.top.terms %>%
  mutate(term=reorder_within(term, beta, topic)) %>%
  ggplot(aes(term, beta, fill=factor(topic))) + 
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip() +
  scale_x_reordered()

# Document-topic probabilities
abs.documents <- tidy(abs.lda, matrix = "gamma")

# Identify documents' clusters
abs.cluster <- abs.documents %>%
  group_by(document) %>%
  top_n(1, gamma) %>%
  ungroup()

# Match documents' titles and keywords
md01.1 <- select(md01, 1, 8) 
md01.1$document <- row.names(md01.1)
abs.cluster <- left_join(abs.cluster, md01.1, by = "document")

# Add each keyword as a column
kw01 <- as.data.frame(matrix(0, nrow=nrow(abs.cluster), ncol = nrow(kw00)))
kw <- select(kw00,Key)
kw[555,1]<-c("Early STEM")
names(kw01) <- t(kw)
kw01$document <- abs.cluster$document
abs.cluster <- left_join(abs.cluster, kw01, by = "document")

# Count if a keyword is present in an article
for (j in 1:nrow(abs.cluster)) {
  for (i in 6:ncol(abs.cluster)) {
    abs.cluster[j,i] <- ifelse(
      identical(
        grep(names(abs.cluster[,i]), abs.cluster[j,5], ignore.case = TRUE), 
        integer(0)),
      abs.cluster[j,i],
      abs.cluster[j,i]+1)
  }
}

# Get top 10 keywords in each topic
tp.kw <- select(abs.cluster, 2, 6:ncol(abs.cluster))
tp.kw <- tp.kw %>%
  group_by(topic) %>%
  summarise_all(funs(sum))
library(tidyr)
tp.kw <- gather(tp.kw, "kw", "n", 2:ncol(tp.kw))

abs.top.kw <- tp.kw %>%
  group_by(topic) %>%
  top_n(10, n) %>%
  ungroup() %>%
  arrange(topic, -n)

# Visualize the top 10 keywords in each topic
abs.top.kw %>%
  mutate(kw=reorder_within(kw, n, topic)) %>%
  ggplot(aes(kw, n, fill=factor(topic))) + 
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip() +
  scale_x_reordered()
